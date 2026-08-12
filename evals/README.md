# Evaluation

The fixtures cover software, Agent Skill, dataset, research, design-resource, portfolio and general projects. They are designed to expose the failure mode of applying one software template to every repository.

```bash
python evals/validate_fixtures.py
```

The command checks fixture balance, schema, type-route coverage, rubric weights and required release files. It reports checks passed, not a model-quality or popularity percentage.

Model comparisons must record model, client, date, prompt, complete sanitized output, method and limitations. One transparent pilot pair is published in [results/model-comparison.md](results/model-comparison.md). It is not a benchmark and does not predict stars, reach or adoption.
