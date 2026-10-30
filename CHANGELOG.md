# Changelog

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
