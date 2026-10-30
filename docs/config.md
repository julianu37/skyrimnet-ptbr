# Patch de configuração (carry tags)

Os arquivos `config/carry_tags_*.yaml` não fazem parte da Content Library do
SkyrimNet, então um plugin não pode distribuí-los. Eles controlam os rótulos de
emoção/estilo usados pelo TTS. O script `tools/patch_config.py` traduz apenas
`name` e `description`; os valores em `tags` continuam em inglês porque são
comparados com as tags geradas pelo modelo.

## Como aplicar

1. Feche o Skyrim.
2. Rode:

   ```powershell
   python tools\patch_config.py "C:\...\mods\skyrimnet\SKSE\Plugins\SkyrimNet\library\skyrimnet.base\config"
   ```

3. Confira sem gravar:

   ```powershell
   python tools\patch_config.py "...\config" --check
   ```

Cada arquivo alterado ganha um backup `.ptbr-original` na primeira execução. O
script é idempotente.

## Reverter

Renomeie os arquivos `.ptbr-original` de volta para `.yaml` ou reinstale o
SkyrimNet por cima.
