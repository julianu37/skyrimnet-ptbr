# Changelog

## 0.2.0 — 2026-10-30

- **Interface web 100% traduzida**: 6.753 de 6.753 chaves, incluindo
  configurações, TTS/STT, LLM, plugins, personagens, gamedata, prompts,
  actions, triggers, routing, tutorial, world knowledge, debug, traces,
  memórias, visão, Vast.ai, bardos e editor de arquivos.
- **Todos os prompts de sistema traduzidos**: 123 de 123 (núcleo, componentes,
  decisões, memória, OmniSight, eval, documentação, decorators).
- **Bios**: 490 bios nomeadas e genéricas traduzidas (em expansão).
- **YAML de conteúdo**: **35 de 35 (100%)** — filtros, efeitos de voz,
  Dialogue Actions, móveis e carry tags (estes via patch local).
- **ESP**: patch opcional `tools/patch_esp.py` para descrições de feitiços e
  mensagens do plugin (9 textos, byte-preserving).
- **UI**: seletor “Português (Brasil)”, locale inicial `pt-br` e bundle
  cache-busted.
- **Qualidade**: validador de prompts com 0 erros; paridade de UI com 0
  placeholders divergentes; normalização de `dunmer`, `Mestre de Jogo`,
  `Forte`/`Mina`/`Caverna`/`Fazenda`.

## 0.1.0 — 2026-10-29

- Primeira camada externa com diretiva de idioma, 58 bios e UI parcial.
- Adapter Kokoro PT-BR publicado separadamente.
