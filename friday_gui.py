#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F.R.I.D.A.Y. — Interface gráfica desktop.
by Axolotl BR

Rodar com:  python3 friday_gui.py
Requisitos: apenas a biblioteca padrão do Python (tkinter já vem com o Python
no Windows). Nada é enviado para a internet — tudo roda localmente.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional

import friday_core as fc

# --------------------------------------------------------------------------- #
# Paleta — Axolotl BR
# Fundo escuro-azulado (água profunda) + rosa-coral (axolote) + verde-água (guelras)
# --------------------------------------------------------------------------- #
BG_APP       = "#10151b"
BG_PAINEL    = "#171e26"
BG_CARD      = "#1c2530"
BORDA        = "#2a3542"
TEXTO        = "#e7edf3"
TEXTO_FRACO  = "#7c8a9a"
ROSA_AXOLOTL = "#ff8fa3"
ROSA_ESCURO  = "#e06c82"
AGUA         = "#49c7b8"
AMARELO      = "#e8b750"
VERMELHO     = "#e2665c"

FONTE_TITULO = ("Segoe UI Semibold", 20)
FONTE_SUB    = ("Segoe UI", 10)
FONTE_CORPO  = ("Segoe UI", 10)
FONTE_MONO   = ("Consolas", 9)


# --------------------------------------------------------------------------- #
# Widgets utilitários
# --------------------------------------------------------------------------- #
def marca_axolotl(pai, tamanho=26):
    """Pequena assinatura visual: duas 'guelras' estilizadas em forma de leque,
    lembrando um axolote, sem virar mascote infantil."""
    c = tk.Canvas(pai, width=tamanho, height=tamanho, bg=pai["bg"],
                  highlightthickness=0)
    cx, cy = tamanho / 2, tamanho / 2
    c.create_oval(cx - tamanho * 0.32, cy - tamanho * 0.32,
                   cx + tamanho * 0.32, cy + tamanho * 0.32,
                   fill=BG_CARD, outline=ROSA_AXOLOTL, width=2)
    for ang in (-35, 0, 35):
        import math
        rad = math.radians(ang - 90)
        x2 = cx + math.cos(rad) * tamanho * 0.55
        y2 = cy + math.sin(rad) * tamanho * 0.55
        c.create_line(cx, cy - tamanho * 0.15, x2, y2, fill=AGUA, width=2,
                       capstyle=tk.ROUND)
    return c


class Cartao(tk.Frame):
    def __init__(self, pai, titulo, valor, cor=ROSA_AXOLOTL, **kw):
        super().__init__(pai, bg=BG_CARD, highlightbackground=BORDA,
                          highlightthickness=1, **kw)
        tk.Label(self, text=titulo, bg=BG_CARD, fg=TEXTO_FRACO, wraplength=190,
                  justify="left", font=FONTE_SUB).pack(anchor="w", padx=16, pady=(14, 0))
        self.valor_lbl = tk.Label(self, text=valor, bg=BG_CARD, fg=cor,
                                   font=("Segoe UI Semibold", 22))
        self.valor_lbl.pack(anchor="w", padx=16, pady=(0, 14))

    def set_valor(self, valor):
        self.valor_lbl.config(text=valor)


def botao(pai, texto, comando, cor=ROSA_AXOLOTL, cor_texto="#10151b", **kw):
    b = tk.Button(pai, text=texto, command=comando, bg=cor, fg=cor_texto,
                   activebackground=cor, activeforeground=cor_texto,
                   font=("Segoe UI Semibold", 10), bd=0, padx=16, pady=9,
                   cursor="hand2", **kw)
    return b


def botao_secundario(pai, texto, comando, **kw):
    b = botao(pai, texto, comando, cor=BG_PAINEL, cor_texto=TEXTO, **kw)
    b.config(highlightbackground=BORDA, highlightthickness=1)
    return b


