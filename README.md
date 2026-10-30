# SkyrimNet PT-BR

**Pacote de conteúdo (mod) em português brasileiro para o SkyrimNet.**

Este projeto traduz o conteúdo do SkyrimNet para PT-BR e o entrega como uma
camada externa (`external/<id>/`), sem alterar a pasta base do mod. Funciona
como um mod separado no MO2 e também pode ser publicado no catálogo de plugins
do SkyrimNet.

## O que já está traduzido

- **Núcleo dos prompts**: `system_head` (8), `user_final_instructions` (11),
  `dialogue_response` e `player_dialogue`, com a instrução de idioma no system
  e no fim da mensagem do usuário.
- **154 bios**: Whiterun, Riverwood, Solitude, Windhelm, Riften, Markarth e
  NPCs nomeados de outras regiões.
- **Interface web**: 2.932 chaves em PT-BR (nav, common, home, settings
  completos, TTS, LLM, logs, chat, plugins e personagens), com fallback para
  inglês nas demais.

O restante está em tradução. O pacote é incremental: cada lote entra como um
commit e um release. O benchmark local com Qwen2.5-3B está em
`benchmarks/REVIEW.md`.

## Interface web

O zip inclui o patch de UI em `SKSE/Plugins/SkyrimNet/assets/web-new/`
(`main.<hash>.js`, `index.html`, `pt-br.js`). O build é feito a partir do
bundle instalado do SkyrimNet:

```powershell
python ui/build_ui.py --source "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\assets\web-new"
```

Veja `ui/README.md` para cobertura, fallback e atualização após updates do
SkyrimNet.

## Modelo de LLM recomendado

Este pacote traduz o conteúdo, mas **não controla o modelo**. Com modelos
pequenos (3B), o prompt do SkyrimNet é dominado por inglês e o modelo pode
ignorar a diretiva de PT-BR. Use **7B–14B** (Qwen2.5-7B/14B-Instruct, Gemma 2
9B, Llama 3.1 8B) para diálogo em português com aderência consistente.

## Instalação

### Mod Organizer 2 (recomendado)

1. Instale o **SkyrimNet** normalmente como um mod.
2. Baixe o zip em **Releases** e instale como um **mod separado** no MO2.
3. Deixe **SkyrimNet PT-BR** abaixo do SkyrimNet no painel esquerdo
   (prioridade maior).
4. Ative e inicie o jogo.

O zip instala apenas:

```
SKSE/Plugins/SkyrimNet/external/julianu37.skyrimnet-ptbr/
```

### Catálogo de plugins do SkyrimNet

O conteúdo do pacote é o próprio plugin: `manifest.json` + `prompts/`. Para
publicar, copie a pasta `dist/marketplace/plugins/julianu37/skyrimnet-ptbr/`
para o repositório `MinLL/SkyrimNet-Plugins` (ou use a página Publish do
dashboard).

## Requisitos

- SkyrimNet 0.25.0 ou superior (beta27/beta28 testados)
- Para voz PT-BR: [skyrimnet-kokoro-ptbr](https://github.com/julianu37/skyrimnet-kokoro-ptbr)
  (engine XTTS em `http://127.0.0.1:8020`)

## Build

```powershell
python tools/package.py
```

Gera:

- `dist/SkyrimNet-PT-BR-<versão>.zip` — instalação no MO2
- `dist/marketplace/plugins/julianu37/skyrimnet-ptbr/` — pacote para o catálogo

## Estrutura

```
skyrimnet-ptbr/
├── manifest.json          # identidade do plugin (id = julianu37.skyrimnet-ptbr)
├── prompts/               # conteúdo traduzido (mesmos caminhos da base)
├── glossary/ptbr.yaml     # glossário e estilo
├── tools/validate_prompts.py
├── tools/package.py
├── docs/plano-traducao.md
├── LICENSE                # MIT para a tradução/ferramentas
├── LICENSES/              # licença do SkyrimNet (conteúdo base)
└── NOTICE.md              # atribuição e termos
```

## Licença e atribuição

A tradução e as ferramentas são MIT. O conteúdo base traduzido pertence a
**Fateless.Ai** e é usado conforme a seção 3 (Content packs) da licença do
SkyrimNet. Leia `NOTICE.md` e `LICENSES/` antes de redistribuir.

The Elder Scrolls V: Skyrim é marca da Bethesda Softworks/ZeniMax. Este projeto
é não oficial e não afiliado.
