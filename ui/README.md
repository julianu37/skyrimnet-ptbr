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

## Build

```powershell
python ui/build_ui.py --source "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\assets\web-new"
```

O `main.*.js` muda de nome/hash a cada release do SkyrimNet. O script detecta o
arquivo atual e valida os padrões antes de aplicar; se o SkyrimNet mudar o
código, o build falha em vez de gerar um bundle quebrado.

## Cobertura

- 965 chaves traduzidas (nav, common, home, settings de voz/áudio/LLM,
  TTS, LLM, logs e chat).
- Chaves ausentes caem no inglês automaticamente (`d.en`).
- Para traduzir mais áreas, adicione fatias em `ui/source/` e traduções em
  `ui/pt-br/`, depois rode o build.

## Instalação

O zip do MO2 inclui:

```
SKSE/Plugins/SkyrimNet/assets/web-new/
├── index.html
├── main.<hash>.js
└── pt-br.js
```

Isso **sobrescreve** os assets da UI base. Se o SkyrimNet for atualizado,
rode o build novamente com o novo bundle. Para desativar só a UI, remova a
pasta `assets/web-new` do mod (ou desative o mod inteiro).
