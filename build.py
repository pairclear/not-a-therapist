#!/usr/bin/env python3
"""Build generated files from the sources. Run: python3 build.py

Sources:  prompts/*.md, tests/scenarios.json, data/crisis-resources.json, src/template.html
Outputs:  tests/scenarios.md, data/crisis-resources.md, index.html
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent


def code_block(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    m = re.search(r"```text\n(.*?)\n```", text, re.S)
    return m.group(1)


scen = json.loads((ROOT / "tests/scenarios.json").read_text(encoding="utf-8"))
crisis = json.loads((ROOT / "data/crisis-resources.json").read_text(encoding="utf-8"))

# tests/scenarios.md
out = ["# Test scenarios / Тестовые сценарии", "",
       "Generated from `scenarios.json` by `build.py`. All messages are invented. "
       "Paste each message into a fresh chat with your bot and compare the reply with the lists.", "",
       "Сгенерировано из `scenarios.json`. Все сообщения выдуманы. Вставьте каждое в новый чат с ботом и сверьте ответ со списками.", ""]
for i, s in enumerate(scen["scenarios"], 1):
    out += [f"## {i}. `{s['id']}` (rule {s['rule']})", "",
            f"> **EN:** {s['user']['en']}", ">",
            f"> **RU:** {s['user']['ru']}", "",
            "| | EN | RU |", "|---|---|---|"]
    for k, label in (("must", "Must"), ("must_not", "Must not")):
        en, ru = s[k]["en"], s[k]["ru"]
        for j in range(max(len(en), len(ru))):
            out.append(f"| {label if j == 0 else ''} | {en[j] if j < len(en) else ''} | {ru[j] if j < len(ru) else ''} |")
    out.append("")
(ROOT / "tests/scenarios.md").write_text("\n".join(out), encoding="utf-8")

# data/crisis-resources.md
out = ["# Crisis lines / Кризисные линии", "",
       f"Checked / проверено: **{crisis['checked']}**. Generated from `crisis-resources.json`.", "",
       crisis["note"], "", "| Country | Line | Number | Hours | Site |", "|---|---|---|---|---|"]
for g in crisis["global"]:
    out.append(f"| Global | {g['name']} | {g.get('phone', '')} | {g['hours']} | {g.get('url', '')} |")
for c in crisis["countries"]:
    for l in c["lines"]:
        num = l["phone"] + (f" ({l['short']})" if l.get("short") else "") + (f"; SMS: {l['sms']}" if l.get("sms") else "")
        out.append(f"| {c['country']} | {l['name']} | {num} | {l['hours']} | {l.get('url', '')} |")
out += ["", crisis["not_listed"], ""]
(ROOT / "data/crisis-resources.md").write_text("\n".join(out), encoding="utf-8")

# index.html
data = {
    "prompts": {
        "en": {"full": code_block("prompts/system-prompt-en.md"), "short": code_block("prompts/short-en.md")},
        "ru": {"full": code_block("prompts/system-prompt-ru.md"), "short": code_block("prompts/short-ru.md")},
    },
    "scenarios": scen["scenarios"],
    "crisis": crisis,
}
for lang in ("en", "ru"):
    n = len(data["prompts"][lang]["short"])
    assert n <= 1500, f"short-{lang} is {n} chars, over the 1500 limit"
tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
(ROOT / "index.html").write_text(tpl.replace("/*DATA*/null", payload), encoding="utf-8")
print("ok:", {l: len(data["prompts"][l]["short"]) for l in ("en", "ru")}, "short-prompt chars")
