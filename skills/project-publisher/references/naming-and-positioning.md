# Naming and positioning

Use this reference before proposing a project name, renaming a repository, or writing the first public description.

## Name the durable role, not the first demo

A project name should describe the role or outcome that remains true across its useful life. Do not name it after:

- the first prompt shown in a README;
- one example, platform or output format;
- a single release stage when the product also audits, revises, distributes or maintains;
- an implementation detail that users must understand before they can value the project.

Keep four layers separate:

1. **Identity:** the short name people remember.
2. **Promise:** the one-sentence user outcome below the name.
3. **Capabilities:** the concrete jobs and lifecycle stages the project supports.
4. **Evidence:** examples, screenshots, failures caught and verified results.

The name does not need to carry all four layers. Put the missing precision in the repository description and README opening.

## Candidate tests

Prefer familiar words and natural word order. Score candidates with these questions instead of copying the surface style of popular repositories:

- **Speech:** Would the intended user naturally say or recommend this name aloud?
- **Guess:** Can a new reader roughly infer what kind of thing it is?
- **Scope:** Does it describe the real core without promising unsupported domains or outcomes?
- **Growth:** Will it still fit the next obvious stages of the product?
- **Collision:** Is the repository slug reasonably searchable and distinguishable?

Reject a candidate when it wins only by being shorter. Reject it when the README must immediately explain why the literal name is misleading.

For English names, check modifier order with the intended meaning. `Grounded AI Tutor` means a grounded tutor powered by AI; `AI Grounded Tutor` sounds like a tutor grounded by AI and is less natural. Use lowercase kebab-case for the Skill ID and repository slug: `grounded-ai-tutor`.

## Match the name to observed product truth

Inspect the current project before naming it. A broad name is not permission to claim broad support. If a tutor is verified only for computing, software, cloud and AI, keep that scope explicit even when the short name does not list every subject.

Likewise, do not let one useful example become the identity. A login-flow explanation may prove how a tutor works, but it is not the tutor's core. A GitHub Release may be one output of a project publisher, but publication also includes project review, positioning, materials, distribution and later updates.

Examples from this project's own rename:

- `Launch GitHub Project` described one platform and one moment. `Project Publisher` names the continuing role across audit, preparation, release, promotion and maintenance.
- `Grounded AI Mentor` left the teaching role less immediate. `Grounded AI Tutor` makes the role familiar while `grounded` preserves the method: start from what the learner already knows and use real project evidence when it helps.
- Candidates such as `Release Prep` or `How It Runs` were rejected because they named a stage or an example rather than the durable product.

## Plan the rename as a release

Before changing identifiers, inspect current adoption and compatibility obligations. Record:

- public repository name and description;
- Skill or package ID, plugin metadata and install commands;
- local state paths, hooks, lock files and generated assets;
- README links, Release specs, tests and CI;
- redirects, aliases or migration notes needed for existing users;
- the remote rename, push and publication actions that still require authorization.

If there are no known installs or compatibility users, prefer one clean identifier rather than carrying a permanent alias. Keep historical Release records accurate, and describe the rename in a new version instead of rewriting published history.

After editing, search for the old identifier. Classify every remaining occurrence as historical evidence, an intentional migration alias or a missed current surface. Validate the current name, slug, promise and install path together.
