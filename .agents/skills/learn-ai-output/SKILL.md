---
name: learn-ai-output
description: Convert work created or substantially modified by AI into a practical learning document that helps the user understand, explain, reproduce, and extend it independently. Use when the user asks to document what AI built, create a study guide or handover, explain generated code or artifacts for later learning, record decisions and concepts, produce a tutorial from completed work, or add exercises and self-check questions based on an AI-created result.
---

# Learn AI Output

Turn an AI-created artifact into a learning path grounded in the actual work. Optimize for transfer of understanding, not a chronological activity log.

## Workflow

1. Identify the artifact and the learner.
   - Inspect the relevant files, diff, conversation, commands, tests, or supplied output.
   - Infer the learner's level from context. State the assumption briefly when it affects depth.
   - Ask only when the target artifact or intended learner cannot be determined safely.

2. Establish evidence.
   - Separate facts observed in the artifact from explanations and reasonable inferences.
   - Cite repository files with paths and symbols or line numbers when useful.
   - Do not invent motivations, requirements, behavior, test results, or implementation details.
   - Mark gaps explicitly as `Chưa xác minh` and explain how to verify them.

3. Build the mental model before details.
   - Explain the problem, constraints, inputs, outputs, major components, and data/control flow.
   - Connect each important implementation choice to the concept it demonstrates.
   - Explain trade-offs and rejected alternatives only when supported by evidence or clearly labeled as analysis.

4. Teach reconstruction.
   - Break the work into small stages the learner could repeat from a blank state.
   - For every stage, include the intent, action, expected result, and a concrete verification.
   - Use minimal excerpts instead of copying large source files.
   - Include common mistakes that are plausible for this exact artifact.

5. Add active recall.
   - Provide questions whose answers are available from the document or artifact.
   - Add at least one modification exercise and one debugging or diagnosis exercise when applicable.
   - Put model answers in a collapsible `<details>` section so the learner can attempt first.

6. Verify the document.
   - Check technical claims against the source artifact.
   - Ensure commands, paths, identifiers, and expected outputs are current.
   - Confirm a learner can answer: what it does, how it works, why it is shaped this way, how to reproduce it, and how to verify it.

## Output Contract

Use Vietnamese unless the user requests another language. Keep technical identifiers in their original form and explain jargon at first use.

Use [assets/learning-document-template.md](assets/learning-document-template.md) as the default structure. Adapt or omit sections that do not fit the artifact; never fill sections with generic padding.

When the user does not specify a destination:

- Return the learning document in the response for explanation-only requests.
- For repository documentation requests, create `docs/learning/<topic>.md`, choosing a short lowercase hyphenated topic.
- Do not modify the original artifact unless explicitly asked.

Prefer diagrams only when relationships or flow are materially clearer than prose. Use Mermaid only when the repository's documentation renderer supports it; otherwise use a compact text diagram.

## Quality Bar

A strong document must be:

- Grounded: traceable to the actual artifact.
- Teachable: progresses from mental model to implementation.
- Reproducible: includes ordered steps and checks.
- Honest: distinguishes verified facts, inference, and unknowns.
- Active: requires the learner to recall, modify, and diagnose.
- Maintainable: points to source locations rather than duplicating whole files.
