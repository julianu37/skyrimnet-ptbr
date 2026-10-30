# Revisão em 3 rodadas — marco atual

Data: 2026-10-30
Escopo: núcleo + todos os prompts de sistema + 250 bios + UI completa + YAML +
ESP.
Status: **sistema e interface 100% traduzidos; restam bios e YAML de config.**

## Rodada 1 — Completude

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts (todos) | 457 | 1632 | 28,0% |
| Bios de personagens | 334 | 1509 | 22,1% |
| Prompts de sistema (não-bios) | 123 | 123 | **100%** |
| Interface web (chaves) | 6753 | 6753 | **100%** |
| YAML de conteúdo | 16 | 35 | 45,7% |
| ESP (textos visíveis) | 9 | 9 | **100%** |
| MCM/Papyrus | n/a | n/a | — |

Detalhe dos prompts de sistema concluídos: raiz (17/17), `components` (15/15),
`decisions` (5/5), `helpers` (3/3), `memory` (5/5), `omnisight` (7/7),
`target_selectors` (2/2), `transformers` (2/2), `web` (2/2),
`submodules/system_head` (8/8), `submodules/user_final_instructions` (11/11),
`submodules/character_bio` (18/18), `guidelines` (1/1),
`submodules/omnisight_*` (6/6), `eval` (7/7), `documentation` (2/2), `dev`
(1/1), `submodules/test_decorators` (11/11).

YAML traduzido: filtros (6), efeitos de voz (8), listas de Dialogue Actions
(2). `furniture` mantido em inglês de propósito: os prompts comparam
`Carriage`, `bed`, `table` etc. e traduzir quebraria a detecção. Os
`config/carry_tags_*` não fazem parte da Content Library.

## Rodada 2 — Funcional

| Verificação | Resultado |
|---|---|
| Validador de prompts (Jinja, tags, expressões, markers, UTF-8) | **0 erros**; 10 warnings de termos de jogo/comentários |
| Chaves JSON dentro dos prompts | **0 divergências** |
| Placeholders da UI | **0 divergências** em 6.753 chaves |
| `node --check` no bundle patchado | OK |
| `node --check` no `pt-br.js` | OK |
| Zip do MO2 | 373 prompts + UI + YAML |
| Mod ativo no MO2 | 373 prompts; UI aplicada na base `skyrimnet` |
| Manifest | `julianu37.skyrimnet-ptbr` |
| Adapter Kokoro | `ok` em `127.0.0.1:8020` |
| Teste com Qwen2.5-3B (prompt núcleo) | resposta em **PT-BR** |
| Seletor de idioma da UI | **Português (Brasil)**; locale inicial `pt-br` |
| ESP patch | 9/9 textos, tamanho preservado, estrutura validada (56 records/19 groups) |

Observação: o patch de UI foi aplicado **na pasta do mod base `skyrimnet`**
(backup `index.html.ptbr-original`), então não depende da ordem do MO2. O bundle
patchado tem nome `main.027620d9.ptbr.js` para evitar cache.

O patch do ESP é byte-preserving: substitui apenas strings de tamanho igual ou
menor, preenchendo com NUL, sem alterar records/GRUPs. Backup em
`SkyrimNet.esp.ptbr-original`.

## Rodada 3 — Consistência e QA

- Terminologia: `dunmer` padronizado; `GameMaster` → **Mestre de Jogo** na UI;
  `Forte`, `Mina`, `Caverna`, `Fazenda` padronizados.
- `intendente`, `Legião Imperial`, `Colégio de Winterhold`, `Concordata
  White-Gold`, `Alto Rei` mantidos conforme glossário.
- `Companions` permanece em inglês para a guilda; `Quinhentos Companheiros`
  para a hoste histórica.
- Warnings de inglês: nomes de itens/facções, comentários Jinja e variáveis;
  nada de prosa instrucional em inglês no núcleo.
- Licença/atribuição: `LICENSE`, `NOTICE.md`, `LICENSES/` presentes.
- Git: árvore limpa; commits recentes `f199d17`, `76e4ba6`, `89b7a6f`,
  `207cd81`, `25de02f`, `646d308`.
- Amostragem manual: Balgruuf, Maven, Hulda, `event_history`, `system_head`,
  `user_final_instructions`, `eval`, `documentation`, UI de navegação e
  Configurações.

## Veredito

O caminho que causava o inglês está corrigido e testado com o mesmo 3B:
prompt português-dominante → resposta em PT-BR. Sistema, UI, YAML de conteúdo
e textos do ESP estão cobertos.

A tradução **ainda não está completa**: faltam 1.175 bios (811 nomeadas + 364
genéricas) e 19 YAML de configuração. As 334 bios atuais e os 457 prompts
estão validados e ativos.