# --------------------------------------------------------------------------- #
# App principal
# --------------------------------------------------------------------------- #
class FridayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("F.R.I.D.A.Y. — by Axolotl BR")
        self.geometry("1080x680")
        self.configure(bg=BG_APP)
        self.minsize(920, 600)
        self._estilo_ttk()

        self.pasta_raiz: Optional[Path] = None
        self.engine: Optional[fc.Friday] = None
        self.plano = []
        self.duplicados = {}
        self.limpeza = []

        self._layout_base()
        self._pagina_dashboard()

    # ---------------------------------------------------------------- #
    def _estilo_ttk(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", background=BG_CARD, fieldbackground=BG_CARD,
                          foreground=TEXTO, rowheight=26, borderwidth=0,
                          font=FONTE_CORPO)
        estilo.configure("Treeview.Heading", background=BG_PAINEL, foreground=TEXTO_FRACO,
                          font=("Segoe UI Semibold", 9), borderwidth=0)
        estilo.map("Treeview", background=[("selected", "#2a3a44")],
                   foreground=[("selected", ROSA_AXOLOTL)])
        estilo.configure("TRadiobutton", background=BG_CARD, foreground=TEXTO,
                          font=FONTE_CORPO)
        estilo.map("TRadiobutton", background=[("active", BG_CARD)])

    def _layout_base(self):
        self.sidebar = tk.Frame(self, bg=BG_PAINEL, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        topo = tk.Frame(self.sidebar, bg=BG_PAINEL)
        topo.pack(fill="x", pady=(22, 26), padx=18)
        marca_axolotl(topo).pack(side="left")
        txt = tk.Frame(topo, bg=BG_PAINEL)
        txt.pack(side="left", padx=(10, 0))
        tk.Label(txt, text="F.R.I.D.A.Y.", bg=BG_PAINEL, fg=TEXTO,
                  font=("Segoe UI Semibold", 13)).pack(anchor="w")
        tk.Label(txt, text="Axolotl BR", bg=BG_PAINEL, fg=AGUA,
                  font=("Segoe UI", 8)).pack(anchor="w")

        self.botoes_nav = {}
        for chave, rotulo in [
            ("dashboard", "Dashboard"),
            ("revisar", "Revisar alterações"),
            ("limpeza", "Limpeza"),
            ("historico", "Histórico"),
            ("regras", "Regras"),
        ]:
            b = tk.Button(self.sidebar, text=rotulo, anchor="w",
                          bg=BG_PAINEL, fg=TEXTO_FRACO, bd=0, padx=18, pady=10,
                          font=FONTE_CORPO, cursor="hand2",
                          activebackground=BG_CARD, activeforeground=TEXTO,
                          command=lambda c=chave: self._navegar(c))
            b.pack(fill="x")
            self.botoes_nav[chave] = b

        rodape = tk.Frame(self.sidebar, bg=BG_PAINEL)
        rodape.pack(side="bottom", fill="x", padx=18, pady=16)
        self.lbl_pasta = tk.Label(rodape, text="Nenhuma pasta selecionada",
                                    bg=BG_PAINEL, fg=TEXTO_FRACO, font=("Segoe UI", 8),
                                    wraplength=170, justify="left")
        self.lbl_pasta.pack(anchor="w")

        self.conteudo = tk.Frame(self, bg=BG_APP)
        self.conteudo.pack(side="left", fill="both", expand=True)

    def _limpar_conteudo(self):
        for w in self.conteudo.winfo_children():
            w.destroy()

    def _navegar(self, chave):
        for k, b in self.botoes_nav.items():
            b.config(bg=BG_CARD if k == chave else BG_PAINEL,
                      fg=ROSA_AXOLOTL if k == chave else TEXTO_FRACO)
        {
            "dashboard": self._pagina_dashboard,
            "revisar": self._pagina_revisar,
            "limpeza": self._pagina_limpeza,
            "historico": self._pagina_historico,
            "regras": self._pagina_regras,
        }[chave]()

    def _cabecalho(self, titulo, subtitulo=""):
        cab = tk.Frame(self.conteudo, bg=BG_APP)
        cab.pack(fill="x", padx=32, pady=(28, 14))
        tk.Label(cab, text=titulo, bg=BG_APP, fg=TEXTO, font=FONTE_TITULO).pack(anchor="w")
        if subtitulo:
            tk.Label(cab, text=subtitulo, bg=BG_APP, fg=TEXTO_FRACO,
                      font=FONTE_SUB).pack(anchor="w", pady=(2, 0))
        return cab

    # ---------------------------------------------------------------- #
    # Ações
    # ---------------------------------------------------------------- #
    def escolher_pasta(self):
        pasta = filedialog.askdirectory(title="Escolha a pasta para o F.R.I.D.A.Y. organizar")
        if not pasta:
            return
        self.pasta_raiz = Path(pasta)
        self.engine = fc.Friday(self.pasta_raiz)
        self.lbl_pasta.config(text=f"📁 {self.pasta_raiz}", fg=TEXTO)
        self._escanear()

    def _escanear(self):
        if not self.engine:
            return
        self.plano, self.duplicados = self.engine.montar_plano()
        self.limpeza = self.engine.montar_plano_limpeza()
        self._navegar("dashboard")

    # ---------------------------------------------------------------- #
    # Dashboard
    # ---------------------------------------------------------------- #
    def _pagina_dashboard(self):
        self._limpar_conteudo()
        self._cabecalho("Boa tarde.", "Aqui está a visão geral do seu workspace.")

        barra = tk.Frame(self.conteudo, bg=BG_APP)
        barra.pack(fill="x", padx=32, pady=(0, 20))
        botao(barra, "ESCOLHER PASTA", self.escolher_pasta).pack(side="left")
        if self.engine:
            botao_secundario(barra, "REESCANEAR", self._escanear).pack(side="left", padx=(10, 0))
            botao_secundario(barra, "GERAR PLANILHA", self._gerar_planilha).pack(side="left", padx=(10, 0))
            botao(barra, "ORGANIZAR WORKSPACE", self._abrir_organizar,
                  cor=AGUA, cor_texto="#0a1a18").pack(side="right")

        if not self.engine:
            tk.Label(self.conteudo, text="Escolha uma pasta para o F.R.I.D.A.Y. analisar.\n"
                     "Nada é movido até você revisar e aprovar as mudanças.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO, justify="left")\
              .pack(anchor="w", padx=32, pady=10)
            return

        n_arquivos = len(self.plano)
        n_confirmar = sum(1 for i in self.plano if i.confianca < 0.75)
        n_dup = len(self.duplicados)
        n_limpeza = len(self.limpeza)
        n_ops = len(self.engine.historico())

        cards = tk.Frame(self.conteudo, bg=BG_APP)
        cards.pack(fill="x", padx=32)
        dados = [
            ("Itens prontos para organizar", str(n_arquivos), ROSA_AXOLOTL),
            ("Precisam da sua atenção", str(n_confirmar), AMARELO),
            ("Grupos de duplicados", str(n_dup), VERMELHO),
            ("Lixo + pastas vazias", str(n_limpeza), AGUA),
        ]
        for i, (titulo, valor, cor) in enumerate(dados):
            c = Cartao(cards, titulo, valor, cor=cor)
            c.grid(row=0, column=i, sticky="nsew", padx=(0, 12) if i < 3 else 0)
            cards.columnconfigure(i, weight=1)

        modo = self.engine.regras_mgr.regras["modo"]
        tk.Label(self.conteudo,
                 text=f"Modo atual: {modo}   ·   {n_ops} operação(ões) no histórico   ·   "
                      f"\"Understand first. Organize second. Delete never.\"",
                 bg=BG_APP, fg=TEXTO_FRACO, font=("Segoe UI", 9)).pack(anchor="w", padx=32, pady=(18, 0))

    def _gerar_planilha(self):
        caminho, formato = self.engine.gerar_planilha()
        aviso_formato = "" if formato == "xlsx" else \
            "\n\n(a biblioteca openpyxl não está instalada, então gerei um .csv — " \
            "abre normalmente no Excel/Google Sheets; rode \"pip install openpyxl\" " \
            "para gerar .xlsx de verdade da próxima vez)"
        messagebox.showinfo("F.R.I.D.A.Y.",
                             f"Planilha gerada com {len(self.engine.catalogo.listar())} item(ns):\n{caminho}"
                             + aviso_formato)

    def _abrir_organizar(self):
        self._navegar("revisar")

    # ---------------------------------------------------------------- #
    # Revisar alterações (preview mode)
    # ---------------------------------------------------------------- #
    def _pagina_revisar(self):
        self._limpar_conteudo()
        self._cabecalho("Revisar alterações",
                         "Selecione o que o F.R.I.D.A.Y. deve organizar agora. "
                         "Nada é movido sem sua confirmação.")

        if not self.engine or not self.plano:
            tk.Label(self.conteudo, text="Nada para organizar aqui. Escolha uma pasta no Dashboard.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO).pack(anchor="w", padx=32)
            return

        area = tk.Frame(self.conteudo, bg=BG_APP)
        area.pack(fill="both", expand=True, padx=32, pady=(0, 10))

        colunas = ("origem", "destino", "categoria", "tags", "confianca", "motivo")
        tree = ttk.Treeview(area, columns=colunas, show="headings", selectmode="extended")
        larguras = {"origem": 190, "destino": 230, "categoria": 130, "tags": 160,
                    "confianca": 80, "motivo": 220}
        titulos = {"origem": "Arquivo", "destino": "Novo local", "categoria": "Categoria",
                   "tags": "Tags", "confianca": "Confiança", "motivo": "Motivo"}
        for c in colunas:
            tree.heading(c, text=titulos[c])
            tree.column(c, width=larguras[c], anchor="w")

        for i, item in enumerate(self.plano):
            confianca_pct = f"{item.confianca * 100:.0f}%"
            tree.insert("", "end", iid=str(i), values=(
                item.origem.name, str(item.destino), item.categoria,
                ", ".join(item.tags), confianca_pct, item.motivo,
            ))
            if item.confianca < 0.5:
                tree.item(str(i), tags=("baixa",))
        tree.tag_configure("baixa", foreground=AMARELO)
        tree.selection_set([str(i) for i in range(len(self.plano))])  # tudo selecionado por padrão

        vsb = ttk.Scrollbar(area, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        rodape = tk.Frame(self.conteudo, bg=BG_APP)
        rodape.pack(fill="x", padx=32, pady=(8, 24))
        tk.Label(rodape, text=f"{len(self.plano)} item(ns) no plano  ·  "
                 f"amarelo = baixa confiança",
                 bg=BG_APP, fg=TEXTO_FRACO, font=("Segoe UI", 9),
                 wraplength=420, justify="left").pack(side="left")

        def organizar():
            selecionados = [int(i) for i in tree.selection()]
            if not selecionados:
                messagebox.showinfo("F.R.I.D.A.Y.", "Nenhum item selecionado.")
                return
            n = len(selecionados)
            if not messagebox.askyesno("Confirmar organização",
                    f"Mover {n} item(ns) para as novas pastas?\n\n"
                    "Você pode desfazer isso a qualquer momento em Histórico."):
                return
            registro, erros = self.engine.aplicar(self.plano, aprovados=set(selecionados))
            msg = f"{len(registro)} item(ns) organizados com sucesso."
            if erros:
                msg += f"\n\n{len(erros)} erro(s):\n" + "\n".join(f"- {n}: {e}" for n, e in erros)
            messagebox.showinfo("F.R.I.D.A.Y.", msg)
            self._escanear()

        botao(rodape, "ORGANIZAR SELECIONADOS", organizar, cor=AGUA,
              cor_texto="#0a1a18").pack(side="right")
        botao_secundario(rodape, "CANCELAR", lambda: self._navegar("dashboard")).pack(side="right", padx=(0, 10))

    # ---------------------------------------------------------------- #
    # Limpeza (pastas vazias + arquivos lixo)
    # ---------------------------------------------------------------- #
    def _pagina_limpeza(self):
        self._limpar_conteudo()
        self._cabecalho("Limpeza",
                         "Pastas vazias e arquivos de lixo do sistema (Thumbs.db, .tmp, etc.). "
                         "Nada é apagado: arquivos vão para _Lixeira e pastas vazias podem ser "
                         "recriadas a qualquer momento pelo Histórico.")

        if not self.engine:
            tk.Label(self.conteudo, text="Escolha uma pasta no Dashboard primeiro.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO).pack(anchor="w", padx=32)
            return

        if not self.limpeza:
            tk.Label(self.conteudo, text="Nada para limpar por aqui. Tudo certinho. ✓",
                     bg=BG_APP, fg=AGUA, font=FONTE_CORPO).pack(anchor="w", padx=32)
            return

        area = tk.Frame(self.conteudo, bg=BG_APP)
        area.pack(fill="both", expand=True, padx=32, pady=(0, 10))

        colunas = ("tipo", "caminho", "motivo", "tamanho")
        tree = ttk.Treeview(area, columns=colunas, show="headings", selectmode="extended")
        larguras = {"tipo": 120, "caminho": 420, "motivo": 260, "tamanho": 90}
        titulos = {"tipo": "Tipo", "caminho": "Local", "motivo": "Motivo", "tamanho": "Tamanho"}
        for c in colunas:
            tree.heading(c, text=titulos[c])
            tree.column(c, width=larguras[c], anchor="w")

        rotulo_tipo = {"arquivo_lixo": "Arquivo lixo", "pasta_vazia": "Pasta vazia"}
        for i, item in enumerate(self.limpeza):
            try:
                caminho_rel = item.caminho.relative_to(self.pasta_raiz)
            except ValueError:
                caminho_rel = item.caminho
            tree.insert("", "end", iid=str(i), values=(
                rotulo_tipo[item.tipo], str(caminho_rel), item.motivo,
                fc.tamanho_legivel(item.tamanho) if item.tamanho else "—",
            ))
        tree.selection_set([str(i) for i in range(len(self.limpeza))])

        vsb = ttk.Scrollbar(area, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        rodape = tk.Frame(self.conteudo, bg=BG_APP)
        rodape.pack(fill="x", padx=32, pady=(8, 24))
        n_arquivos = sum(1 for i in self.limpeza if i.tipo == "arquivo_lixo")
        n_pastas = sum(1 for i in self.limpeza if i.tipo == "pasta_vazia")
        tk.Label(rodape, text=f"{n_arquivos} arquivo(s) de lixo  ·  {n_pastas} pasta(s) vazia(s)",
                 bg=BG_APP, fg=TEXTO_FRACO, font=("Segoe UI", 9)).pack(side="left")

        def limpar():
            selecionados = [int(i) for i in tree.selection()]
            if not selecionados:
                messagebox.showinfo("F.R.I.D.A.Y.", "Nenhum item selecionado.")
                return
            itens = [self.limpeza[i] for i in selecionados]
            if not messagebox.askyesno("Confirmar limpeza",
                    f"Mover {sum(1 for i in itens if i.tipo == 'arquivo_lixo')} arquivo(s) lixo "
                    f"para _Lixeira e remover {sum(1 for i in itens if i.tipo == 'pasta_vazia')} "
                    f"pasta(s) vazia(s)?\n\nVocê pode desfazer isso em Histórico."):
                return
            registro, erros = self.engine.aplicar_limpeza(itens)
            msg = f"{len(registro)} item(ns) processados."
            if erros:
                msg += f"\n\n{len(erros)} erro(s):\n" + "\n".join(f"- {n}: {e}" for n, e in erros)
            messagebox.showinfo("F.R.I.D.A.Y.", msg)
            self._escanear()
            self._navegar("limpeza")

        botao(rodape, "LIMPAR SELECIONADOS", limpar, cor=AGUA,
              cor_texto="#0a1a18").pack(side="right")
        botao_secundario(rodape, "CANCELAR", lambda: self._navegar("dashboard")).pack(side="right", padx=(0, 10))

    # ---------------------------------------------------------------- #
    # Histórico
    # ---------------------------------------------------------------- #
    def _pagina_historico(self):
        self._limpar_conteudo()
        self._cabecalho("Histórico de operações", "Toda alteração pode ser desfeita, a qualquer momento.")

        if not self.engine:
            tk.Label(self.conteudo, text="Escolha uma pasta no Dashboard primeiro.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO).pack(anchor="w", padx=32)
            return

        historico = self.engine.historico()
        area = tk.Frame(self.conteudo, bg=BG_APP)
        area.pack(fill="both", expand=True, padx=32)

        if not historico:
            tk.Label(area, text="Nenhuma operação registrada ainda.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO).pack(anchor="w", pady=10)
            return

        for op in historico:
            linha = tk.Frame(area, bg=BG_CARD, highlightbackground=BORDA,
                              highlightthickness=1)
            linha.pack(fill="x", pady=6)
            info = tk.Frame(linha, bg=BG_CARD)
            info.pack(side="left", fill="x", expand=True, padx=16, pady=12)
            tk.Label(info, text=f"{len(op['itens'])} item(ns) organizados", bg=BG_CARD,
                      fg=TEXTO, font=("Segoe UI Semibold", 10)).pack(anchor="w")
            tk.Label(info, text=op["timestamp"].replace("T", "  ·  "), bg=BG_CARD,
                      fg=TEXTO_FRACO, font=("Segoe UI", 9)).pack(anchor="w")

            def fazer_desfazer(op_id=op["id"]):
                if not messagebox.askyesno("Desfazer", "Restaurar todos os arquivos desta operação "
                                            "para o local original?"):
                    return
                restaurados, erros = self.engine.desfazer(op_id)
                msg = f"{restaurados} item(ns) restaurados."
                if erros:
                    msg += f"\n\n{len(erros)} aviso(s):\n" + "\n".join(f"- {n}: {e}" for n, e in erros)
                messagebox.showinfo("F.R.I.D.A.Y.", msg)
                self._escanear()
                self._navegar("historico")

            botao_secundario(linha, "DESFAZER", fazer_desfazer).pack(side="right", padx=16, pady=12)

    # ---------------------------------------------------------------- #
    # Regras / Configurações
    # ---------------------------------------------------------------- #
    def _pagina_regras(self):
        self._limpar_conteudo()
        self._cabecalho("Regras", "O F.R.I.D.A.Y. prioriza suas regras manuais sobre as decisões automáticas.")

        if not self.engine:
            tk.Label(self.conteudo, text="Escolha uma pasta no Dashboard primeiro.",
                     bg=BG_APP, fg=TEXTO_FRACO, font=FONTE_CORPO).pack(anchor="w", padx=32)
            return

        regras = self.engine.regras_mgr.regras
        area = tk.Frame(self.conteudo, bg=BG_APP)
        area.pack(fill="both", expand=True, padx=32, pady=(0, 20))

        # --- Modo --- #
        bloco_modo = tk.Frame(area, bg=BG_CARD, highlightbackground=BORDA, highlightthickness=1)
        bloco_modo.pack(fill="x", pady=(0, 14))
        tk.Label(bloco_modo, text="Modo de organização", bg=BG_CARD, fg=TEXTO,
                  font=("Segoe UI Semibold", 11)).pack(anchor="w", padx=16, pady=(14, 4))
        var_modo = tk.StringVar(value=regras["modo"])
        descricoes = {
            "SAFE": "Máxima confirmação — toda alteração precisa da sua aprovação.",
            "SMART": "Organiza automaticamente o que tem alta confiança; pergunta no resto.",
            "AUTO": "Aplica regras já aprovadas automaticamente, sem perguntar.",
        }
        for modo in ("SAFE", "SMART", "AUTO"):
            f = tk.Frame(bloco_modo, bg=BG_CARD)
            f.pack(anchor="w", padx=16, pady=2, fill="x")
            ttk.Radiobutton(f, text=modo, value=modo, variable=var_modo).pack(side="left")
            tk.Label(f, text=descricoes[modo], bg=BG_CARD, fg=TEXTO_FRACO,
                      font=("Segoe UI", 9)).pack(side="left", padx=(8, 0))

        def salvar_modo(*_):
            regras["modo"] = var_modo.get()
            self.engine.regras_mgr.salvar()
        var_modo.trace_add("write", salvar_modo)
        tk.Frame(bloco_modo, bg=BG_CARD, height=10).pack()

        # --- Pastas protegidas --- #
        bloco_prot = tk.Frame(area, bg=BG_CARD, highlightbackground=BORDA, highlightthickness=1)
        bloco_prot.pack(fill="x", pady=(0, 14))
        tk.Label(bloco_prot, text="Pastas nunca organizadas automaticamente", bg=BG_CARD,
                  fg=TEXTO, font=("Segoe UI Semibold", 11)).pack(anchor="w", padx=16, pady=(14, 6))
        lista_prot = tk.Listbox(bloco_prot, bg=BG_PAINEL, fg=TEXTO, bd=0, height=4,
                                  selectbackground="#2a3a44", font=FONTE_MONO,
                                  highlightthickness=0)
        for p in regras["pastas_protegidas"]:
            lista_prot.insert("end", p)
        lista_prot.pack(fill="x", padx=16)

        linha_add = tk.Frame(bloco_prot, bg=BG_CARD)
        linha_add.pack(fill="x", padx=16, pady=12)
        entrada_prot = tk.Entry(linha_add, bg=BG_PAINEL, fg=TEXTO, insertbackground=TEXTO,
                                  bd=0, font=FONTE_CORPO)
        entrada_prot.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        def add_protegida():
            nome = entrada_prot.get().strip()
            if not nome:
                return
            regras["pastas_protegidas"].append(nome)
            self.engine.regras_mgr.salvar()
            lista_prot.insert("end", nome)
            entrada_prot.delete(0, "end")

        botao_secundario(linha_add, "ADICIONAR", add_protegida).pack(side="left")

        # --- Regra personalizada --- #
        bloco_regra = tk.Frame(area, bg=BG_CARD, highlightbackground=BORDA, highlightthickness=1)
        bloco_regra.pack(fill="x")
        tk.Label(bloco_regra, text="Nova regra — ex: \"deadlock\" → VIDEOS/GAMES/Deadlock/Clips",
                  bg=BG_CARD, fg=TEXTO, font=("Segoe UI Semibold", 11)).pack(anchor="w", padx=16, pady=(14, 8))
        linha_regra = tk.Frame(bloco_regra, bg=BG_CARD)
        linha_regra.pack(fill="x", padx=16, pady=(0, 16))
        e_chave = tk.Entry(linha_regra, bg=BG_PAINEL, fg=TEXTO, insertbackground=TEXTO,
                             bd=0, font=FONTE_CORPO, width=20)
        e_chave.insert(0, "palavra-chave")
        e_chave.pack(side="left", ipady=6, padx=(0, 8))
        e_destino = tk.Entry(linha_regra, bg=BG_PAINEL, fg=TEXTO, insertbackground=TEXTO,
                               bd=0, font=FONTE_CORPO)
        e_destino.insert(0, "PROJECTS/EDITING/Meu Projeto")
        e_destino.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        def add_regra():
            chave, destino = e_chave.get().strip(), e_destino.get().strip()
            if not chave or not destino:
                return
            self.engine.regras_mgr.adicionar_regra_personalizada(chave, destino)
            messagebox.showinfo("F.R.I.D.A.Y.", f"Regra adicionada: \"{chave}\" → {destino}")
            e_chave.delete(0, "end")
            e_destino.delete(0, "end")

        botao(bloco_regra, "SALVAR REGRA", add_regra).pack(anchor="e", padx=16, pady=(0, 16))


def main():
    app = FridayApp()
    app.mainloop()


if __name__ == "__main__":
    main()
