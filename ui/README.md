# Interface web em PT-BR

O dashboard do SkyrimNet usa um dicionário i18n embutido no bundle
`main.*.js`. Não existe carregamento externo de locale, então o pacote
**injeta** um dicionário `pt-br` e adiciona a opção no seletor de idioma.

## Como funciona

1. `ui/pt-br/*.json` contém as traduções por área (`core`, `settings`, `pages`).
2. `ui/build_ui.py`:
   - lê o bundle **instalado** do SkyrimNet (`assets/web-new`);
   - gera `pt-br.json` e `pt-br.js`;
   - injeta `"pt-br"` no mapa de locales;
   - adiciona `Português (Brasil)` ao seletor;
   - força o locale inicial `pt-br` (ignora `Dashboard.locale=en`);
   - adiciona `<script src="pt-br.js">` ao `index.html`.
3. A saída fica em `ui/build/assets/web-new/` e é incluída no zip do MO2.
   O bundle patchado é renomeado para `main.<hash>.ptbr.js` para evitar cache
   do navegador; o `index.html` aponta para ele.

## Build

```powershell
python ui/build_ui.py --source "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\assets\web-new"
```

O `main.*.js` muda de nome/hash a cada release do SkyrimNet. O script detecta o
arquivo atual e valida os padrões antes de aplicar; se o SkyrimNet mudar o
código, o build falha em vez de gerar um bundle quebrado.

## Cobertura

- **6.753 de 6.753 chaves (100%)** do bundle `main.027620d9.js` traduzidas,
  incluindo nav, common, home, settings, TTS, LLM, logs, chat, plugins,
  personagens, gamedata, prompts, actions, triggers, routing, tutorial,
  world knowledge, debug, traces, memórias, visão, Vast.ai, bardos, editor de
  arquivos e telas finais.
- Chaves ausentes caem no inglês automaticamente (`d.en`).
- Para traduzir uma nova área após um update do SkyrimNet, adicione fatias em
  `ui/source/` e traduções em `ui/pt-br/`, depois rode o build.
- O build valida que o número de chaves do dicionário final é 6.753 e que os
  placeholders `{{...}}` batem com o inglês.

## Instalação

O zip do MO2 inclui:

```
SKSE/Plugins/SkyrimNet/assets/web-new/
├── index.html
├── main.<hash>.js
└── pt-br.js
```

Isso **sobrescreve** os assets da UI base. O mod de tradução precisa ficar
**abaixo** de `skyrimnet` no painel esquerdo do MO2 (prioridade maior).

Alternativa usada na instalação local: aplicar o overlay diretamente na pasta
do mod base `skyrimnet` (com backup de `index.html` em
`index.html.ptbr-original`). Assim a UI não depende da ordem do MO2. Um update
do SkyrimNet sobrescreve o patch; rode o build novamente.

Se o SkyrimNet for atualizado, rode o build novamente com o novo bundle. Para
desativar só a UI, restaure o `index.html` original e remova
`main.<hash>.ptbr.js`/`pt-br.js`.
