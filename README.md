# F.R.I.D.A.Y. — by Axolotl BR

**File Retrieval, Indexing, Directory & Archiving Y-system**

o F.R.I.D.A.Y. é um organizador de arquivos pra windows que usa regras e automações pra tentar deixar seu pc menos bagunçado.

a ideia é organizar arquivos, pastas, vídeos, clipes e projetos sem sair movendo coisa aleatoriamente.

tudo roda localmente. nada dos seus arquivos é enviado pra internet.

> *understand first. organize second. delete never.*

---

## como rodar

você só precisa de **python 3.9+**.

não precisa instalar um monte de pacote. a interface usa `tkinter`.

```bash
python friday_gui.py
```

depois é só abrir o programa, clicar em **ESCOLHER PASTA** e selecionar a pasta que você quer organizar.

se estiver usando pela primeira vez, começa pelo modo **SAFE**.

---

## o que ele faz

### arquivos

o F.R.I.D.A.Y. consegue separar arquivos por tipo:

* documentos
* planilhas
* apresentações
* PDFs
* imagens
* vídeos
* música
* compactados
* programas
* código

---

### vídeos e jogos

vídeos de jogos têm uma organização própria.

o F.R.I.D.A.Y. tenta descobrir qual jogo é pelo nome do arquivo ou da pasta e também tenta identificar o tipo do vídeo.

por exemplo:

```text
VIDEOS/
└── GAMES/
    └── CS2/
        ├── Clips/
        ├── Highlights/
        ├── Gameplay/
        └── Recordings/
```

se quiser, também dá pra adicionar seus próprios jogos e palavras-chave nas **Regras**.

---

### projetos

projetos são tratados de um jeito diferente.

se o F.R.I.D.A.Y. encontrar coisas como:

```text
.git
package.json
requirements.txt
.prproj
.aep
```

ele entende que provavelmente aquilo é um projeto e move a pasta inteira.

```text
PROJECTS/
├── CODE/
│   └── MeuProjeto/
│
└── EDITING/
    └── MeuVideo/
```

ele não reorganiza os arquivos de dentro do projeto.

isso evita quebrar estrutura, dependências ou qualquer outra coisa importante.

---

### duplicados

também existe um sistema pra encontrar arquivos duplicados.

em vez de olhar só o nome, o F.R.I.D.A.Y. usa **hash do conteúdo** pra saber se dois arquivos são realmente iguais.

os duplicados vão pra:

```text
_Duplicados/
```

o original continua onde estava.

**nada é apagado.**

---

## antes de organizar

não precisa confiar cegamente no programa.

o modo de revisão mostra o que ele pretende fazer antes de aplicar qualquer mudança:

* qual arquivo vai ser movido
* pra onde
* nível de confiança
* motivo da classificação

você escolhe o que quer aprovar.

---

## histórico

toda mudança feita pelo F.R.I.D.A.Y. fica registrada.

se alguma coisa for parar no lugar errado:

```text
Histórico → DESFAZER
```

o arquivo volta pro lugar exato de onde veio.

---

## regras personalizadas

também dá pra criar suas próprias regras.

por exemplo:

```text
"meuprojeto" → PROJECTS/CODE/MeuProjeto
```

essas regras têm prioridade sobre a classificação automática.

---

## modos

existem três modos:

**SAFE**
mais conservador. bom pra começar e revisar tudo.

**SMART**
deixa o F.R.I.D.A.Y. tomar mais decisões sozinho.

**AUTO**
focado em automatizar o máximo possível.

---

## pastas protegidas

você pode escolher pastas que o F.R.I.D.A.Y. nunca deve mexer.

algumas já ficam protegidas por padrão:

```text
Downloads
node_modules
.git
AppData
```

---

## estrutura

depois de organizar, a pasta pode ficar assim:

```text
SUA_PASTA/
├── Documentos/
├── Planilhas/
├── PDFs/
├── Imagens/
├── Musica/
├── Compactados/
├── Programas/
├── Codigo/
│
├── VIDEOS/
│   └── GAMES/
│       └── <Jogo>/
│           ├── Clips/
│           ├── Highlights/
│           ├── Gameplay/
│           └── Recordings/
│
├── PROJECTS/
│   ├── CODE/
│   └── EDITING/
│
├── UNSORTED/
├── _Duplicados/
└── .friday/
```

`UNSORTED` é onde ficam as coisas que o F.R.I.D.A.Y. não conseguiu identificar direito.

`.friday` guarda os arquivos internos do programa, como histórico e regras.

---

## o que ainda falta

o projeto ainda está no começo e tem bastante coisa que pode entrar depois.

algumas ideias:

* análise de metadados de vídeo
* identificação melhor de jogos
* aprendizado com as correções do usuário
* busca usando linguagem natural
* classificação usando IA
* mais automações
* uma interface melhor
* integração maior com a identidade da Axolotl BR

a estrutura atual já foi feita pensando nisso.

o sistema de classificação fica principalmente no `classificar_arquivo()`, então dá pra adicionar novas formas de identificar arquivos sem precisar refazer tudo.

---

## arquivos

```text
friday_core.py
```

é o motor do F.R.I.D.A.Y.

cuida da classificação, projetos, duplicados, aplicação das mudanças, histórico e undo.

```text
friday_gui.py
```

é a interface gráfica.

dashboard, revisão, histórico e regras.

---

## axolotl BR

o F.R.I.D.A.Y. é um dos projetos da **Axolotl BR**.

a ideia é fazer uma ferramenta que realmente seja útil pra quem tem um pc cheio de projetos, jogos, clipes, vídeos, código e um monte de arquivo espalhado.

sem complicar.

sem mandar seus arquivos pra algum servidor.

e principalmente:

**sem apagar suas coisas.**

---

*f.r.i.d.a.y. — understand first. organize second. delete never.*

**axolotl BR — player pra player.**
