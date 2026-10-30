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
- **421 prompts**: 298 bios (Whiterun, Riverwood, Solitude, Windhelm, Riften,
  Markarth e NPCs nomeados de outras regiões) + 123 prompts de sistema
  (100% do sistema).
- **Interface web**: **6.753 de 6.753 chaves (100%)** — nav, common, home,
  settings completos, TTS, LLM, logs, chat, plugins, personagens, gamedata,
  prompts, actions, triggers, routing, tutorial, world knowledge, debug e
  demais telas.
- **YAML de conteúdo**: filtros, efeitos de voz e regras de Dialogue Actions
  (16 registros).
- **ESP**: descrições de feitiços e mensagens do plugin traduzidas via
  `tools/patch_esp.py` (patch local, com backup).

A UI, os prompts de sistema, os YAML de conteúdo e os textos do ESP estão
completos. O restante em tradução são as bios de personagens. O pacote é
incremental: cada lote entra como um commit e um release. O benchmark local com
Qwen2.5-3B está em `benchmarks/REVIEW.md`.

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

O pacote traduz o conteúdo, mas **não controla o modelo**. Com o núcleo de
prompts traduzido, o Qwen2.5-3B-Instruct já responde em PT-BR de forma
consistente no teste local. Modelos **7B–14B** (Qwen2.5-7B/14B-Instruct,
Gemma 2 9B, Llama 3.1 8B) tendem a dar mais qualidade, aderência e tolerância a
contextos longos. O benchmark está em `benchmarks/REVIEW.md`.

## Instalação

### Mod Organizer 2 (recomendado)

1. Instale o **SkyrimNet** normalmente como um mod.
2. Baixe o zip em **Releases** e instale como um **mod separado** no MO2.
3. Deixe **SkyrimNet PT-BR** **abaixo** do SkyrimNet no painel esquerdo
   (prioridade maior), para que o patch de UI do pacote vença.
4. Ative e inicie o jogo.
5. Opcional: feche o jogo e rode `tools\patch_esp.py` apontando para o
   `SkyrimNet.esp` instalado, para traduzir as mensagens e descrições de
   feitiços que ficam dentro do ESP. Veja `docs/esp.md`.

O zip instala:

```
SKSE/Plugins/SkyrimNet/external/julianu37.skyrimnet-ptbr/
SKSE/Plugins/SkyrimNet/assets/web-new/    (patch de UI)
tools/patch_esp.py                        (opcional)
docs/esp.md
```

### Catálogo de plugins do SkyrimNet

O conteúdo do pacote é o próprio plugin: `manifest.json` + `prompts/` +
`filters/` + `voice_effects/` + `dialogue_actions/`. Para publicar, copie a
pasta `dist/marketplace/plugins/julianu37/skyrimnet-ptbr/` para o repositório
`MinLL/SkyrimNet-Plugins` (ou use a página Publish do dashboard).

O catálogo instala apenas conteúdo da Content Library (prompts, bios, filtros,
efeitos de voz e regras). O **patch de UI** e o **patch do ESP** só vêm no zip
do MO2, porque não são arquivos de plugin.

## Requisitos

- SkyrimNet 0.25.0 ou superior (beta27/beta28 testados)
- Para voz PT-BR: [skyrimnet-kokoro-ptbr](https://github.com/julianu37/skyrimnet-kokoro-ptbr)
  (engine XTTS em `http://127.0.0.1:8020`)

## Build

```powershell
python tools/validate_prompts.py --source "...\skyrimnet.base\prompts" --translated prompts --allow-subset
python tools/check_ui.py
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
├── filters/               # listas de atores/memórias traduzidas
├── voice_effects/          # nomes dos efeitos de voz
├── dialogue_actions/       # listas de Dialogue Actions
├── glossary/ptbr.yaml     # glossário e estilo
├── tools/validate_prompts.py
├── tools/patch_esp.py
├── tools/package.py
├── docs/plano-traducao.md
├── docs/esp.md
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
