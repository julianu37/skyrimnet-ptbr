# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura atual

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | 304 | 1632 | 18,6% |
| Bios de personagens | 202 | 1509 | 13,4% |
| Prompts de sistema (não-bios) | 102 | 123 | 82,9% |
| Interface web (chaves) | 4267 | 6753 | 63,2% |
| YAML de conteúdo | 16 | 35 | 45,7% |
| MCM/Papyrus | n/a | n/a | — |
| ESP | n/a | n/a | — |

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
| Bios 01–04 | 48 | `7735d35`, `fd242ca`, `3dbd27d`, `7c6ba97` |
| Bios 05–08 | 48 | `b38818b`, `9fbb5f1`, `3d39a9c`, `ce765b2` |
| Bios 09–12 | 48 | `2b60a99`, `594cd34`, `50f6ec0`, `8ea5446` |
| UI `settings` restante | 1047 chaves | `9072d00`, `9d1d44b`, `dfc61f9` |
| UI `plugins` + `characters` | 920 chaves | `bf4ff25`, `073ced9`, `20d78c9` |
| UI `gamedata` + `prompts` | 795 chaves | `7234876`, `c2047ed`, `f1d9dd1` |
| UI `actions` + `triggers` + `routing` | 540 chaves | `4ce1cb7` |
| YAML: filtros, voice effects, dialogue actions | 16 registros | `d896cb8` |

## Ferramentas e regras

- Glossário: `glossary/ptbr.yaml`.
- Validador: `tools/validate_prompts.py --allow-subset` (Jinja, tags,
  expressões, markers, UTF-8, proporção, inglês residual; literais traduzidos
  são permitidos).
- Listas de lote: `batches/*.txt`.
- UI: `ui/build_ui.py` + `ui/pt-br/*.json` + `ui/source/*.json`.
- Empacotamento: `tools/package.py` (zip MO2 + pasta do catálogo).

## Pendente

1. 1.307 bios restantes (lotes de ~48).
2. `eval` (7), `documentation` (2), `dev` (1), `test_decorators` (10).
3. 1.840 chaves de UI (tutorial e world_knowledge em andamento; depois
   debug, vast_ai, bards, file_editor, etc.).
4. 19 YAML restantes: `config/carry_tags_*` (11, fora da Content Library)
   e `furniture` (4, mantidos em inglês por dependência da lógica dos prompts).
5. MCM/Papyrus: o SkyrimNet não usa MCM do SkyUI; as opções ficam no
   dashboard web (já traduzido). ESP: só contém registros de teste
   (`Alrik Test-Alpha`, `Bera Test-Beta`) e nenhum texto de jogador.

## Em andamento

- Bios lotes 13–16 (`batches/bios_13..16.txt`), 48 arquivos.
- UI `actions`, `triggers`, `routing` (540 chaves).
- Prompts restantes de sistema (`batches/prompt_remaining.txt`, 21 arquivos).

## Próximo lote sugerido

- UI `tutorial` + `world_knowledge` (~646 chaves).
- Bios: novas rodadas de 4 × 12.
- Prompts restantes de sistema (20).
