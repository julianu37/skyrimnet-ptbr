# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura atual

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | 256 | 1632 | 15,7% |
| Bios de personagens | 154 | 1509 | 10,2% |
| Prompts de sistema (não-bios) | 102 | 123 | 82,9% |
| Interface web (chaves) | 2932 | 6753 | 43,4% |
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
| Bios 01–04 | 48 | `7735d35`, `fd242ca`, `3dbd27d`, `7c6ba97` |
| Bios 05–08 | 48 | `b38818b`, `9fbb5f1`, `3d39a9c`, `ce765b2` |
| UI `settings` restante | 1047 chaves | `9072d00`, `9d1d44b`, `dfc61f9` |
| UI `plugins` + `characters` | 920 chaves | `bf4ff25`, `073ced9`, `20d78c9` |

## Ferramentas e regras

- Glossário: `glossary/ptbr.yaml`.
- Validador: `tools/validate_prompts.py --allow-subset` (Jinja, tags,
  expressões, markers, UTF-8, proporção, inglês residual; literais traduzidos
  são permitidos).
- Listas de lote: `batches/*.txt`.
- UI: `ui/build_ui.py` + `ui/pt-br/*.json` + `ui/source/*.json`.
- Empacotamento: `tools/package.py` (zip MO2 + pasta do catálogo).

## Pendente

1. 1.355 bios restantes (lotes de ~48).
2. `eval` (7), `documentation` (2), `dev` (1), `test_decorators` (10).
3. 3.821 chaves de UI (gamedata, prompts, actions, triggers, routing, etc.).
4. 35 YAML de conteúdo.
5. MCM/Papyrus e ESP.

## Próximo lote sugerido

- UI `gamedata` + `prompts` (~795 chaves).
- Bios: 4 subagentes × 12 por rodada.
- Prompts restantes de sistema (20).
