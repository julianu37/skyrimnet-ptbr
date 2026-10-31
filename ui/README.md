# Interface PT-BR

O SkyrimNet tem dois dashboards:

| Onde | Bundle | Patch |
|---|---|---|
| **In-game (PrismaUI)** | `PrismaUI/views/SkyrimNet/dashboard/dashboard.<hash>.js` | `ui/build_prisma.py` |
| **Web** | `SKSE/Plugins/SkyrimNet/assets/web-new/main.<hash>.js` | `ui/build_ui.py` |

Os dois usam um dicionário i18n embutido, sem carregamento externo de locale.
O pacote injeta um dicionário `pt-br` e registra a opção no seletor.

## Dashboard in-game (PrismaUI)

`ui/build_prisma.py`:

- lê `PrismaUI/views/SkyrimNet/dashboard`;
- gera `pt-br.js` com 7.785 chaves;
- adiciona `<script src="pt-br.js">` e `pt-br.js` à lista de assets;
- patcheia `const n={en:i}` para incluir `pt` e `pt-br`;
- copia o resultado para `ui/build/prisma/dashboard/`.

```powershell
python ui/build_prisma.py --source "C:\...\mods\skyrimnet\PrismaUI\views\SkyrimNet\dashboard"
```

O `Dashboard.yaml` já vem com `locale: pt-br`; o alias `pt-br` no provider faz
o dashboard abrir em português.

## Dashboard web

`ui/build_ui.py`:

- lê `assets/web-new`;
- gera `pt-br.json`/`pt-br.js`;
- injeta `pt-br` no mapa de locales e cache-busta o bundle para
  `main.<hash>.ptbr.js`;
- copia para `ui/build/assets/web-new/`.

```powershell
python ui/build_ui.py --source "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\assets\web-new"
```

## Cobertura

- **7.785 de 7.785 chaves (100%)**: 6.753 do bundle web + 1.032 específicas do
  PrismaUI.
- Chaves ausentes caem no inglês.
- `python tools/check_ui.py` valida chaves e placeholders.

## Instalação

O zip inclui:

```
PrismaUI/views/SkyrimNet/dashboard/
├── index.html
├── dashboard.<hash>.js
└── pt-br.js
SKSE/Plugins/SkyrimNet/assets/web-new/
├── index.html
├── main.<hash>.ptbr.js
└── pt-br.js
```

O mod PT-BR deve ficar **abaixo** de `skyrimnet` no MO2 (prioridade maior).
Na instalação local, os assets também foram aplicados diretamente na pasta do
mod base, com backups `*.ptbr-original`, para não depender da ordem do MO2.

Se o SkyrimNet atualizar, rode os dois builds novamente. Para reverter,
restaure os `*.ptbr-original` e remova `pt-br.js`/`main.<hash>.ptbr.js`.
