# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura atual

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | 208 | 1632 | 12,7% |
| Bios de personagens | 106 | 1509 | 7,0% |
| Prompts de sistema (não-bios) | 102 | 123 | 82,9% |
| Interface web (chaves) | 2012 | 6753 | 29,8% |
| YAML de conteúdo | 0 | 35 | 0% |
| MCM/Papyrus | 0 | 1 | 0% |
| ESP | 0 | 1 | 0% |

## Lotes concluídos

| Lote | Arquivos | Commit |
|---|---:|---|
| Piloto (10 bios + diretiva) | 12 | `ee2aff9` |
| 48 bios (principais holds) | 48 | `687e419` |
| Núcleo: `system_head`, `user_final_instructions`, diálogo | 21 | `1918933` |
| UI core/settings/pages | 965 chaves | `1918933` |
| `components` + `target_selectors` + `web` | 19 | `d6c36db` |
| `decisions` + `helpers` + `memory` + `transformers` | 15 | `d6c36db` |
| `omnisight` + `submodules/omnisight_*` + guidelines | 14 | `d6c36db` |
| Prompts raiz | 15 | `d6c36db` |
| `submodules/character_bio` | 18 | `d6c36db` |
| Bios lote 01 | 12 | `7735d35` |
| Bios lote 02 | 12 | `fd242ca` |
| Bios lote 03 | 12 | `3dbd27d` |
| Bios lote 04 | 12 | `7c6ba97` |
| UI `settings` restante (3 lotes) | 1047 chaves | `9072d00`, `9d1d44b`, `dfc61f9` |

## Ferramentas e regras

- Glossário: `glossary/ptbr.yaml`.
- Validador: `tools/validate_prompts.py --allow-subset` (Jinja, tags,
  expressões, markers, UTF-8, proporção, inglês residual; literais traduzidos
  são permitidos).
- Listas de lote: `batches/*.txt`.
- UI: `ui/build_ui.py` + `ui/pt-br/*.json` + `ui/source/*.json`.
- Empacotamento: `tools/package.py` (zip MO2 + pasta do catálogo).

## Pendente

1. 1.403 bios restantes (lotes de ~48).
2. `eval` (7), `documentation` (2), `dev` (1), `test_decorators` (10).
3. 4.741 chaves de UI (plugins, characters, gamedata, prompts, actions,
   triggers, routing, etc.).
4. 35 YAML de conteúdo.
5. MCM/Papyrus e ESP.

## Em andamento

- Bios lotes 05–08 (`batches/bios_05..08.txt`), 48 arquivos.
- UI `plugins_1`, `plugins_2` e `characters` (920 chaves).

## Próximo lote sugerido

- Concluir bios restantes em rodadas de 4 × 12.
- UI `gamedata`, `prompts`, `actions`, `triggers`, `routing`.
- Prompts restantes de sistema (20).
