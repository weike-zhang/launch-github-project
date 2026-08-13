# README patterns

## Build the reader's decision path

A README is not an inventory of project features. Help a new visitor answer these questions in order:

1. Is this meant for my situation, unmet need or goal?
2. What will become easier, safer or possible for me?
3. What concrete example or evidence supports that claim?
4. What is the smallest useful thing I can try?
5. Where can I inspect the method, limits and maintenance details?

Do not make readers understand the implementation before they can understand the value. For problem-solving projects, name a recognizable stalled state. For datasets, research, design resources and other artifacts, name the intended use or decision instead of inventing emotional pain.

When publishing in more than one language, share claims and evidence but rebuild the reader path in each language. Section-for-section translation often preserves foreign syntax, weakens the hook and makes one language feel secondary. For Chinese copy, use `chinese-public-copy.md` before the final cold-reader pass.

## Keep the current README synchronized

Re-read the existing README after implementation, not only before it. Check whether the change affects any of these public contracts:

- what the project does, who it is for or what appears in the first result;
- install, update, invocation, configuration or uninstall commands;
- screenshots, examples, inputs, outputs and linked evidence;
- permissions, data handling, security boundaries or known limits;
- supported hosts, platforms, versions and compatibility status;
- Release links, package names, repository layout and contribution paths;
- removed or renamed behavior that the README still teaches.

Use the existing README as the editing target. Update stale statements where they already live, then search the full document for older wording, commands and images that now conflict. Do not solve drift by adding a fresh “latest update” paragraph above stale instructions. If no README change is required, state the inspected change and why no reader-facing contract moved.

## First screen

Within the first screen, communicate:

- project name and one user-visible outcome;
- the intended user through a recognizable situation or goal;
- one concrete differentiator expressed as a consequence, not an internal mechanism;
- a compact example, output or visual when it adds proof;
- the shortest valid start action after the reader has a reason to care.

Badges are metadata, not a value proposition. Move them below the positioning copy when they compete with the message. For installable projects, keep one tested, copyable install command near the first useful example, but do not lead with installation before explaining why the project matters.

Treat the first screen as a composition, not a checklist. Choose one of two openings:

- **Visual opening:** place a project-owned hero, real output, before/after or compact product preview before long prose. Follow it with at most one outcome line and one compact row of navigation, proof or status links.
- **Text opening:** use the project name, one short outcome line, one recognizable situation and one proof or start link. Do not stack several explanatory paragraphs before the first example or visual.

Do not bury an existing hero below the introduction it was meant to replace. Do not add a decorative hero when real output or a compact text opening explains the project better. A hero with embedded text must remain legible at the rendered README width, use localized text for each public language, and have alt text that states the same outcome without relying on the image.

Before calling the README ready, render the exact opening at a normal desktop GitHub width and a narrow width. Capture or inspect the initial viewport without scrolling. Confirm that the visual hierarchy—not only the source order—makes the name or identity, outcome, differentiator and next action discoverable. Treat a Markdown source check as partial validation; after publication, repeat the check on the unsigned GitHub page.

## Translate from the inside out

Project authors naturally describe protocols, architecture and safeguards. A new user describes what they are trying to do and where they are stuck. Preserve the technical truth while translating the point of view.

| Internal or maintainer language | User-visible language |
| --- | --- |
| routes explanation, diagnosis and implementation | does not turn “help me understand” into an unrequested code change |
| grounds claims in authorized evidence | points to the file, log or page behind a project-specific statement |
| verifies prerequisite understanding | asks the learner to predict or safely observe once instead of assuming they understood |
| exports multiple artifact formats | gives the user the specific file they need to download or reuse |

Do not solve “AI-sounding” copy by swapping synonyms, adding casual filler or deleting every technical term. Rewrite the vantage point: lead with the reader's situation and observable result, then introduce the exact technical term when it helps verification or use.

Prefer concrete nouns and verbs over clusters such as “comprehensive,” “end-to-end,” “evidence-driven,” “empower” or “unlock.” These words are acceptable only when the next sentence shows what they mean. Keep paragraphs short enough to scan; one to three sentences is usually enough.

## Show proof a reader can interpret

Prefer proof in this order when available:

1. a real input and output;
2. a short, reproducible task;
3. a screenshot or visual with legible evidence;
4. an observed behavior comparison;
5. a feature or architecture description.

A before/after visual must name the same user task on both sides and show the observable difference. Do not fill comparison cards with labels such as “adaptive routing,” “complete system path” or “evidence state” unless the intended reader already uses those terms.

Keep limitations beside the claim they qualify, but do not make release-integrity caveats replace the value explanation. When evidence is weak, narrow the promise to the observed process or pilot behavior instead of implying adoption, reliability or long-term outcomes.

