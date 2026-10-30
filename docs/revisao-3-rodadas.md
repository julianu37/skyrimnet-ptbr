# Revisão em 3 rodadas — marco atual

Data: 2026-10-30
Escopo: núcleo + prompts de sistema + 58 bios + UI core.
Status: **núcleo e sistema funcionais; tradução completa pendente**.

## Rodada 1 — Completude

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts (todos) | 256 | 1632 | 15,7% |
| Bios de personagens | 154 | 1509 | 10,2% |
| Prompts de sistema (não-bios) | 102 | 123 | 82,9% |
| Interface web (chaves) | 2932 | 6753 | 43,4% |
| YAML de conteúdo | 0 | 35 | 0% |
| MCM/Papyrus | 0 | 1 | 0% |
| ESP | 0 | 1 | 0% |

Detalhe dos prompts de sistema concluídos: raiz (17/17), `components` (15/15),
`decisions` (5/5), `helpers` (3/3), `memory` (5/5), `omnisight` (7/7),
`target_selectors` (2/2), `transformers` (2/2), `web` (2/2),
`submodules/system_head` (8/8), `submodules/user_final_instructions` (11/11),
`submodules/character_bio` (18/18), `guidelines` (1/1),
`submodules/omnisight_*` (6/6).

Pendentes de sistema: `eval` (7), `documentation` (2), `dev` (1),
`submodules/test_decorators` (10).

## Rodada 2 — Funcional

| Verificação | Resultado |
|---|---|
| Validador de prompts (Jinja, tags, expressões, markers, UTF-8) | **0 erros**; 9 warnings de termos de jogo/comentários |
| Chaves JSON dentro dos prompts | **0 divergências** |
| Placeholders da UI | **0 divergências** |
| `node --check` no bundle patchado | OK |
| `node --check` no `pt-br.js` | OK |
| Zip do MO2 | 256 prompts + 3 arquivos de UI |
| Mod ativo no MO2 | 256 prompts; UI aplicada na base `skyrimnet` |
| Manifest | `julianu37.skyrimnet-ptbr` |
| Adapter Kokoro | `ok` em `127.0.0.1:8020` |
| Teste com Qwen2.5-3B (prompt núcleo) | resposta em **PT-BR** |
| Seletor de idioma da UI | opção **Português (Brasil)** no bundle; locale inicial `pt-br` |

Observação: o patch de UI foi aplicado **na pasta do mod base `skyrimnet`**
(backup `index.html.ptbr-original`), então não depende da ordem do MO2. O bundle
patchado tem nome `main.027620d9.ptbr.js` para evitar cache.

## Rodada 3 — Consistência e QA

- Terminologia: `intendente` (17), `Legião Imperial` (12), `Colégio de
  Winterhold` (5), `Concordata White-Gold` (6). `administrador` restante (3)
  refere-se a administradores de mina.
- `Companheiros`/`Círculo` restantes são substantivos comuns em minúsculas.
- Warnings de inglês: nomes de itens/facções, comentários Jinja e variáveis;
  nada de prosa instrucional em inglês no núcleo.
- Licença/atribuição: `LICENSE`, `NOTICE.md`, `LICENSES/` presentes.
- Git: árvore limpa; commits recentes `d6c36db`, `3f01234`, `e39cd1c`,
  `1918933`, `687e419`.
- Amostragem manual: Balgruuf, Maven, Hulda, `event_history`, `system_head`,
  `user_final_instructions` e UI de navegação.

## Veredito

O caminho que causava o inglês está corrigido e testado com o mesmo 3B:
prompt português-dominante → resposta em PT-BR. A UI agora tem o seletor
PT-BR e o bundle patchado.

A tradução **não está completa**: faltam 1.376 prompts, 3.821 chaves de UI,
35 YAML e MCM/ESP. Os oito lotes de bios (96 arquivos) foram validados e commitados;
154 bios estão ativas.
