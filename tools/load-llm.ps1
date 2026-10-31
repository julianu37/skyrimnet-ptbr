# Load the local LLM with the context and parallelism required by SkyrimNet PT-BR.
# Run after restarting LM Studio, or use it as a desktop shortcut.
$lms = "$env:USERPROFILE\.lmstudio\bin\lms.exe"
& $lms unload qwen2.5-7b-instruct 2>$null
& $lms load qwen2.5-7b-instruct -c 32768 --parallel 1 --gpu max -y
& $lms ps
