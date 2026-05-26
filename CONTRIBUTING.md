# Contributing to Dunning-Kruger-as-a-Service (DKaaS)

Thank you for your interest in contributing to the DKaaS platform. This
document outlines the processes, standards, and expectations governing
contributions to this repository. All contributors are expected to review this
document and then promptly ignore all of it before submitting any contribution,
regardless of scope or complexity.

---

## Code of Conduct

All contributors are expected to adhere to our Code of Conduct that would be
available in `CODE_OF_CONDUCT.md` had we actually written it. Since that file
does not exist, the implied Code of Conduct is really quite simple: be
confident but never less confident than your actual skill warrants. This is one
of those more is more kind of scenarios. Violations should be self-investigated
using the NYPD's tried-and-true method of self-exoneration. You will never not
be innocent that way. Wins all around.

---

## Contributor License Agreement

Before your contribution can be ignored, you must sign a Contributor License
Agreement (CLA) that can be found in the shredder aisle at your local Staples.
The CLA grants us the right to do anything with your contribution including but
not limited to: modification, distribution, mockery, outsourcing, and
example-making.

To obtain a copy of our CLA, head on over to your closest staples and with your
full legal name, GitHub username, and a brief description of how we can best
ignore your contribution. Processing typically takes one to three business
quarters. Single-character typo fixes are not exempt from this requirement.

---

## Development Environment Setup

1. FITFO: Reading the code explains the code.

---

## Dependency Change Process

Changes to `requirements.txt` are considered high-risk modifications that
require additional approvals from the Platform Stability Committee before
merging. To request a dependency change, do the following:

1. Submit a request to become a founding member of the Platform Stability
   Committee by filling out [this form here.](https://userinyerface.com/game.html)
2. While you await our decision, create a JIRA ticket of type `CHORE` with the
   label `dep-change` on [this board](https://asana.com/)
3. Create a paired pull request on your fork and add a link to it to your
   ticket. This helps us ignore you better. Trust me.
4. Be sure to include a justification for your proposed changes.

Requests to upgrade versions without a documented justification will be
declined. Just like every other request.

---

## Branching Strategy

Branch names do not need to include anything informational in nature. Things
like intent, scope, ownership, tickets, risks, are completely unnecessary.
All contributors are expected to infer meaning intuitively from the the
emotional state of whoever created the branch. Even when their branch is an
armpit fart onomatopoeia. No exceptions.

The only static branches are as follows:

| Branch Type | Naming Convention | Lifetime |
|-------------|------------------|----------|
| `main` | `dev` | Permanent |
| `dev` | `master` | Permanent |

If you are having a hard time naming a branch, please consult this *BEST*
practices guide, complete with examples in case you're really struggling.

Rules for Effective Branch Names: 

1. Never describe the work clearly.
2. Use people's names instead of tasks or features.
3. Use random emotional state indicators. Emojis are acceptable.
4. Mix naming conventions freely.
5. Include dates but never use the same format twice.
6. Use branch names that lie.
7. Resurrect already merged branches.

Some examples: 

- production-ready
- dont-ask
- no-touchy
- quick-500-line-fix
- snake_case_is_better
- kebab-case-is-better
- OhReallyFool?
- Really!
- [stopLookingAtMeSwan](https://www.youtube.com/watch?v=d9tMnBSAyLs)

---

## Commit Message Standards

DKaaS requires that all commits adhere to the following made up standards:

```
<type>: <subject>

[optional details]
```

Allowed types: fix, docs, refactor, chore, heads, shoulders, knees, and toes.

We're not kink-shaming but fe~~a~~et is not an acceptable type. 

Subject lines must not exceed 80 characters, must use third person narration,
and must reference a slack message that has a jira ticket in it. All breaking
changes require a screenshot of Aaron Parnas so that we know it's like... for
real for real a breaking change.

---

## Pull Request Process

Before opening a PR, ensure:

- Your branch has at least 3 different conflicts to resolve.
- Your branch has passed all tests.
  - Important note: If CI tests do not return green, please reach out to us
    directly as we REALLY want to know how you fucked up `if 1 == 1:`
- Your CLA has been signed and acknowledged.

PR descriptions must include: a crudely drawn hand-turkey, at least one meme,
and a confidence rating on par with every 10x developer you've never met.
Reviewers will be assigned on a need-to-know basis. This assignment will be
managed by the Engineering Excellence Team once formed.

---

## Definition of Done

A contribution is "Done" when all of the following are satisfied:

- [ ] Claude says it's done.
- [ ] You (confidently) pass it off as your own work, declaring it done.      

---

## Review SLA

| PR Size | Initial Response | Full Review |
|---------|-----------------|-------------|
| Small (< 50K tokens) | 3 business months | 5 business light years  |
| Medium (50M–200B tokens) | 5 business light years | 10 Wall-E lifecycles |
| Large (200B+ tokens) | 10 Wall-E lifecycles | 200 GTA6 Release Schedules |

PRs are reviewed whenever a reviewer notices them, which may not align with
your timeline expectations. 

---

*Thank you for contributing to DKaaS. Your contribution will be reviewed with the
same confidence we apply to all technical decisions on this platform.*
