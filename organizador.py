#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organizador de Arquivos Inteligente
------------------------------------
Organiza os arquivos de uma pasta do seu computador em subpastas por
categoria, detecta duplicados e sugere nomes melhores — tudo rodando
localmente, sem enviar nada para fora.

Uso básico:
    python3 organizador.py "C:/Users/voce/Downloads"                 -> mostra o que seria feito (não move nada)
    python3 organizador.py "C:/Users/voce/Downloads" --aplicar        -> aplica as mudanças de verdade
    python3 organizador.py "C:/Users/voce/Downloads" --desfazer       -> desfaz a última organização aplicada
    python3 organizador.py "C:/Users/voce/Downloads" --duplicados     -> só lista os duplicados encontrados

Segurança:
    - Por padrão o script SEMPRE roda em modo "simulação" (dry-run): mostra o
      que faria, mas não move nenhum arquivo até você usar --aplicar.
    - Nunca exclui arquivos. Duplicados vão para uma subpasta "_Duplicados"
      dentro da própria pasta, para você revisar e decidir.
    - Toda operação aplicada fica registrada em .organizador_logs/, o que
      permite desfazer com --desfazer.
    - Em caso de conflito de nomes, o arquivo original nunca é sobrescrito.
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ------------------------------------------------------------------ #
# Categorias por extensão — ajuste à vontade
# ------------------------------------------------------------------ #
CATEGORIAS = {
    "Documentos":     [".doc", ".docx", ".odt", ".txt", ".rtf", ".md"],
    "Planilhas":      [".xls", ".xlsx", ".ods", ".csv"],
    "Apresentacoes":  [".ppt", ".pptx", ".odp", ".key"],
    "PDFs":           [".pdf"],
    "Imagens":        [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".svg", ".tiff"],
    "Videos":         [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Musica":         [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Compactados":    [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Programas":      [".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage"],
    "Codigo":         [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".json",
                        ".xml", ".sh", ".rb", ".go", ".rs"],
}
PASTAS_CATEGORIA = set(CATEGORIAS.keys()) | {"_Duplicados", "_Renomeados"}
NOME_LOG_DIR = ".organizador_logs"

# Padrões de nomes "genéricos" que ganham sugestão de renomeação
PREFIXOS_GENERICOS = ("img_", "screenshot", "download_", "documento", "sem título", "sem titulo", "novo documento")


# ------------------------------------------------------------------ #
# Utilidades
# ------------------------------------------------------------------ #
def cor(texto, codigo):
    if not sys.stdout.isatty():
        return texto
    return f"\033[{codigo}m{texto}\033[0m"


def categoria_de(ext):
    ext = ext.lower()
    for nome, extensoes in CATEGORIAS.items():
        if ext in extensoes:
            return nome
    return "Outros"


def tamanho_legivel(bytes_):
    for unidade in ["B", "KB", "MB", "GB"]:
        if bytes_ < 1024:
            return f"{bytes_:.0f} {unidade}" if unidade == "B" else f"{bytes_:.1f} {unidade}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


def hash_arquivo(caminho, bloco=65536):
    h = hashlib.md5()
    try:
        with open(caminho, "rb") as f:
            while chunk := f.read(bloco):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def listar_arquivos(pasta):
    """Lista só os arquivos no primeiro nível da pasta, ignorando subpastas
    que já são categorias (para não reorganizar o que já foi organizado)
    e ignorando o diretório de logs."""
    itens = []
    for entrada in os.scandir(pasta):
        if entrada.is_dir():
            continue
        if entrada.name.startswith("."):
            continue
        itens.append(Path(entrada.path))
    return itens


def caminho_sem_colisao(destino):
    """Se já existe um arquivo com esse nome no destino, acrescenta (1), (2)... """
    if not destino.exists():
        return destino
    base, ext = destino.stem, destino.suffix
    i = 1
    while True:
        candidato = destino.with_name(f"{base} ({i}){ext}")
        if not candidato.exists():
            return candidato
        i += 1


SINGULAR = {
    "Documentos": "Documento", "Planilhas": "Planilha", "Apresentacoes": "Apresentacao",
    "PDFs": "PDF", "Imagens": "Imagem", "Videos": "Video", "Musica": "Musica",
    "Compactados": "Compactado", "Programas": "Programa", "Codigo": "Codigo", "Outros": "Arquivo",
}


def sugerir_nome(caminho, categoria):
    nome = caminho.stem.lower()
    if not nome.startswith(PREFIXOS_GENERICOS):
        return None
    try:
        data = datetime.fromtimestamp(caminho.stat().st_mtime)
    except OSError:
        data = datetime.now()
    base = SINGULAR.get(categoria, categoria)
    sufixo = caminho.stem[-4:] if caminho.stem[-4:].isdigit() else data.strftime("%H%M%S")
    novo = f"{base}_{data.strftime('%Y-%m-%d')}_{sufixo}{caminho.suffix}"
    return novo


# ------------------------------------------------------------------ #
# Núcleo: analisar, planejar, aplicar
# ------------------------------------------------------------------ #
def analisar(pasta):
    arquivos = listar_arquivos(pasta)
    info = []
    hashes = {}
    for caminho in arquivos:
        try:
            stat = caminho.stat()
        except OSError:
            continue
        categoria = categoria_de(caminho.suffix)
        h = hash_arquivo(caminho) if stat.st_size < 200 * 1024 * 1024 else None  # evita hashear arquivos gigantes
        item = {
            "caminho": caminho,
            "categoria": categoria,
            "tamanho": stat.st_size,
            "hash": h,
        }
        info.append(item)
        if h:
            hashes.setdefault(h, []).append(item)

    duplicados = {h: v for h, v in hashes.items() if len(v) > 1}
    return info, duplicados


def montar_plano(pasta, info, duplicados, renomear=False):
    pasta = Path(pasta)
    ids_duplicados_secundarios = set()
    for grupo in duplicados.values():
        grupo_ordenado = sorted(grupo, key=lambda x: x["caminho"].stat().st_mtime)
        for item in grupo_ordenado[1:]:
            ids_duplicados_secundarios.add(str(item["caminho"]))

    plano = []
    for item in info:
        caminho = item["caminho"]
        chave = str(caminho)

        if chave in ids_duplicados_secundarios:
            destino_pasta = pasta / "_Duplicados"
            motivo = "duplicado"
            novo_nome = caminho.name
        else:
            destino_pasta = pasta / item["categoria"]
            motivo = "categoria"
            novo_nome = caminho.name
            if renomear:
                sugestao = sugerir_nome(caminho, item["categoria"])
                if sugestao:
                    novo_nome = sugestao

        destino = destino_pasta / novo_nome
        if destino.parent == caminho.parent and destino.name == caminho.name:
            continue  # já está no lugar certo, nada a fazer

        plano.append({
            "origem": caminho,
            "destino": destino,
            "motivo": motivo,
            "categoria": item["categoria"],
            "tamanho": item["tamanho"],
        })
    return plano


def imprimir_plano(plano, duplicados):
    if not plano:
        print(cor("\n✓ Tudo já está organizado nessa pasta.", "32"))
        return

    por_categoria = {}
    for p in plano:
        por_categoria.setdefault(p["categoria"], []).append(p)

    print(cor(f"\n{len(plano)} arquivo(s) seriam organizados:\n", "1"))
    for categoria, itens in por_categoria.items():
        total = tamanho_legivel(sum(i["tamanho"] for i in itens))
        print(cor(f"  {categoria}", "36") + f"  ({len(itens)} arquivos, {total})")
        for i in itens[:5]:
            marca = cor(" [duplicado]", "33") if i["motivo"] == "duplicado" else ""
            print(f"    {i['origem'].name}  →  {i['destino'].relative_to(i['destino'].parents[1])}{marca}")
        if len(itens) > 5:
            print(f"    ... e mais {len(itens) - 5} arquivo(s)")
        print()

    if duplicados:
        espaco = sum(sorted(g, key=lambda x: x['caminho'].stat().st_mtime)[1:][0]['tamanho']
                     for g in duplicados.values() for _ in [0])
        total_dup_kb = sum(item["tamanho"] for grupo in duplicados.values()
                            for item in sorted(grupo, key=lambda x: x["caminho"].stat().st_mtime)[1:])
        print(cor(f"⚠ {len(duplicados)} grupo(s) de arquivos duplicados encontrados ", "33")
              + f"— mover para _Duplicados pode liberar até {tamanho_legivel(total_dup_kb)}.\n")


def aplicar_plano(pasta, plano, confirmar=True):
    if not plano:
        return

    if confirmar:
        resposta = input(cor(f"Confirmar e mover {len(plano)} arquivo(s)? Digite SIM para continuar: ", "1"))
        if resposta.strip().upper() != "SIM":
            print("Operação cancelada. Nada foi alterado.")
            return

    registro = []
    erros = []
    for item in plano:
        origem, destino = item["origem"], item["destino"]
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino_final = caminho_sem_colisao(destino)
        try:
            shutil.move(str(origem), str(destino_final))
            registro.append({"origem": str(origem), "destino": str(destino_final)})
        except (OSError, PermissionError) as e:
            erros.append((origem.name, str(e)))

    log_dir = Path(pasta) / NOME_LOG_DIR
    log_dir.mkdir(exist_ok=True)
    nome_log = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_dir / nome_log, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)

    print(cor(f"\n✓ {len(registro)} arquivo(s) movidos com sucesso.", "32"))
    print(f"  Registro salvo em: {log_dir / nome_log}")
    print(f"  Para desfazer: python3 organizador.py \"{pasta}\" --desfazer\n")

    if erros:
        print(cor(f"⚠ {len(erros)} arquivo(s) não puderam ser movidos:", "33"))
        for nome, msg in erros:
            print(f"    {nome}: {msg}")


def desfazer(pasta):
    log_dir = Path(pasta) / NOME_LOG_DIR
    if not log_dir.exists():
        print("Nenhum registro de organização encontrado nessa pasta.")
        return

    logs = sorted(log_dir.glob("log_*.json"))
    if not logs:
        print("Nenhum registro de organização encontrado nessa pasta.")
        return

    ultimo = logs[-1]
    with open(ultimo, encoding="utf-8") as f:
        registro = json.load(f)

    print(cor(f"Desfazendo {len(registro)} movimentação(ões) do registro {ultimo.name}...", "1"))
    resposta = input("Confirmar? Digite SIM para continuar: ")
    if resposta.strip().upper() != "SIM":
        print("Operação cancelada.")
        return

    restaurados = 0
    for mov in reversed(registro):
        origem, destino = Path(mov["origem"]), Path(mov["destino"])
        if destino.exists():
            origem.parent.mkdir(parents=True, exist_ok=True)
            destino_volta = caminho_sem_colisao(origem)
            shutil.move(str(destino), str(destino_volta))
            restaurados += 1

    ultimo.unlink()
    print(cor(f"✓ {restaurados} arquivo(s) restaurados para o local original.", "32"))


def apenas_duplicados(pasta):
    _, duplicados = analisar(pasta)
    if not duplicados:
        print(cor("Nenhum arquivo duplicado encontrado.", "32"))
        return
    print(cor(f"{len(duplicados)} grupo(s) de duplicados encontrados:\n", "1"))
    for h, grupo in duplicados.items():
        grupo_ordenado = sorted(grupo, key=lambda x: x["caminho"].stat().st_mtime)
        print(f"  Hash {h[:10]}...  ({tamanho_legivel(grupo_ordenado[0]['tamanho'])} cada)")
        for item in grupo_ordenado:
            tag = " (mais antigo — mantido)" if item is grupo_ordenado[0] else " (cópia)"
            print(f"    {item['caminho']}{tag}")
        print()


# ------------------------------------------------------------------ #
# CLI
# ------------------------------------------------------------------ #
def main():
    parser = argparse.ArgumentParser(
        description="Organiza arquivos de uma pasta do seu computador por categoria, com segurança.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pasta", help="Caminho da pasta a organizar (ex: C:/Users/voce/Downloads)")
    parser.add_argument("--aplicar", action="store_true", help="Aplica de verdade as mudanças (padrão é só simular)")
    parser.add_argument("--desfazer", action="store_true", help="Desfaz a última organização aplicada nessa pasta")
    parser.add_argument("--duplicados", action="store_true", help="Só lista os arquivos duplicados encontrados")
    parser.add_argument("--renomear", action="store_true", help="Também sugere/renomeia arquivos com nomes genéricos (IMG_1234.jpg etc.)")
    parser.add_argument("-y", "--sim", action="store_true", help="Não pedir confirmação antes de aplicar (use com cuidado)")
    args = parser.parse_args()

    pasta = Path(args.pasta).expanduser().resolve()
    if not pasta.exists() or not pasta.is_dir():
        print(cor(f"Erro: a pasta '{pasta}' não existe ou não é um diretório.", "31"))
        sys.exit(1)

    if args.desfazer:
        desfazer(pasta)
        return

    if args.duplicados:
        apenas_duplicados(pasta)
        return

    print(cor(f"Analisando: {pasta}", "1"))
    info, duplicados = analisar(pasta)
    plano = montar_plano(pasta, info, duplicados, renomear=args.renomear)
    imprimir_plano(plano, duplicados)

    if args.aplicar:
        aplicar_plano(pasta, plano, confirmar=not args.sim)
    elif plano:
        print(cor("Isto foi apenas uma simulação — nada foi movido.", "2"))
        print(f"Para aplicar de verdade, rode: python3 organizador.py \"{pasta}\" --aplicar\n")


if __name__ == "__main__":
    main()
