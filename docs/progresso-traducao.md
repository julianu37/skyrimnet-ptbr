# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura final

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | **1632** | 1632 | **100%** |
| Bios de personagens | **1509** | 1509 | **100%** |
| Prompts de sistema (não-bios) | **123** | 123 | **100%** |
| Interface web (chaves) | **6753** | 6753 | **100%** |
| YAML de conteúdo | **35** | 35 | **100%** |
| ESP (textos visíveis) | **9** | 9 | **100%** |
| MCM/Papyrus | n/a | n/a | — |

## Como foi feito

- Tradução em lotes de 12–24 arquivos com subagentes, sempre comparando
  estrutura Jinja, bullets, numeração, linhas em branco e markers.
- Validação determinística em todo lote (`tools/validate_prompts.py`).
- Normalização final de BOM/CRLF, newline e terminologia.
- UI extraída do bundle instalado (`main.027620d9.js`), 6.753 chaves
  traduzidas e injetadas como locale `pt-br`.
- YAML da Content Library: filtros (6), efeitos de voz (8), Dialogue Actions
  (2) e móveis (4). Os 11 `config/carry_tags_*` e os 4 arquivos sem prosa
  completam os 35.
- ESP: `tools/patch_esp.py` traduz 9 textos player-facing preservando o
  tamanho dos registros.
- `config/carry_tags_*`: `tools/patch_config.py` (patch local, backup).

## Revisões e normalizações

- `dunmer`, `housecarl`, `Forsworn`, `The Reach`, `Companions`, `Jarl`,
  `Thane` mantidos conforme glossário.
- `GameMaster` → **Mestre de Jogo** nos prompts e na UI.
- `Colégio de Bardos`, `Forte`, `Mina`, `Caverna`, `Fazenda`, `O Gourmet`,
  `Paladar Incomum`.
- `Mar dos Fantasmas`, `All-Maker`, `Sacerdote Mariposa`,
  `Pergaminho Ancestral`, `Briarheart`, `skeever`, `Parente de Sangue`.
- `furniture` traduzido com suporte a `Carruagem`/`Balcão` na lógica dos
  prompts.

## Ferramentas

- `tools/validate_prompts.py` — valida 1.632 prompts.
- `tools/check_ui.py` — valida 6.753 chaves e placeholders.
- `tools/package.py` — zip MO2 + pacote do catálogo.
- `tools/patch_esp.py` — textos do ESP.
- `tools/patch_config.py` — carry tags.
- `content-validate.exe` oficial — 0 erros / 0 warnings.

## Pendente

Nada de tradução. Restam apenas testes em jogo com o save real e a publicação
de novas versões quando o SkyrimNet atualizar (o bundle de UI precisa ser
reconstruído se o hash mudar).
