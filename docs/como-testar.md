# Como testar o pacote

## 1. Antes de abrir o jogo

1. Confirme que o **SkyrimNet** está instalado e ativo no MO2.
2. Confirme que **SkyrimNet PT-BR** está ativo e **abaixo** do SkyrimNet no
   painel esquerdo (prioridade maior para os assets de UI).
3. Confirme que o modelo local tem **32.768 tokens e Parallel = 1**:

   ```powershell
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" ps
   ```

   A coluna `CONTEXT` deve mostrar `32768` e `PARALLEL` deve mostrar `1`.
   Se estiver `4`, recarregue:

   ```powershell
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" unload qwen2.5-3b-instruct
   & "$env:USERPROFILE\.lmstudio\bin\lms.exe" load qwen2.5-3b-instruct -c 32768 --parallel 1 --gpu max -y
   ```

   O paralelismo divide o contexto: com 32k e 4 slots, cada memória/combate
   recebe só 8k e falha com “Context size has been exceeded”.

4. Confirme que o adapter Kokoro está no ar:

   ```powershell
   curl http://127.0.0.1:8020/health
   ```

   A resposta deve conter `"status":"ok"`.

4. Confira que o plugin foi reconhecido no log:

   ```text
   ...\Documents\My Games\Skyrim Special Edition\SKSE\SkyrimNet.log
   ```

   Procure por `julianu37.skyrimnet-ptbr` e por avisos de arquivos ignorados.

## 2. Dashboard

1. Entre no jogo e abra o dashboard do SkyrimNet.
2. Para o dashboard **in-game**, não é preciso Ctrl+F5: ele carrega
   `PrismaUI/views/SkyrimNet/dashboard`, já patcheado. Para o dashboard **web**,
   pressione **Ctrl+F5**.
3. O `Dashboard.yaml` já está com `locale: pt-br`; o dicionário tem os aliases
   `pt` e `pt-br`.
4. Verifique:
   - menu lateral em PT-BR;
   - página **Plugins** listando `SkyrimNet PT-BR`;
   - página **Personagens** com bios em português;
   - página **Prompts** com os templates em português;
   - **Configurações → Voz** com as opções em português.

## 3. Diálogo

1. Converse com um NPC conhecido (Hulda, Balgruuf, Lydia).
2. A fala deve sair em **português brasileiro**, não em inglês.
3. Confira se as ações (`ACTION:`) continuam funcionando.
4. Confira se o TTS fala em PT-BR (voz Kokoro `pf_dora`/`pm_alex`).

Se o NPC responder em inglês:

- verifique se é uma fala **vanilla** do jogo (crianças, guardas, saudações
  genéricas). Essas linhas não são geradas pelo LLM e continuam em inglês;
- para falas geradas, confirme que o plugin PT-BR está ativo e acima da base
  na Content Library;
- confira no log se `dialogue_response` e `player_dialogue` estão vindo da
  camada `julianu37.skyrimnet-ptbr`;
- o **Qwen2.5-3B-Instruct funciona**; não é necessário trocar para 7B;
- em último caso, comece uma conversa nova para descartar histórico antigo.

## 4. Conteúdo YAML

1. **Configurações → Filtros**: os nomes devem aparecer como
   “Animais não falam”, “Manequins não falam” etc.
2. **Configurações → Voz → Efeitos de Voz**: nomes como “Fantasma”,
   “Lobisomem”, “Senhor Vampiro”.
3. **Configurações → Ações de Diálogo**: listas “Controlador do Nether's
   Follower Framework” e “Definidor de estágio de missão”.

## 5. ESP (opcional)

Se você rodou `tools/patch_esp.py`:

1. Use o feitiço de telepatia.
2. A descrição deve estar em português (“Ouça os pensamentos...”).
3. Ao carregar um save antigo, a caixa de mensagem deve oferecer
   “Apagar dados”, “Manter dados” e “Voltar”.

## 6. Reversão

- **UI**: restaure `index.html.ptbr-original` na pasta `assets/web-new` do mod
  base e remova `main.*.ptbr.js`/`pt-br.js`.
- **ESP**: renomeie `SkyrimNet.esp.ptbr-original` de volta para
  `SkyrimNet.esp`.
- **Conteúdo**: desative o mod `SkyrimNet PT-BR` no MO2.
