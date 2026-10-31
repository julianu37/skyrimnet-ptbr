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
- **1.632 prompts (100%)**: 1.509 bios + 123 prompts de sistema.
- **Interface web (100%)**: **7.785 de 7.785 chaves** — 6.753 do bundle web +
  1.032 específicas do dashboard in-game (PrismaUI).
- **YAML (100%)**: 35 registros — filtros, efeitos de voz, Dialogue Actions e
  móveis, além dos `carry_tags` via patch local.
- **ESP (100%)**: 9 textos visíveis via `tools/patch_esp.py`.
- **ESP**: descrições de feitiços e mensagens do plugin traduzidas via
  `tools/patch_esp.py` (patch local, com backup).

A tradução está **completa**. O pacote é versionado e pode ser reconstruído a
partir dos scripts. O benchmark local com Qwen2.5-3B está em
`benchmarks/REVIEW.md`.

## Interface web

O dashboard existe em dois bundles e o zip cobre os dois:

- **Dashboard in-game (PrismaUI)**: `PrismaUI/views/SkyrimNet/dashboard/`
  (`dashboard.<hash>.js`, `index.html`, `pt-br.js`).
- **Dashboard web**: `SKSE/Plugins/SkyrimNet/assets/web-new/`
  (`main.<hash>.ptbr.js`, `index.html`, `pt-br.js`).

Builds:

```powershell
python ui/build_prisma.py --source "C:\...\mods\skyrimnet\PrismaUI\views\SkyrimNet\dashboard"
python ui/build_ui.py --source "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\assets\web-new"
```

O dashboard in-game lê `PrismaUI/views/...`; o patch antigo só em
`assets/web-new` não era carregado dentro do jogo. Veja `ui/README.md`.

## Modelo de LLM recomendado

O pacote traduz o conteúdo, mas **não controla o modelo**. **Recomendação
atual: Qwen2.5-7B-Instruct com 16.384 tokens de contexto.** O 3B responde em
PT-BR em conversas novas, mas em saves antigos ele tende a imitar as falas
 anteriores do histórico que estão em inglês; o 7B segue a diretiva mesmo com
esse histórico.

No `OpenRouter.yaml`, use `model_name: qwen2.5-7b-instruct` e mantenha o
servidor LM Studio com o modelo carregado em 16.384 tokens. **Com 8.192 o
prompt completo (~10.800 tokens) falha com HTTP 400 e nenhuma fala é gerada.**

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
python tools/validate_prompts.py --source "...\skyrimnet.base\prompts" --translated prompts --allow-subset `
  --allow-structural components/context/component_npc_state_summary.prompt submodules/character_bio/0050_physical_activity.prompt
python tools/check_ui.py
python tools/package.py

# validação oficial (dev kit beta28)
content-validate.exe dist\marketplace\plugins\julianu37\skyrimnet-ptbr `
  --base-tree "...\library\skyrimnet.base" --report dist\validate-report.json
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
