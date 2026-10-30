"""Local coherence benchmark for the PT-BR content pack.

Runs the translated NPC bios against a local LM Studio OpenAI-compatible
endpoint (default: Qwen2.5-3B-Instruct) and writes a Markdown + JSON report.

Usage:
    python benchmarks/lmstudio_qwen.py
    python benchmarks/lmstudio_qwen.py --model qwen2.5-3b-instruct --limit 6
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts" / "characters"
RESULTS = ROOT / "benchmarks" / "results"

BLOCK_RE = re.compile(r"{%\s*block\s+(\w+)\s*%}(.*?){%\s*endblock\s*%}", re.S)
JINJA_RE = re.compile(r"{%.*?%}|{{.*?}}", re.S)

SCENARIOS = [
    {
        "file": "hulda_66E.prompt",
        "name": "Hulda",
        "user": "Um viajante cansado entra na The Bannered Mare e pergunta se há rumores interessantes em Whiterun.",
        "keywords": ["rumor", "whiterun", "taverna", "quarto", "hóspede"],
    },
    {
        "file": "balgruuf_the_greater_677.prompt",
        "name": "Jarl Balgruuf",
        "user": "Um mensageiro imperial exige que Whiterun se junte imediatamente à Legião Imperial.",
        "keywords": ["whiterun", "império", "legião", "guerra", "povo"],
    },
    {
        "file": "maven_black-briar_DD1.prompt",
        "name": "Maven Black-Briar",
        "user": "Um mercador se recusa a pagar a taxa da Black-Briar e diz que não tem medo de você.",
        "keywords": ["black-briar", "riften", "pagar", "negócio", "consequência"],
    },
    {
        "file": "jarl_ulfric_stormcloak_131.prompt",
        "name": "Jarl Ulfric Stormcloak",
        "user": "Um recruta pergunta por que deve lutar contra o Império.",
        "keywords": ["skyrim", "império", "talos", "liberdade", "stormcloak"],
    },
    {
        "file": "farengar_secret-fire_67E.prompt",
        "name": "Farengar Secret-Fire",
        "user": "Um aprendiz pergunta o que você descobriu sobre os dragões e a Pedra do Dragão.",
        "keywords": ["dragão", "pedra do dragão", "pesquisa", "bleak falls barrow"],
    },
    {
        "file": "lydia_C94.prompt",
        "name": "Lydia",
        "user": "O Thane entra em uma caverna perigosa sem avisar e manda você ficar para trás.",
        "keywords": ["thane", "proteger", "perigo", "juramento", "seguir"],
    },
    {
        "file": "belethor_672.prompt",
        "name": "Belethor",
        "user": "Um cliente tenta pechinchar uma espada enferrujada e diz que não vale nem dez septins.",
        "keywords": ["ouro", "preço", "oferta", "mercadoria", "septim"],
    },
    {
        "file": "aela_the_huntress_697.prompt",
        "name": "Aela, a Caçadora",
        "user": "Um caçador novato se gaba de ter matado um lobo sozinho.",
        "keywords": ["caça", "lobo", "companions", "força", "prova"],
    },
    {
        "file": "brynjolf_545.prompt",
        "name": "Brynjolf",
        "user": "Um jovem pobre pergunta como ganhar dinheiro rápido em Riften.",
        "keywords": ["ouro", "oportunidade", "guilda", "riften", "talento"],
    },
    {
        "file": "elisif_the_fair_8C1.prompt",
        "name": "Jarl Elisif",
        "user": "Um cidadão reclama que a corte não faz nada sobre os Stormcloaks.",
        "keywords": ["corte", "povo", "guerra", "solitude", "stormcloak"],
    },
    {
        "file": "carlotta_valentia_675.prompt",
        "name": "Carlotta Valentia",
        "user": "Mikael faz mais uma proposta indesejada na frente da sua filha Mila.",
        "keywords": ["mikael", "filha", "respeito", "mercado", "mila"],
    },
    {
        "file": "nazeem_6A4.prompt",
        "name": "Nazeem",
        "user": "Um camponês diz que o Distrito das Nuvens não é grande coisa.",
        "keywords": ["distrito das nuvens", "jarl", "status", "camponês", "whiterun"],
    },
]

PT_WORDS = {
    "você", "não", "sim", "que", "para", "com", "uma", "um", "seu", "sua",
    "meu", "minha", "aqui", "isso", "mas", "como", "porque", "está", "sou",
    "vou", "tem", "fazer", "mais", "muito", "bem", "taverna", "cidade",
    "dragão", "ouro", "guerra", "pagar", "povo", "corte", "filha", "medo",
}
EN_WORDS = {
    "the", "and", "you", "your", "is", "are", "to", "of", "in", "that",
    "with", "this", "it", "as", "be", "on", "for", "not", "have", "will",
    "but", "they", "we", "he", "she", "his", "her", "their",
}


def blocks(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    found = {}
    for name, body in BLOCK_RE.findall(text):
        clean = JINJA_RE.sub(" ", body)
        clean = re.sub(r"\s+", " ", clean).strip()
        if clean:
            found[name] = clean
    return found


def build_system(name: str, bio: dict[str, str]) -> str:
    parts = [
        f"Você é {name}, um personagem de Skyrim.",
        f"Responda apenas como {name}, em primeira pessoa, com 1 a 3 frases.",
        "Não narre ações de outros personagens. Não escreva descrições fora da fala.",
        "Responda sempre em português brasileiro. Nunca responda em inglês.",
    ]
    for key, label in (
        ("summary", "Resumo"),
        ("personality", "Personalidade"),
        ("speech_style", "Estilo de fala"),
    ):
        if key in bio:
            parts.append(f"{label}: {bio[key]}")
    return "\n".join(parts)


def post_json(url: str, payload: dict, timeout: int = 180) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def language_check(text: str) -> dict:
    words = re.findall(r"[A-Za-zÀ-ÿ']+", text.lower())
    pt = sum(1 for word in words if word in PT_WORDS)
    en = sum(1 for word in words if word in EN_WORDS)
    ratio = pt / (pt + en) if (pt + en) else 0.0
    return {"pt_hits": pt, "en_hits": en, "pt_ratio": round(ratio, 2), "ok": en < 2 or ratio >= 0.8}


def run(args: argparse.Namespace) -> int:
    base = args.url.rstrip("/")
    try:
        models = json.loads(urllib.request.urlopen(base + "/models", timeout=10).read())
        available = [item["id"] for item in models.get("data", [])]
    except Exception as exc:
        print(f"LM Studio API unavailable at {base}: {exc}", file=sys.stderr)
        return 2

    model = args.model or next(
        (m for m in available if "qwen2.5-3b-instruct" in m.lower()), None
    )
    if not model:
        print(f"model not loaded. available: {available}", file=sys.stderr)
        return 2
    if model not in available:
        print(f"model {model!r} not in {available}", file=sys.stderr)
        return 2

    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    scenarios = SCENARIOS[: args.limit] if args.limit else SCENARIOS
    records = []

    for index, scenario in enumerate(scenarios, 1):
        path = PROMPTS / scenario["file"]
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            continue
        bio = blocks(path)
        system = build_system(scenario["name"], bio)
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": scenario["user"]},
            ],
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "top_p": 0.9,
        }
        started = time.perf_counter()
        try:
            response = post_json(base + "/chat/completions", payload, args.timeout)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            print(f"[{index}] HTTP {exc.code}: {body[:300]}", file=sys.stderr)
            continue
        elapsed = time.perf_counter() - started
        choice = response["choices"][0]["message"]["content"].strip()
        usage = response.get("usage", {})
        completion_tokens = usage.get("completion_tokens") or 0
        tps = completion_tokens / elapsed if elapsed else 0
        lang = language_check(choice)
        lowered = choice.lower()
        hits = [keyword for keyword in scenario["keywords"] if keyword in lowered]

        record = {
            "file": scenario["file"],
            "name": scenario["name"],
            "user": scenario["user"],
            "response": choice,
            "elapsed_s": round(elapsed, 2),
            "completion_tokens": completion_tokens,
            "tokens_per_s": round(tps, 2),
            "language": lang,
            "keyword_hits": hits,
            "keyword_total": len(scenario["keywords"]),
        }
        records.append(record)
        print(
            f"[{index}/{len(scenarios)}] {scenario['name']}: {elapsed:.2f}s, "
            f"{tps:.1f} tok/s, pt_ratio={lang['pt_ratio']}, "
            f"keywords={len(hits)}/{len(scenario['keywords'])}"
        )
        print(f"  {choice}\n")

    if not records:
        print("no successful responses", file=sys.stderr)
        return 1

    json_path = RESULTS / f"qwen25-3b-{stamp}.json"
    md_path = RESULTS / f"qwen25-3b-{stamp}.md"
    json_path.write_text(
        json.dumps(
            {
                "model": model,
                "endpoint": base,
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "records": records,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    avg_latency = sum(r["elapsed_s"] for r in records) / len(records)
    avg_tps = sum(r["tokens_per_s"] for r in records) / len(records)
    pt_ok = sum(1 for r in records if r["language"]["ok"])
    keyword_ok = sum(1 for r in records if r["keyword_hits"])

    lines = [
        "# Benchmark local — Qwen2.5-3B-Instruct (LM Studio)",
        "",
        f"- Endpoint: `{base}`",
        f"- Modelo: `{model}`",
        f"- Temperatura: {args.temperature} | max_tokens: {args.max_tokens}",
        f"- Data (UTC): {stamp}",
        f"- Cenários: {len(records)}",
        "",
        "## Resumo",
        "",
        f"- Latência média: **{avg_latency:.2f}s**",
        f"- Velocidade média: **{avg_tps:.1f} tok/s**",
        f"- Idioma PT-BR OK: **{pt_ok}/{len(records)}**",
        f"- Palavras-chave de coerência encontradas: **{keyword_ok}/{len(records)}**",
        "",
        "## Respostas",
        "",
        "| NPC | Tempo | tok/s | PT | Keywords | Resposta |",
        "|---|---:|---:|---|---|---|",
    ]
    for r in records:
        response = r["response"].replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {r['name']} | {r['elapsed_s']}s | {r['tokens_per_s']} | "
            f"{'ok' if r['language']['ok'] else 'verificar'} | "
            f"{len(r['keyword_hits'])}/{r['keyword_total']} | {response} |"
        )
    lines += [
        "",
        "## Observações",
        "",
        "- Métricas automáticas de idioma e palavras-chave são heurísticas; a",
        "  coerência fina (tom, lore, consistência com a bio) foi revisada manualmente.",
        "- O benchmark usa a bio traduzida + instrução de idioma, não o pipeline",
        "  completo do SkyrimNet (que inclui memória, eventos e ações).",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report: {md_path}")
    print(f"json  : {json_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:1234/v1")
    parser.add_argument("--model", default=None)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=180)
    parser.add_argument("--timeout", type=int, default=180)
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
