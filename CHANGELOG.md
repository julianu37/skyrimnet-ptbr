# Changelog

## 1.2.0 — 2026-10-30

- **Correção das respostas em inglês**: o Qwen2.5-3B estava imitando o
  histórico de falas antigas em inglês, mesmo com a diretiva em português.
  O modelo local foi trocado para **Qwen2.5-7B-Instruct** em 16.384 tokens.
- **Diretiva reforçada** em `dialogue_response` e `player_dialogue`: ignorar
  falas antigas do histórico em inglês e responder obrigatoriamente em PT-BR.
- **Validação real**: o payload exato da conversa foi reexecutado no 7B e
  respondeu em português, inclusive com histórico inglês.
- Contexto do LM Studio: 16.384 tokens (o 3B/7B precisa disso; 8.192 causa
  HTTP 400).

## 1.1.0 — 2026-10-30

- **Correção do dashboard in-game**: o patch de UI agora é aplicado em
  `PrismaUI/views/SkyrimNet/dashboard` (o bundle que o jogo realmente carrega),
  além de `assets/web-new`.
- **UI completa também no PrismaUI**: 7.785 chaves (6.753 do bundle web + 1.032
  específicas do dashboard in-game).
- **Correção do contexto do LLM**: Qwen2.5-3B recarregado com 16.384 tokens
  (antes 8.192); as requisições de memória de ~10.800 tokens voltaram a
  funcionar.
- **Diagnóstico**: logs mostravam HTTP 400 `exceed_context_size_error` em todas
  as chamadas; prompts já estavam em PT-BR.
- **Pacote** inclui o overlay PrismaUI e o `pt-br.js` do dashboard.

## 1.0.0 — 2026-10-30

- **Tradução completa**: 1.632 de 1.632 prompts (1.509 bios + 123 de sistema).
- **Interface web 100%**: 6.753 de 6.753 chaves.
- **YAML 100%**: filtros, efeitos de voz, Dialogue Actions, móveis e carry tags.
- **ESP 100%**: 9 textos player-facing via `tools/patch_esp.py`.
- **Terminologia normalizada** em todos os prompts (dunmer, housecarl,
  Forsworn, The Reach, Mestre de Jogo, Colégio de Bardos, Forte, Mina,
  Caverna, Fazenda, Mar dos Fantasmas, All-Maker, Briarheart etc.).
- **Validação oficial**: `content-validate.exe` 0 erros / 0 warnings.
- **Validador próprio**: 0 erros; 9 avisos de termos técnicos.
- **UI**: seletor “Português (Brasil)”, locale inicial `pt-br`, bundle
  cache-busted.
- **Qualidade**: paridade de placeholders 0; BOM/CRLF normalizados.

## 0.2.0 — 2026-10-30

- UI 100%, prompts de sistema 100%, 490 bios, YAML de conteúdo e patch do ESP.
- Primeira validação oficial limpa.

## 0.1.0 — 2026-10-29

- Primeira camada externa com diretiva de idioma, 58 bios e UI parcial.
- Adapter Kokoro PT-BR publicado separadamente.
