# Plano de tradução PT-BR do SkyrimNet

Status: executado até o marco de 2026-10-30 — prompts de sistema e UI 100%,
250+ bios, YAML de conteúdo e ESP cobertos. Restam bios. Objetivo: jogar em
português brasileiro sem forkar o mod e sem quebrar a cada update.

## 1. Princípio: camadas, não fork

Não editar `library/skyrimnet.base`. A tradução vira uma **camada externa**:

```
SKSE/Plugins/SkyrimNet/external/julianu37.skyrimnet-ptbr/
├── manifest.json
└── prompts/...
```

A camada externa resolve acima da base, aparece no dashboard e pode ser
desativada. Updates do SkyrimNet não sobrescrevem a tradução.

## 2. O que existe para traduzir

| Camada | Arquivos | Impacto | Risco |
|---|---|---|---|
| Diretiva de idioma (diálogo) | ~2–5 prompts | alto | baixo |
| UI do dashboard | 6.753 chaves i18n | alto | médio (bundle minificado) |
| Bios de personagens | 1.509 `.prompt` | médio | baixo (Jinja) |
| Outros prompts | 123 `.prompt` | médio | baixo |
| YAML de conteúdo | 16 de 35 (resto é config) | baixo | baixo |
| MCM / Papyrus | não existe MCM SkyUI | — | — |
| ESP | 9 strings visíveis | baixo | médio (patch byte-preserving) |

## 3. O que NÃO traduzir

- Jinja: `{% ... %}`, `{{ ... }}`, `{# ... #}` e **nomes de blocos**.
- Funções/decorators (`decnpc`, `render_subcomponent`, `get_actor_tts`), campos
  (`npc.UUID`, `actor.name`), chaves YAML/JSON, ids, nomes de arquivos.
- Tags de áudio (`[emotion-*]`, `[style-*]`, `[prosody-*]`, `[sfx-*]`).
- Nomes próprios de lugares/raças: a localização oficial PT-BR mantém a maioria
  em inglês (Whiterun, Riverwood, Jarl, Dragonborn). Ver glossário.

## 4. Ordem recomendada

### Fase 0 — glossário e estilo (1–2 dias)

`skyrimnet-ptbr/glossary/ptbr.yaml` com:
- termos que ficam em inglês;
- termos traduzidos (Vigor, Magia, Perícia, Missão...);
- tratamento (`você`), gírias, formatação de números;
- regra de ouro: em dúvida, manter o nome próprio.

Validar contra as strings oficiais do jogo (`Skyrim_portuguese.txt` se tiver a
instalação PT-BR; senão, conferir in game).

### Fase 1 — NPCs falando PT-BR (1 dia)

O idioma de saída não vem das 1.509 bios; vem da instrução de diálogo. Duas
opções:

**A. Universal Translator nativo (runtime).** O SkyrimNet já tem
`UniversalTranslator.yaml`, página `/universal-translator` e regras por
facção/raça. Testar primeiro: traduz a fala do NPC em tempo real, sem traduzir
conteúdo. Custo: uma chamada extra de LLM por linha e mais latência.

**B. Diretiva estática (recomendada para TTS).** Override de
`dialogue_response.prompt` e `player_dialogue.prompt` adicionando
"Responda sempre em português brasileiro". Custo zero em runtime, e o texto já
sai em PT-BR para o Kokoro. Precisa de revisão a cada update dos prompts.

Teste: 10 diálogos, 3 NPCs, com ações e pensamentos; conferir idioma, tags e
nomes.

### Fase 2 — UI do dashboard (3–5 dias)

O bundle tem um registro i18n (`_meta.locale`, `registerLocale`,
`Dashboard.locale`). O caminho limpo é adicionar um dicionário `pt-br` e setar
`Dashboard.locale = pt-br`. Se não houver carregamento externo de locale, gerar
um patch reproduzível do bundle (script que injeta o dicionário e recompila).

Não traduzir o código; só os valores do dicionário. Preservar `{{count}}` e
plurais.

### Fase 3 — prompts e bios (2–4 semanas, em lotes)

Ordem:
1. `components`, `decisions`, `helpers`, `memory`, `target_selectors`
   (123 arquivos) — impacto sistêmico.
2. Followers e NPCs de Whiterun/Riverwood/Riften/Solitude.
3. Restante das 1.509 bios.

Pipeline por lote:
1. Subagente tradutor recebe 25–40 arquivos + glossário + regras.
2. Validador determinístico (Jinja, `{{ }}`, blocos, proporção, UTF-8).
3. Subagente revisor amostra 10% + todas as falhas.
4. Merge só depois de validador + revisor.

### Fase 4 — MCM, ESP e release

- MCM: o SkyrimNet Beta25+ não usa MCM do SkyUI; as opções ficam no dashboard
  web. Não há script Papyrus de MCM para recompilar.
- ESP: `tools/patch_esp.py` traduz as 9 strings visíveis (descrições de
  feitiços e mensagens) preservando o tamanho dos registros. Backup automático.
- Empacotar `dist/SkyrimNet-PT-BR-<versão>.zip`, testar em load order limpa,
  versionar.

## 5. Sozinho ou com subagentes?

**Híbrido.** Subagentes são bons para volume e paralelismo; não são bons para
consistência global.

| Papel | Quem | Por quê |
|---|---|---|
| Glossário, arquitetura, validador | agente principal | decisões globais, uma fonte de verdade |
| Tradução em lote | subagentes (4–6 em paralelo) | 1.509 arquivos, contexto isolado |
| Revisão/QA | subagente revisor | amostragem e julgamento de estilo |
| Empacotamento/teste | agente principal | integração e validação final |

Regras para subagentes:
- um lote por vez, com caminhos absolutos;
- saída = conteúdo do arquivo, sem comentários;
- proibido renomear blocos, variáveis ou tags;
- nunca "corrigir" Jinja;
- o validador é a autoridade, não o subagente.

## 6. Estimativas

| Item | Volume | Esforço |
|---|---|---|
| Bios | ~6 MB de texto | ~26 lotes de 48 arquivos |
| Outros prompts | ~0,5 MB | concluído |
| UI | 6.753 chaves | concluído |
| MCM | não existe | — |

Com 4 subagentes em paralelo, as bios restantes ficam prontas em ~1–2 dias de
rodadas, mais revisão. O gargalo real é QA e teste in game, não a tradução.

## 7. Riscos

- **Update do mod**: prompts mudam; a camada externa precisa de merge guiado.
- **Aderência ao idioma**: só traduzir bios não garante resposta em PT-BR; a
  diretiva é obrigatória.
- **UI minificada**: patch de bundle quebra a cada release; manter script.
- **TTS**: pt-BR Kokoro tem 3 vozes; usar Voice Effects para variar timbre.
- **Custo**: Universal Translator adiciona chamada de LLM por fala; a diretiva
  estática não.

## 8. Próximos passos concretos

1. Fechar o glossário (Fase 0).
2. Testar a diretiva de idioma em 10 diálogos (Fase 1).
3. Usar `skyrimnet-ptbr/tools/validate_prompts.py` em cada lote.
4. Medir qualidade e custo antes de encomendar as 1.509.
5. Publicar o pacote no `MinLL/SkyrimNet-Plugins` quando estiver estável.
6. Empacotar com `python tools/package.py` (zip MO2 + pasta do catálogo).
