# Organizador de Arquivos Inteligente — versão para o seu PC

Um script Python que organiza uma pasta real do seu computador: identifica os
arquivos por tipo, separa em subpastas, encontra duplicados e nunca apaga nada
sem sua confirmação.

## Requisitos

- Python 3.8 ou mais recente (já vem instalado no macOS e na maioria das
  distribuições Linux; no Windows, baixe em https://python.org).
- Nenhuma biblioteca extra é necessária.

## Como usar

1. Baixe o arquivo `organizador.py` para o seu computador.
2. Abra o Terminal (macOS/Linux) ou PowerShell/CMD (Windows).
3. Rode uma simulação primeiro — **isto não move nenhum arquivo**, só mostra
   o que seria feito:

   ```bash
   python3 organizador.py "/caminho/da/sua/pasta"
   ```

   Exemplo real:
   ```bash
   python3 organizador.py "C:/Users/SeuNome/Downloads"
   ```

4. Se o plano parecer correto, aplique de verdade:

   ```bash
   python3 organizador.py "/caminho/da/sua/pasta" --aplicar
   ```

   O script vai pedir para você digitar `SIM` antes de mover qualquer coisa.

## Outros comandos

| Comando | O que faz |
|---|---|
| `--duplicados` | Só lista os arquivos duplicados encontrados, sem mover nada |
| `--renomear` | Além de organizar, sugere/renomeia arquivos com nomes genéricos (`IMG_1234.jpg`, `Screenshot...`) |
| `--desfazer` | Desfaz a última organização aplicada nessa pasta, restaurando tudo ao lugar original |
| `-y` | Aplica sem pedir confirmação (use com cuidado, ex: em automações) |

Exemplo combinando opções:
```bash
python3 organizador.py "/caminho/da/pasta" --aplicar --renomear
```

## Como funciona a segurança

- **Nunca exclui arquivos.** Duplicados são movidos para uma subpasta
  `_Duplicados` dentro da própria pasta analisada, para você decidir o que
  fazer com eles.
- **Sempre em modo simulação por padrão.** Só move algo se você usar
  `--aplicar`.
- **Registro de tudo.** Cada vez que o script aplica mudanças, ele salva um
  log em `.organizador_logs/` dentro da pasta organizada — é esse log que
  permite o `--desfazer`.
- **Sem sobrescrever nada.** Se já existir um arquivo com o mesmo nome no
  destino, o script acrescenta `(1)`, `(2)`, etc.
- **100% local.** Nada é enviado para a internet; toda a análise roda no seu
  computador.

## Categorias criadas

Documentos, Planilhas, Apresentações, PDFs, Imagens, Vídeos, Música,
Compactados, Programas, Código e Outros (para o que não se encaixa em
nenhuma extensão conhecida). Você pode editar a lista de extensões de cada
categoria abrindo `organizador.py` e alterando o dicionário `CATEGORIAS` no
topo do arquivo.

## Limitações desta versão

- Organiza apenas o primeiro nível da pasta (não entra em subpastas), para
  evitar reorganizar coisas que você já separou manualmente.
- É uma ferramenta de linha de comando, sem interface gráfica — pensada para
  ser simples, transparente e fácil de auditar (você pode ler o código
  inteiro em poucos minutos).
- Se quiser uma versão com janelas e botões (interface gráfica de verdade,
  tipo um app instalável), dá para evoluir este script com bibliotecas como
  `tkinter` (vem com o Python) ou empacotar como app desktop — é só pedir.
