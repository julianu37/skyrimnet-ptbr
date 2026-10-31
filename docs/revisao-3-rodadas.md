# Revisão em 3 rodadas — versão 1.0

Data: 2026-10-30
Escopo: 1.632 prompts, 7.785 chaves de UI, 35 YAML, textos do ESP e carry tags.
Status: **tradução 100% concluída e validada**.

## Rodada 1 — Completude

| Camada | Traduzido | Total | % |
|---|---:|---:|---:|
| Prompts | **1632** | 1632 | **100%** |
| Bios de personagens | **1509** | 1509 | **100%** |
| Prompts de sistema | **123** | 123 | **100%** |
| Interface web | **7785** | 7785 | **100%** |
| YAML de conteúdo | **35** | 35 | **100%** |
| ESP (textos visíveis) | **9** | 9 | **100%** |
| MCM/Papyrus | n/a | n/a | — |

- Todos os arquivos da base têm contraparte traduzida no mesmo caminho.
- Nenhuma bio, prompt de sistema ou chave de UI ficou sem tradução.
- `config/carry_tags_*` e ESP são patches locais reproduzíveis por script.

## Rodada 2 — Funcional

| Verificação | Resultado |
|---|---|
| `tools/validate_prompts.py` (1.632 prompts) | **0 erros**; 9 avisos de termos técnicos |
| `content-validate.exe` oficial (beta28) | **0 erros, 0 warnings**, exit 0 |
| Placeholders da UI (7.785 chaves) | **0 divergências** |
| Chaves JSON dentro dos prompts | **0 divergências** |
| `node --check` no bundle patchado | OK |
| `node --check` no `pt-br.js` | OK |
| Dashboard in-game (PrismaUI) | patch em `dashboard.b3966cee.js` + `pt-br.js`, 7.785 chaves |
| Contexto do LM Studio | 16.384 tokens; replay de 10.881 tokens OK |
| Zip do MO2 | 1.632 prompts + UI + 35 YAML + ferramentas |
| Mod ativo no MO2 | 1.632 prompts sincronizados |
| ESP patch | 9/9, estrutura e tamanho preservados |
| Carry tags | 11/11, backups `.ptbr-original` |
| Adapter Kokoro | `ok` em `127.0.0.1:8020` |
| Teste com Qwen2.5-3B | resposta em **PT-BR** |
| Seletor de idioma | **Português (Brasil)**, locale inicial `pt-br` |

## Rodada 3 — Consistência e QA

- Terminologia normalizada em todos os 1.632 prompts:
  `dunmer`, `housecarl`, `Forsworn`, `The Reach`, `Companions`, `Jarl`,
  `Thane`, `Mestre de Jogo`, `Colégio de Bardos`, `Forte`, `Mina`,
  `Caverna`, `Fazenda`, `Mar dos Fantasmas`, `All-Maker`,
  `Sacerdote Mariposa`, `Pergaminho Ancestral`, `Briarheart`, `skeever`,
  `Parente de Sangue`.
- Móveis traduzidos (`Carruagem`, `Balcão`) com condições equivalentes na
  lógica de `component_npc_state_summary` e `0050_physical_activity`.
- Warnings restantes: nomes de itens/facções, comentários Jinja e variáveis;
  nenhuma prosa instrucional em inglês.
- Licença/atribuição: `LICENSE`, `NOTICE.md`, `LICENSES/` presentes.
- Git: árvore limpa; versão `1.1.0`.
- Amostragem manual: Balgruuf, Maven, Hulda, Lydia, `system_head`,
  `user_final_instructions`, `event_history`, `eval`, `documentation`,
  genéricos de guarda/bandido, UI de configurações e plugins.

## Veredito

**Tradução completa.** O caminho que causava respostas em inglês está
corrigido e testado com o mesmo Qwen2.5-3B. O pacote 1.0.0 contém prompts,
bios, UI, YAML e textos do ESP em PT-BR, com validação oficial limpa.
