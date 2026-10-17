# How To Use

## 1. Purpose

This Harness reduces irrelevant context, separates authority from derived records, and prevents repeated mistakes. Report conclusions and actual verification in the conversation; ordinary questions, read-only investigation, and simple fixes need no Harness record.

## 2. Rule Entry

The root `AGENTS.md` contains a bounded Harness integration block. It requires Codex to read and follow `.harness/AGENTS.md` before project work. Do not remove or partially edit either marker.

## 3. Project Map

Populate [HCA_PROJECT_MAP.md](HCA_PROJECT_MAP.md) only from real files and confirmed information:

- Resolve workspace and repository boundaries.
- Identify normative, implementation, verification, historical, and derived documents with their lifecycle and ownership.
- Index current module responsibility boundaries, direct dependencies, entry points, deeper documentation, and verification owners.
- Record dependency direction and verification routing.
- Mark unknown information explicitly.

The Project Map is a derived, non-normative locator. Do not store task status, completion history, incidents, commands, versions, hashes, or test evidence in it. Update it in the same change when documents move or module/ownership topology changes.

## 4. Start A Task

Use this compact recovery route:

```text
Read AGENTS.md, .harness/HCA_PROJECT_MAP.md, and .harness/ERROR_LEDGER.md. Read `.harness/TASK_STATUS.md` only when it exists for work that needs recovery.
Search active Error Ledger patterns and the catalog, then open only matching canonical entries. Do not preload every shard or unrelated project document.
Define acceptance criteria and classify the task. Lightweight work may be implemented directly and may omit independent Review; full-flow work uses a bounded implementation Subagent and independent read-only Review.
Make the smallest necessary in-scope change with no unrelated refactors or authority expansion, verify it through the owning route, and complete every gate required by the classification before advancing.
```

## 5. Task Classification And Review Gates

Classify each task before editing:

1. Use the lightweight flow for narrow, low-risk, reversible work with straightforward verification and no runtime behavior, architecture, normative product semantics, authority hierarchy, security, migration, destructive-state, release, or publication impact. Mechanical synchronization across copies may remain lightweight.
2. In the lightweight flow, the main Agent may implement directly and may omit independent Review. Delegation and Review are optional independently; make no unrelated refactors or authority expansion, and still verify the result.
3. Use the full flow when risk crosses those boundaries, the user requests it, or lightweight work expands or requires non-trivial rework.
4. In the full flow, delegate the smallest necessary implementation with no unrelated refactors or authority expansion to a bounded single-writer Subagent, verify it, and assign a different read-only Review Subagent.
5. Use at most two Review rounds by default. Round 1 covers the declared scope; round 2 covers only the blocker-fix delta, affected checks, and direct regression boundary.
6. Treat acceptance failures, correctness defects, out-of-scope changes, authority/ownership conflicts, security/data/destructive risks, missing required verification, and issues that make completion claims false as blocking. Report non-blocking suggestions in the conversation; do not fix or re-review them.
7. Require each Review to report its round, checked scope, blocking findings, non-blocking suggestions, evidence, conclusion, and remaining risk. Reject duplicate, unsupported, out-of-scope, and re-litigation findings with a recorded rationale.
8. Do not start an automatic third Review. After round 2, allow one scope-preserving deterministic small fix without another Review; otherwise report budget exhaustion and request user direction. Administrative recovery or evidence-link updates after Review do not consume a round.

Unavailable Subagents block only tasks whose classification requires them. The main Agent owns integration, and Reviewers never edit implementation or evidence. Explicit Review requests use the same two-round cap unless the user authorizes more.

## 6. Error Ledger Workflow

1. Search `.harness/error-ledger/PATTERNS.md` by failure class.
2. Search `.harness/error-ledger/CATALOG.md` by tool, path, module, symptom, or keyword.
3. Open only the linked canonical entry under `.harness/error-ledger/entries/`.
4. For an exact repeat, update the matching pattern only when it adds reusable prevention information; no new incident or task record is required.
5. For a distinct reusable failure, allocate `max(ERR) + 1`, append it to the correct fixed 25-ID shard, and add its catalog record.
6. Preserve removed IDs as permanent gaps. Never renumber or reuse them.

## 7. Daily Use

- Use [PROMPTS.md](PROMPTS.md) for new tasks, continuation, mistake handling, and review.
- Create or update one `TASK_STATUS.md` only when interruption, handoff, or cross-session recovery requires it. Include only goal, scope, key decisions, verified progress, blockers, and next step; overwrite it as work proceeds and delete it on completion.
- Use module-owned verification routes and inspect the actual output artifact.
- Keep Harness records concise and free of secrets, private data, chat history, and transient debug noise.

## 8. Lightweight Tasks

For a typo, one known field, local copy, or another narrow low-risk change, make the smallest necessary in-scope change with no unrelated refactors or authority expansion directly or through an optional Subagent, verify it, and report briefly. Do not create a Harness record by default. Independent Review is optional unless risk, scope growth, rework, or the user makes it required.
