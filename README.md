# SkyrimNet PT-BR

**Pacote de conteúdo (mod) em português brasileiro para o SkyrimNet.**

Este projeto traduz o conteúdo do SkyrimNet para PT-BR e o entrega como uma
camada externa (`external/<id>/`), sem alterar a pasta base do mod. Funciona
como um mod separado no MO2 e também pode ser publicado no catálogo de plugins
do SkyrimNet.

## O que já está traduzido

- **Fala dos NPCs em PT-BR**: diretiva de idioma em `dialogue_response.prompt` e
  `player_dialogue.prompt`.
- **58 bios**: Whiterun, Riverwood, Solitude, Windhelm, Riften e Markarth.

O restante está em tradução. O pacote é incremental: cada lote entra como um
commit e um release. O benchmark local com Qwen2.5-3B está em
`benchmarks/REVIEW.md`.

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
