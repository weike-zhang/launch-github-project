# Privacy, ownership and license

This reference supports risk identification, not legal advice.

## Public-data review

Check source, examples, screenshots, history, archives and generated outputs for:

- credentials and tokens;
- personal contact or identity data;
- customer or employee information;
- company code, internal documents or confidential roadmaps;
- exact infrastructure details that create unnecessary security exposure;
- copyrighted images, fonts, course materials, articles or datasets;
- model outputs whose source assets or terms are unclear.

If ownership or consent is uncertain, keep the asset local, replace it, or obtain permission. Do not infer permission from possession.

When permission is confirmed, replace provisional language with a final public notice that states provenance and reuse terms. Do not leave a public asset notice saying approval is still required, and do not publish rejected generation prompts unless they are necessary evidence for the shipped artifact.

## License selection

Ask about the intended reuse only when a license decision is required.

- MIT: permissive reuse with attribution and warranty disclaimer; common for code and Skills.
- Apache-2.0: permissive code license with an explicit patent grant.
- GPL-family: reciprocal code sharing; choose only when the author understands the effect.
- CC licenses: often better for documentation, courses, datasets or creative assets; choose the exact variant deliberately.
- No license: others generally do not receive permission to reuse; this is not the same as open source.

A repository may need different licenses or notices for code, documentation, data and visual assets. Record third-party notices when required.

## Safe reporting

Secret scanners should report a category, file and line number. Do not print the matched value. If a real secret entered Git history, removing it from the latest file is insufficient: revoke or rotate it and clean history with an appropriate, explicitly authorized procedure.
