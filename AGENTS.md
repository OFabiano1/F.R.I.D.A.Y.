# AGENTS — F.R.I.D.A.Y. (organizador desktop local)

## Marca (resumo MASTER UNIVERSE)

- Parte do ecossistema **AXOLOTL BR — De player para player**. Tom produto: claro, moderno, objetivo. Sem corporativês.
- F.R.I.D.A.Y. tem identidade própria de ferramenta (`File Retrieval, Indexing, Directory & Archiving Y-system`), mas mantém ligação com Axolotl BR. Não criar submarcas que competem com a principal.
- Nunca fingir IA/extração que não existe. O que for roadmap (`ffprobe`, busca NL, aprendizado) fica fora do código até existir.

## Filosofia inegociável

- `Understand first. Organize second. Delete never.` Sempre preview em Revisar/Limpeza antes de mover. Toda operação com DESFAZER no Histórico. Lixo vai para `_Lixeira/`, nunca `unlink`. Pastas vazias removidas devem ser recriáveis pelo undo.

## Stack / run

- Python 3.9+, só stdlib `tkinter` para GUI. `python friday_gui.py`.
- Opcional `pip install openpyxl` para `.xlsx` real (formatado); sem isso cai para `.csv`.
- Motor sem GUI: `friday_core.py`. Ponto de extensão: `classificar_arquivo` — plugar novas regras ali, não na GUI.

## Estrutura / regras

- `friday_gui.py` = Dashboard, Revisar, Limpeza, Histórico, Regras. `friday_core.py` = classificação, projetos, catálogo (`FRD-xxxxx` + tags), duplicados por hash (mantém o mais antigo), limpeza, planilha, undo.
- Saída: `Documentos/ Planilhas/ PDFs/ Imagens/ Musica/ VIDEOS/GAMES/<Jogo>/ PROJECTS/{CODE,EDITING}/ UNSORTED/ _Duplicados/ _Lixeira/` + interno `.friday/` (`friday_regras.json`, `catalogo.json`, `operacao_*.json`). Nunca mexer em `.friday/` manualmente nem tocar em pastas protegidas (`Downloads`, `node_modules`, `.git`, `AppData` por padrão).
- Projetos detectados por `.git`/`package.json`/`requirements.txt`/`.prproj`/`.aep` movem inteiros sem mexer dentro. Regras custom > classificação automática. Modo default SAFE.