## Run a cold-reader check

Read the first screen without relying on repository history or implementation knowledge. Confirm that a target reader can answer:

- Who is this for?
- What situation or goal should they recognize?
- What changes when they use it?
- What concrete proof is visible?
- What should they try first?
- Is there one sentence they would naturally repeat or forward?

Rewrite when the answers require decoding internal terms, reading the architecture section or trusting unsupported praise. A structurally complete README can still fail this check.

Also fail the cold-reader check when the right facts exist but the initial viewport is dominated by undifferentiated prose, repeated titles or badge clutter while the useful visual, proof or first action sits below the fold.

### Separate comprehension from desire to try

Passing Humanizer or sounding natural answers only “does this read like a person wrote it?” Run a second gate for “why would the intended user try this now?” Do not accept a smooth sentence that merely lists internal actions.

Require the opening to connect three facts without turning them into a fixed slogan template:

- a problem, stalled state or goal the intended user already recognizes;
- the concrete first result they receive, such as a diagnosis, changed file, preview or usable artifact;
- a small, low-risk action that lets them see value before making a large commitment.

Run the **name-swap test**: replace the project name with an unrelated tool. If the outcome line still sounds equally plausible, it is a category description rather than this project's value proposition. Run the **method-removal test**: remove verbs such as audit, inspect, validate, orchestrate and optimize. If nothing user-visible remains, the copy explains how the project works but not what it solves.

For an Agent Skill, show what the first response or changed behavior looks like. “Checks the repository, validates claims and reviews the release” describes a workflow. “Returns the release blockers and the single issue most likely to stop first use before changing files” gives a reader a result worth trying. Keep the latter bounded by observed capability; do not invent urgency, savings or outcomes.

## Remove AI-shaped copy without removing the author's voice

Run this pass after claims and evidence are settled. Use `$humanizer` when it is installed; otherwise inspect the prose and every visible image string manually.

Rewrite clusters of these patterns:

- repeated `not X, but Y` or `不是……而是……` contrasts;
- forced groups of three used to make an ordinary claim sound complete;
- stacked short sentences that all try to land as a slogan;
- fake-candid hooks such as “别先听我吹” or “here's the real question”;
- compressed framework labels such as `AUDIT / PROVE / PACKAGE / VERIFY` when plain task names are clearer;
- abstract product nouns where a concrete action works better;
- bold slogans, centered taglines and headings that repeat the same promise.

Do not rewrite a single em dash, list or casual phrase in isolation. Preserve specific details, uneven but natural rhythm, real opinions, commands, links, numbers and explicit evidence limits. Humanizing copy never authorizes invented facts, urgency, testimonials or adoption claims.

Do not overcorrect into bland operational copy. Removing slogans, symmetry and hype is not permission to erase the product's pain, concrete result or point of difference. Run the desire-to-try gate again after Humanizer because a voice edit can accidentally flatten positioning.

## Common core

Select and order only the sections the reader needs:

1. Recognizable situation, need or goal.
2. User-visible outcome and concrete example.
3. Quick start or first useful task.
4. How it works or how content is organized.
5. Evidence and limitations.
6. Privacy, security, provenance and license.
7. Contribution and roadmap.

The order may vary when prerequisites require it, but maintainer detail should not displace user value from the opening.

## Type-specific sections

### Software or CLI

Requirements, install, command examples, real output, configuration, test, architecture only if useful, known limits, security.

### Agent Skill

The user's recognizable starting problem, what behavior changes, a real prompt and response excerpt, installation by host, when it triggers, permissions, evaluation, compatibility and limits. Describe Skill rules through their effect on the user's task before listing protocol steps.

### Dataset

Intended decisions or analyses, data card, schema, sample, collection or creation method, source and consent, splits, bias, license, citation.

### Course or documentation

Audience, current knowledge or goal, prerequisites, learning outcomes, navigation, exercises or evidence, how to study, maintenance and corrections.

### Research

Question, who can use the result and for what decision, method, environment, reproduction, results, uncertainty, limitations, citation.

### Design resource

Intended design task, preview, included source formats, compatible tools and versions, usage examples, editing rules, attribution and license.

### Content project

Audience need, scope, index, selection criteria, source and citation policy, update method, contribution.

### Portfolio

Problem context, users, personal responsibility, constraints, decisions, artifacts, outcomes, evidence boundaries and lessons.

## Claims

Prefer observed statements: “tested on macOS 15 with Codex” over “works everywhere.” Link each score or benchmark to its method and raw results. Remove decorative claims that cannot be checked.

Do not invent user pain, adoption, results or urgency. Do not expose internal launch-copy drafts, replacement instructions, generation prompts or unresolved rights decisions in user-facing README sections.
