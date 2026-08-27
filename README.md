# F.R.I.D.A.Y. — by Axolotl BR

Ferramenta desktop de organização inteligente de arquivos, pastas, vídeos e
projetos de trabalho. Roda 100% local — nada é enviado para a internet. 
*Understand first. Organize second. Delete never.*

## Como rodar daleeee 

Precisa apenas de Python 3.9+ (windows já vem com ele, ou baixe em
python.org). não precisa instalar nenhum pacote extra — a interface usa só
a biblioteca padrão (`tkinter`).

```bash
python friday_gui.py
```

Isso abre a janela do F.R.I.D.A.Y. Clique em **ESCOLHER PASTA** e selecione
a pasta que você quer organizar (por exemplo, sua pasta de Downloads, ou
uma pasta de projetos).

## O que ele faz hoje

- **Categoriza arquivos soltos** por extensão: Documentos, Planilhas,
  Apresentações, PDFs, Imagens, Vídeos, Música, Compactados, Programas,
  Código.
- **Identifica vídeos de jogos** pelo nome do arquivo/pasta (ex.: um
  arquivo com "CS2" ou "Deadlock" no nome vai para
  `VIDEOS/GAMES/<Jogo>/<Tipo>`, com o tipo — Clips, Highlights, Gameplay,
  Recordings — também detectado por palavras-chave). Você pode adicionar
  seus próprios jogos na tela **Regras**.
- **Protege projetos de código e de edição**: pastas com `.git`,
  `package.json`, `requirements.txt`, arquivos `.prproj`/`.aep` etc. são
  reconhecidas como projetos e movidas inteiras para
  `PROJECTS/CODE/...` ou `PROJECTS/EDITING/...` — o conteúdo interno nunca
  é reorganizado, então nenhum projeto quebra.
- **Detecta duplicados de verdade** (por hash do conteúdo, não só nome) e
  os move para `_Duplicados/`, mantendo o mais antigo no lugar. Nada é
  apagado.
- **Modo Preview** (tela "Revisar alterações"): mostra exatamente o que
  seria movido, para onde, com que confiança e por quê, antes de qualquer
  coisa acontecer. Você escolhe quais itens aprovar.
- **Reversível 100%**: toda operação aplicada fica registrada na tela
  **Histórico**, com um botão **DESFAZER** que devolve os arquivos para o
  lugar exato de onde vieram.
- **Regras personalizadas**: em **Regras** você pode dizer, por exemplo,
  que arquivos com "meuprojeto" no nome sempre vão para uma pasta
  específica — essas regras têm prioridade sobre a classificação
  automática.
- **Três modos** (SAFE / SMART / AUTO) — hoje o modo é salvo e usado para
  guiar o quanto o F.R.I.D.A.Y. deveria confiar nas próprias decisões;
  o modo SAFE é o mais indicado para começar, revisando tudo manualmente.
- **Pastas protegidas**: você define pastas que o F.R.I.D.A.Y. nunca deve
  tocar (por padrão: `Downloads`, `node_modules`, `.git`, `AppData`).

## Estrutura de pastas criada

```
SUA_PASTA/
├── Documentos/
├── Planilhas/
├── PDFs/
├── Imagens/
├── Musica/
├── Compactados/
├── Programas/
├── Codigo/
├── VIDEOS/
│   └── GAMES/
│       └── <Jogo>/
│           ├── Clips/
│           ├── Highlights/
│           ├── Gameplay/
│           └── Recordings/
├── PROJECTS/
│   ├── CODE/<nome do projeto>/
│   └── EDITING/<nome do projeto>/
├── UNSORTED/           ← itens de baixa confiança, para você revisar
├── _Duplicados/
└── .friday/             ← logs internos (histórico + regras), não mexa aqui
```

## O que ainda não está implementado (próximos passos naturais)

O pedido original também descrevia coisas mais avançadas — leitura de
metadados de vídeo, análise de conteúdo, aprendizado contínuo a partir de
correções do usuário na interface, busca em linguagem natural, e uma
identidade visual mais elaborada da Axolotl BR. A base atual (`friday_core.py`)
já foi pensada para isso: o motor de classificação é uma função só
(`classificar_arquivo`), então dá para plugar ali, por exemplo, extração de
metadados de vídeo com `ffprobe`, ou trocar as regras por palavra-chave por
uma chamada a um modelo de IA. Posso construir qualquer uma dessas partes
a seguir — é só dizer qual você quer primeiro.

## Arquivos

- `friday_core.py` — todo o motor: classificação, projetos, duplicados,
  aplicação de mudanças, histórico e undo. Pode ser usado sozinho, sem a
  interface, se você quiser automatizar por script.
- `friday_gui.py` — a interface gráfica (dashboard, revisar, histórico,
  regras).
