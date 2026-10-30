# Progresso da tradução

Atualizado em 2026-10-30.

## Cobertura atual

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | 160 | 1632 | 9,8% |
| Bios de personagens | 58 | 1509 | 3,8% |
| Núcleo de sistema/diálogo | 102 | 123 | 82,9% |
| Interface web (chaves) | 965 | 6753 | 14,3% |
| YAML de conteúdo | 0 | 35 | 0% |
| MCM/Papyrus | 0 | 1 | 0% |
| ESP | 0 | 1 | 0% |

## Lotes concluídos

| Lote | Arquivos | Status |
|---|---:|---|
| Piloto (10 bios + diretiva) | 12 | commit `ee2aff9` |
| 48 bios (Whiterun/Riverwood/Solitude/Windhelm/Riften/Markarth) | 48 | commit `687e419` |
| Núcleo: `system_head`, `user_final_instructions`, diálogo | 21 | commit `1918933` |
| Interface web: core, settings, TTS/LLM/logs/chat | 965 chaves | commit `1918933` |
| `components` + `target_selectors` + `web` | 19 | este lote |
| `decisions` + `helpers` + `memory` + `transformers` | 15 | este lote |
| `omnisight` + `submodules/omnisight_*` + guidelines | 14 | este lote |
| Prompts raiz (agentes, pensamentos, gamemaster) | 15 | este lote |
| `submodules/character_bio` | 18 | este lote |

## Regras e ferramentas

- Glossário: `glossary/ptbr.yaml`.
- Validador: `tools/validate_prompts.py --allow-subset` (Jinja, tags,
  expressões, markers, UTF-8, proporção, inglês residual).
- Listas de lote: `batches/*.txt`.
- UI: `ui/build_ui.py` + `ui/pt-br/*.json`.
- Empacotamento: `tools/package.py` (zip MO2 + pasta do catálogo).

## Pendente

1. 1.451 bios restantes (lotes de ~40).
2. `eval` (7), `documentation` (2), `dev` (1), `test_decorators` (10).
3. 5.788 chaves de UI (settings restantes, plugins, characters, gamedata,
   prompts, actions, triggers, etc.).
4. 35 YAML de conteúdo (filtros, voice effects, furniture, etc.).
5. MCM/Papyrus e ESP.

## Próximo lote sugerido

- UI `settings` restante (~1.047 chaves) em 3 subagentes.
- UI `plugins`/`characters` em 3 subagentes.
- Bios: 4 subagentes × 12 por rodada.
