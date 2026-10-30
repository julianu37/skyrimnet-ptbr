# Revisão do benchmark local — Qwen2.5-3B-Instruct

Ambiente: LM Studio, endpoint `http://127.0.0.1:1234/v1`, modelo
`qwen2.5-3b-instruct`, 12 cenários com as bios traduzidas.

Duas rodadas:

| Rodada | Prompt de sistema | Temperatura | max_tokens |
|---|---|---|---|
| 1 | bio + resumo + personalidade + estilo + relações | 0,7 | 180 |
| 2 | bio + resumo + personalidade + estilo, primeira pessoa, sem narração | 0,5 | 140 |

## Métricas

| Métrica | Rodada 1 | Rodada 2 |
|---|---:|---:|
| Latência média | ~0,60 s | ~0,52 s |
| Velocidade média | ~128 tok/s | ~127 tok/s |
| Respostas em PT-BR | 12/12 | 12/12 |
| Coerência manual (média) | ~2,8/5 | ~3,0/5 |

A rodada 2 melhorou o formato (primeira pessoa, menos narração de terceiros),
mas os erros de gramática/coerência continuam.

## Avaliação manual (rodada 2)

| NPC | Nota | Observação |
|---|---:|---|
| Hulda | 3/5 | Tom de taverneira, mas "só sougo" é erro grave. |
| Jarl Balgruuf | 3/5 | Postura firme; "Voua Imperial" quebra a frase. |
| Maven Black-Briar | 4/5 | Ameaça coerente e no tom; a melhor da rodada. |
| Jarl Ulfric | 4/5 | Discurso de liberdade consistente com a bio. |
| Farengar | 2/5 | Inventa lore sobre a Pedra do Dragão ("energia ancestral"). |
| Lydia | 2/5 | Fora do personagem: recusa o dever e fala em "mulheres solteiras". |
| Belethor | 3/5 | Tom mercenário, mas a piada com criança ficou estranha. |
| Aela | 3/5 | Tom de caçadora, mas "invisível em meio à neve" não faz sentido. |
| Brynjolf | 4/5 | Coerente: oferece a guilda sem entregar o golpe. |
| Jarl Elisif | 3/5 | Tom correto; "Vou e seus companheiros" é erro de concordância. |
| Carlotta | 2/5 | Trata Mila como filho e reage de forma estranha. |
| Nazeem | 3/5 | Arrogância correta; concordância fraca ("camponês ignorante"). |

**Média: 3,0/5.** Idioma: 12/12 em PT-BR.

## Conclusão

- O **pacote de conteúdo** não é o gargalo: as bios direcionam tom, facção e
  vocabulário (Maven, Ulfric, Brynjolf e Nazeem saíram claramente no personagem).
- O **Qwen2.5-3B-Instruct** é pequeno demais para diálogo final: erros de
  concordância, frases quebradas e desvios de lore aparecem em ~metade das
  respostas.
- Para jogar de verdade, usar um modelo 7B–14B (Qwen2.5-7B/14B-Instruct,
  Gemma 2 9B, Llama 3.1 8B). O 3B serve para teste de fumaça/latência.
- O pipeline real do SkyrimNet adiciona memória, eventos e ações; isso tende a
  melhorar o contexto, mas também sobrecarrega modelos 3B.

## Limitações do benchmark

- Usa a bio traduzida + instrução de idioma, não o prompt completo do SkyrimNet.
- Métricas de idioma/palavras-chave são heurísticas; a nota de coerência é
  revisão manual.
- Um único modelo e uma única execução por cenário; temperatura 0,5–0,7.
