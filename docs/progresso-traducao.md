# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura atual

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | 613 | 1632 | 37,6% |
| Bios de personagens | 490 | 1509 | 32,5% |
| Prompts de sistema (não-bios) | 123 | 123 | **100%** |
| Interface web (chaves) | 6753 | 6753 | **100%** |
| YAML de conteúdo | 16 | 35 | 45,7% |
| ESP (textos visíveis) | 9 | 9 | **100%** |
| MCM/Papyrus | n/a | n/a | — |

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
| Bios 13–16 | 48 | `7274aa6`, `8ee7650`, `aebd4b7`, `d4c23fb` |
| UI `settings` restante | 1047 chaves | `9072d00`, `9d1d44b`, `dfc61f9` |
| UI `plugins` + `characters` | 920 chaves | `bf4ff25`, `073ced9`, `20d78c9` |
| UI `gamedata` + `prompts` | 795 chaves | `7234876`, `c2047ed`, `f1d9dd1` |
| UI `actions` + `triggers` + `routing` | 540 chaves | `4ce1cb7` |
| UI `world_knowledge` + `tutorial` | 646 chaves | `d87d26f`, `646d308` |
| UI `debug` + `vast_ai` + `bards` + `file_editor` | 493 chaves | `8ddca6b` |
| UI `memories` + `vision` + `traces` + `record` | 324 chaves | `d87d26f` |
| UI final A–C | 791 chaves | `f199d17` |
| UI final D | 232 chaves | `8e304e0` |
| Prompts de sistema restantes | 21 | `25de02f`, `76e4ba6` |
| YAML: filtros, voice effects, dialogue actions | 16 registros | `d896cb8` |
| ESP: descrições e mensagens | 9 textos | local (backup) |

## Revisões e normalizações

- `dunmer` padronizado (substituído "elfo negro").
- `GameMaster` padronizado como **Mestre de Jogo** na UI.
- `Forte`, `Mina`, `Caverna`, `Fazenda` padronizados nos textos de bios.
- Glossário ganhou a seção `review_decisions` com as decisões acima.

## Ferramentas e regras

- Glossário: `glossary/ptbr.yaml`.
- Validador: `tools/validate_prompts.py --allow-subset` (Jinja, tags,
  expressões, markers, UTF-8, proporção, inglês residual; literais traduzidos
  são permitidos).
- Listas de lote: `batches/*.txt`.
- UI: `ui/build_ui.py` + `ui/pt-br/*.json` + `ui/source/*.json`.
- Empacotamento: `tools/package.py` (zip MO2 + pasta do catálogo).
- ESP: `tools/patch_esp.py` (patch byte-preserving com backup).

## Pendente

1. 1.019 bios restantes (lotes de ~48): 751 nomeadas + 268 genéricas.
2. 19 YAML restantes: `config/carry_tags_*` (11, fora da Content Library) e
   `furniture` (4, mantidos em inglês por dependência da lógica dos prompts).
3. MCM/Papyrus: o SkyrimNet não usa MCM do SkyUI; as opções ficam no
   dashboard web (já 100% traduzido).

## Próximo lote sugerido

- Bios 21–24 (`batches/bios_21..24.txt`), 48 arquivos.
- Depois priorizar bios genéricas de guardas, soldados e bandidos, que são as
  vozes mais frequentes em jogo.

