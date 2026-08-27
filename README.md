# F.R.I.D.A.Y. — by Axolotl BR

Ferramenta desktop de organização inteligente de arquivos, pastas, vídeos e
projetos de trabalho. Roda 100% local — nada é enviado para a internet.

**Filosofia:** *Understand first. Organize second. Delete never.*

## Como rodar

Precisa apenas de Python 3.9+ (Windows já vem com ele, ou baixe em
python.org). A interface usa só a biblioteca padrão (`tkinter`).

```bash
python friday_gui.py
```

Isso abre a janela do F.R.I.D.A.Y. Clique em **ESCOLHER PASTA** e selecione
a pasta que você quer organizar (por exemplo, Downloads, ou uma pasta de
projetos).

**Opcional, mas recomendado** — para gerar planilhas `.xlsx` de verdade
(formatadas, com filtro e cabeçalho colorido) em vez de `.csv`:

```bash
pip install openpyxl
```

Sem isso, o F.R.I.D.A.Y. ainda gera a planilha, só que em `.csv` (que abre
normalmente no Excel/Google Sheets).

## O que ele faz

- **Separa arquivos por tipo**: Documentos, Planilhas, Apresentações, PDFs,
  Imagens, Vídeos, Música, Compactados, Programas, Código.
- **Separa por projeto**: pastas com `.git`, `package.json`,
  `requirements.txt`, arquivos `.prproj`/`.aep` etc. são reconhecidas como
  projetos inteiros e movidas para `PROJECTS/CODE/...` ou
  `PROJECTS/EDITING/...` sem mexer no conteúdo interno — nenhum projeto
  quebra.
- **Identifica vídeos de jogos** pelo nome do arquivo/pasta (ex.: "CS2" ou
  "Deadlock" no nome vai para `VIDEOS/GAMES/<Jogo>/<Tipo>`). Você adiciona
  seus próprios jogos na tela **Regras**.
- **Dá um ID e tags para cada item organizado** (ex.: `FRD-00042`, tags
  `["cs2", "highlights", "mp4", "2026"]`). Isso fica registrado no catálogo
  interno (`.friday/catalogo.json`) e é a base da planilha exportável.
- **Encontra duplicados de verdade** (por hash do conteúdo, não só nome) —
  vão para `_Duplicados/`, mantendo o mais antigo no lugar.
- **Encontra pastas vazias e arquivos de lixo** (`Thumbs.db`,
  `desktop.ini`, `.tmp`, `.crdownload`, `.log` etc.) na tela **Limpeza**.
  Arquivos de lixo são movidos para `_Lixeira/` (nunca apagados de
  verdade); pastas vazias são removidas mas podem ser recriadas pelo
  Histórico.
- **Preview de cada coisa, antes de qualquer alteração**: as telas
  **Revisar alterações** e **Limpeza** mostram exatamente o que vai
  acontecer — origem, destino, categoria, tags, confiança e motivo — e
  você escolhe o que aprovar.
- **100% reversível**: toda operação (organização ou limpeza) fica
  registrada no **Histórico**, com um botão **DESFAZER** que devolve tudo
  — inclusive recria pastas vazias que foram removidas.
- **Gera planilha** (botão "GERAR PLANILHA" no Dashboard): exporta todo o
  catálogo — ID, nome, categoria, projeto/jogo, tags, tamanho, caminho,
  hash e data — em `.xlsx` (ou `.csv` sem o openpyxl).
- **Regras personalizadas**: diga que arquivos com "meuprojeto" no nome
  sempre vão para uma pasta específica — tem prioridade sobre a
  classificação automática.
- **Pastas protegidas**: pastas que o F.R.I.D.A.Y. nunca toca (por padrão:
  `Downloads`, `node_modules`, `.git`, `AppData`).
- **Três modos** (SAFE / SMART / AUTO) salvos nas regras, para guiar o
  quanto o F.R.I.D.A.Y. deveria confiar nas próprias decisões — SAFE é o
  mais indicado para começar.

## Estrutura de pastas criada

```
SUA_PASTA/
├── Documentos/  Planilhas/  PDFs/  Imagens/  Musica/  Compactados/
├── Programas/   Codigo/
├── VIDEOS/GAMES/<Jogo>/{Clips,Highlights,Gameplay,Recordings}/
├── PROJECTS/{CODE,EDITING}/<nome do projeto>/
├── UNSORTED/            ← baixa confiança, para você revisar
├── _Duplicados/
├── _Lixeira/            ← arquivos de lixo movidos pela Limpeza
└── .friday/             ← catálogo, regras e logs internos (não mexa aqui)
    ├── friday_regras.json
    ├── catalogo.json
    ├── friday_catalogo.xlsx   ← gerado ao clicar em "GERAR PLANILHA"
    └── operacao_*.json        ← um log por operação, usado no Undo
```

## Arquivos

- `friday_core.py` — todo o motor: classificação, projetos, catálogo
  (IDs/tags), duplicados, pastas vazias, limpeza, geração de planilha,
  histórico e undo. Pode ser usado sozinho, sem a interface, se você
  quiser automatizar por script.
- `friday_gui.py` — a interface gráfica (Dashboard, Revisar alterações,
  Limpeza, Histórico, Regras).

## Próximos passos naturais

A base já foi pensada para crescer: o motor de classificação é uma função
só (`classificar_arquivo` em `friday_core.py`), então dá pra plugar ali
coisas como extração de metadados de vídeo com `ffprobe`, aprendizado a
partir de correções do usuário na interface, busca em linguagem natural
sobre o catálogo, ou uma identidade visual ainda mais elaborada da
Axolotl BR. Me diga qual dessas você quer primeiro.
