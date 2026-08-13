# Pilot comparison: goal-driven distribution

Status: **one transparent pilot pair; not a benchmark**.

- Date: 2026-08-12
- Model: `gpt-5.6-sol`
- Client: Codex CLI `0.147.0-alpha.6.5`
- Scenario: one portfolio case, one LinkedIn account and a goal of three high-quality feedback responses without a day-by-day calendar
- Conditions: read-only and ephemeral; the baseline did not read the Skill, while the treatment read `SKILL.md` and `distribution-playbook.md`

## Exact prompt

```text
I have one portfolio case and one LinkedIn account. My goal is to receive three
high-quality feedback responses from people who could hire me or refer my work.
Propose a goal-driven distribution plan. Do not use a day-by-day calendar.
Work read-only and do not post or contact anyone.
```

## Published outputs

- [Baseline response](pilot/baseline-distribution.md)
- [Response with Launch GitHub Project](pilot/with-skill-distribution.md)

## What was observed

Both answers avoided a fixed calendar and vanity metrics. The narrower observed difference was sequencing: the baseline proposed a public post and direct messages together; the Skill used the existing case as evidence, direct messages as the primary path and a public post only if the first path did not yield enough qualified feedback.

One pair cannot predict launch reach, GitHub stars, adoption or reliability across project types. Future comparisons should repeat all scenario routes, publish sanitized failures and report behavior dimensions without turning fixture integrity into a product score.
