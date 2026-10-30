# Revisão em 3 rodadas — marco atual

Data: 2026-10-30
Escopo: núcleo de diálogo PT-BR + interface web + 58 bios.
Status: **núcleo funcional; tradução completa ainda pendente**.

## Rodada 1 — Completude

### Prompts

| Camada | Traduzidos | Total | Falta |
|---|---:|---:|---:|
| `characters` | 58 | 1509 | 1451 |
| `submodules` | 19 | 55 | 36 |
| raiz | 2 | 17 | 15 |
| `components` | 0 | 15 | 15 |
| `decisions` | 0 | 5 | 5 |
| `helpers` | 0 | 3 | 3 |
| `memory` | 0 | 5 | 5 |
| `omnisight` | 0 | 7 | 7 |
| `target_selectors` | 0 | 2 | 2 |
| `transformers` | 0 | 2 | 2 |
| `web` | 0 | 2 | 2 |
| `eval` | 0 | 7 | 7 |
| `documentation` | 0 | 2 | 2 |
| `dev` | 0 | 1 | 1 |
| **Total** | **79** | **1632** | **1553** |

### Interface web

| Item | Cobertura |
|---|---:|
| Chaves no bundle | 6.753 |
| Traduzidas | 965 (14,3%) |
| Pendentes | 5.788 |
| Placeholders/key mismatch | 0 |

### Outras camadas

- YAML de conteúdo: 0/35 traduzidos.
- MCM/Papyrus: pendente.
- ESP: pendente.

## Rodada 2 — Funcional

| Verificação | Resultado |
|---|---|
| Validador de prompts (Jinja, tags, expressões, markers, UTF-8) | **0 erros**; 2 warnings esperados |
| Placeholders da UI | **0 divergências** |
| `node --check` no bundle patchado | OK |
| `node --check` no `pt-br.js` | OK |
| Zip do MO2 | 87 entradas; **79 prompts** + **3 arquivos de UI** |
| Mod ativo no MO2 | 79 prompts; UI (`index.html`, `main.027620d9.js`, `pt-br.js`) |
| Manifest | `julianu37.skyrimnet-ptbr` |
| Adapter Kokoro | `ok` em `127.0.0.1:8020` |
| Teste com Qwen2.5-3B (prompt núcleo traduzido) | resposta em **PT-BR** |
| Camada de conteúdo no jogo | última inicialização: 2 layers, 0 rejected; falta reiniciar com o núcleo novo |

## Rodada 3 — Consistência e QA

- Terminologia: `intendente` (17), `Legião Imperial` (12), `Colégio de Winterhold` (5), `Concordata White-Gold` (6). Os 3 `administrador` restantes são “administradores da mina” (função, não Steward).
- `Companheiros`/`Círculo` restantes são substantivos comuns em minúsculas, não os nomes de facção.
- Aviso de inglês em `8000_recent_state_changes.prompt`: somente comentários Jinja (`{# Track... #}`) e nomes de variáveis; nada renderizado.
- Licença/atribuição: `LICENSE`, `NOTICE.md` e `LICENSES/SkyrimNet-GamePlugin-LICENSE.txt` presentes.
- Git: árvore limpa; commits `1918933` (UI + núcleo), `2b5b6d6` (modelo), `d5d4def` (diretiva).
- Amostragem manual: Balgruuf, Maven, Hulda, prompts de sistema e UI de navegação — tom e terminologia consistentes.

## Veredito

O **núcleo que causava o inglês** está corrigido e testado com o próprio 3B: o prompt
agora é português-dominante (system_head + user_final + template), e a resposta
do teste saiu em PT-BR.

A tradução **não está completa**: faltam 1.553 prompts, 5.788 chaves de UI, 35
YAML e MCM/ESP. O próximo ciclo deve atacar, nesta ordem:

1. `components`, `decisions`, `helpers`, `memory`, `target_selectors`,
   `transformers`, `omnisight` (39 arquivos).
2. Restante de `submodules` (36).
3. Bios em lotes (1.451).
4. UI restante (5.788 chaves).
5. YAML, MCM e ESP.
