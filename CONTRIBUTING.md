# Contributing to Dunning-Kruger-as-a-Service (DKaaS)

Thank you for your interest in contributing to the DKaaS platform. This document
outlines the processes, standards, and expectations governing contributions to this
repository. All contributors are expected to review this document in its entirety
before submitting any contribution, regardless of scope or complexity.

---

## Code of Conduct

All contributors are expected to adhere to our Code of Conduct, available in
`CODE_OF_CONDUCT.md`. If that file does not exist, the implied Code of Conduct is:
be professional, be respectful, and be confident — but not more confident than your
demonstrated knowledge warrants. Violations should be reported to conduct@dkaas.io.

---

## Contributor License Agreement

Before your contribution can be accepted, you must sign a Contributor License Agreement
(CLA). The CLA grants the DKaaS project the right to use, modify, distribute, and
sublicense your contribution under the project's license terms.

To obtain the CLA, email legal@dkaas.io with your full name, GitHub username, and a
brief description of your intended contribution. Processing typically takes one to three
business quarters. Single-character typo fixes are not exempt from this requirement.

---

## Development Environment Setup

1. Fork the repository and clone your fork
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (do not modify versions)
4. Copy `.env.example` to `.env` and populate with your credentials
5. Verify setup: `uvicorn app.main:app` and confirm `http://localhost:8000/docs` loads

### Dependency Change Process

Changes to `requirements.txt` are considered high-risk modifications and require
an additional approval from the Platform Stability Committee before merging. To
request a dependency change:

1. Create a JIRA ticket of type `CHORE` with the label `dep-change`
2. Document the current pinned version, the proposed version, and the reason
3. Provide evidence that the new version does not introduce breaking changes,
   regressions, or incompatibilities with the remaining pinned versions
4. Include a note explaining why the current version is insufficient

Requests to upgrade versions without a documented justification will be declined.
The current pins represent a known-stable configuration and stability is preferred
over currency.

---

## Branching Strategy

DKaaS follows a GitFlow-adjacent branching model with the following conventions:

| Branch Type | Naming Convention | Lifetime |
|-------------|------------------|----------|
| `main` | `main` | Permanent |
| `develop` | `develop` | Permanent |
| Feature | `feature/DKAAS-{ticket}-{description}` | Until merge |
| Bugfix | `bugfix/DKAAS-{ticket}-{description}` | Until merge |
| Hotfix | `hotfix/DKAAS-{ticket}-{description}` | Until merge |

All branch names must be lowercase with hyphens as separators. The `main` and
`develop` branches are protected and require at least one approved review before
merging. Direct pushes are not permitted except by repository administrators in
emergencies, which are broadly defined.

---

## Commit Message Standards

DKaaS follows the Conventional Commits specification. Format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer: Refs: DKAAS-{ticket}]
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`.

Subject lines must not exceed 72 characters, must use the imperative mood, and must
reference a JIRA ticket in the footer. Breaking changes require a `BREAKING CHANGE:`
footer annotation.

---

## Pull Request Process

Before opening a PR, ensure:

1. Your branch is up to date with `develop`
2. You have manually verified all affected endpoints
3. Your CLA has been signed and acknowledged
4. Documentation is updated if public-facing behavior changed

PR descriptions must include: a summary, a list of specific changes, a description
of testing performed, and a JIRA ticket reference. Reviewer assignment is managed
by the Engineering Excellence Team on a rotating basis. Unsolicited assignments
are considered a minor breach of contribution etiquette.

---

## Definition of Done

A contribution is "Done" when all of the following are satisfied:

- [ ] Functionality implements the specified ticket acceptance criteria
- [ ] All endpoints return HTTP 200 for valid requests
- [ ] `docker build -t dkaas .` completes successfully
- [ ] `docker run` starts the service and `/docs` is accessible
- [ ] All `confidence_score` fields in responses remain ≥ 0.99
- [ ] The `prompt_used` field in `/advise` contains the verbatim system prompt
- [ ] PR has received at least one maintainer approval
- [ ] CLA is on file for all authors
- [ ] No credentials or secrets are present in the diff

---

## Review SLA

| PR Size | Initial Response | Full Review |
|---------|-----------------|-------------|
| Small (< 50 lines) | 3 business days | 5 business days |
| Medium (50–200 lines) | 5 business days | 10 business days |
| Large (200+ lines) | 1 business week | 3 business weeks |

Review SLA timers begin when the PR is marked "Ready for Review." PRs in Draft
status are reviewed when a reviewer notices them, which may not align with your
timeline expectations.

---

*Thank you for contributing to DKaaS. Your contribution will be reviewed with the
same confidence we apply to all technical decisions on this platform.*
