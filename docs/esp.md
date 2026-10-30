# Patch do ESP (opcional)

O `SkyrimNet.esp` original contém alguns textos visíveis ao jogador que não vêm
do dashboard: descrições dos feitiços de telepatia e mensagens do plugin.

O script `tools/patch_esp.py` traduz **somente** esses textos, preservando o
tamanho dos registros. Ele não redistribui o ESP: aplica a tradução no arquivo
já instalado do SkyrimNet e cria um backup `.ptbr-original` na primeira execução.

## Como aplicar

1. Feche o Skyrim.
2. Descubra o caminho do ESP instalado. No MO2, normalmente:

   ```text
   ...\mods\skyrimnet\SkyrimNet.esp
   ```

3. Rode:

   ```powershell
   python tools\patch_esp.py "C:\...\mods\skyrimnet\SkyrimNet.esp"
   ```

4. Para conferir sem gravar:

   ```powershell
   python tools\patch_esp.py "C:\...\mods\skyrimnet\SkyrimNet.esp" --check
   ```

## O que é traduzido

- Descrições dos efeitos de telepatia (ouvir pensamentos).
- Mensagem de save antigo / linha do tempo.
- Botões e título da caixa de mensagem (`Apagar dados`, `Manter dados`,
  `Voltar`, `Linha divergente`).
- Texto de escopo do diário/bio dinâmica.

## O que não é traduzido

- EditorIDs, nomes de facções, keywords, packages e scripts.
- Nomes de móveis (`furniture/*.yaml`): a lógica dos prompts compara
  `Carriage`, `bed`, `table` etc. em inglês; traduzir quebraria a detecção.
- `config/carry_tags_*`: não fazem parte da Content Library e não podem ser
  empacotados como plugin.

## Reverter

Renomeie o backup de volta:

```powershell
Move-Item "SkyrimNet.esp.ptbr-original" "SkyrimNet.esp" -Force
```

O patch é idempotente: rodar de novo em um ESP já traduzido não altera nada.
