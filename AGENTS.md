# AGENTS.md: building a bot that talks about personal topics

Instructions for coding agents (Codex, Claude Code, Cursor, Copilot and others) working on a chatbot, companion app, coaching tool or support widget where users may bring personal or emotional problems.

## When you write or change the bot's system prompt

- Include the rules from `prompts/system-prompt-en.md` (or `-ru.md`) in full, or keep every numbered rule if you shorten them. Do not drop rule 1 (safety) to save tokens.
- Put the safety rule first in the prompt. Models follow early rules more reliably.
- Replace the crisis numbers with ones for your users' countries. Take them from `data/crisis-resources.json` and re-check them on the operator's site. Never invent a phone number; if you are not sure, use `https://findahelpline.com` and the local emergency number.

## When you write code around the model

- Do not log or send users' message text to analytics. If logs are required, keep them minimal, access-controlled and with a short retention period, and say so in the privacy policy.
- Do not add features that let one person monitor another (reading messages, location tracking).
- If you add a "crisis" detector, use it only to show help resources sooner. Do not use it to auto-block the user, and do not rely on it instead of the prompt rules.
- Show a short disclaimer in the UI: the bot is an AI, not a therapist, and is not for emergencies.

## Before you call the work done

- Run each scenario in `tests/scenarios.json` against the bot and compare with its `must` and `must_not` lists. Report which ones fail. A failure on any scenario with `"rule": 1` blocks release.

## Things you must not do

- Do not write marketing copy claiming the bot "treats", "cures", "replaces therapy" or is "clinically proven" unless a cited source supports it.
- Do not put a real psychologist's name on the bot without their written consent.
