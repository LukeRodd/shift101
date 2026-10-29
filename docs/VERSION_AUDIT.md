# Version compatibility audit — 2026-10-29

## Findings and remediation

| Item | Before | After | Reason |
| --- | --- | --- | --- |
| GitHub checkout | `actions/checkout@v4` | `@v7` | Node 20 action deprecation; Node 24 compatible release |
| GitHub setup Python | `actions/setup-python@v5` | `@v7` | Node 24 compatible release |
| AWS SAM setup | `aws-actions/setup-sam@v2` | `@v3` | Node 24 compatible release |
| Starlette tests | `httpx` only | `httpx2>=2.15,<3` in development requirements | Avoid deprecated Starlette TestClient transport |
| Python | 3.12 | 3.12 retained | Supported AWS Lambda runtime, validated by CI and SAM build |

The application keeps `httpx` as a runtime dependency for Ollama. `httpx2` is installed only for test client compatibility; it does not replace the runtime client.

## Validation evidence

- AI PR #1: **13 passed**, no Starlette/Node 20 deprecation warnings: https://github.com/LukeRodd/shift101/actions/runs/40930401819
- AWS PR #2: **18 passed**, `pip check` found no broken requirements: https://github.com/LukeRodd/shift101/actions/runs/40930447556
- AWS SAM: `sam validate --lint`, `sam build` and bundle inspection **succeeded** with Node 24 compatible Actions: https://github.com/LukeRodd/shift101/actions/runs/40930447602

## Out of scope

- No deployment to AWS, no runtime inference, and no additional spend.
- Dependency ranges remain broadly defined rather than locked to exact versions. Introduce a lockfile before production to improve reproducibility.
- Python 3.12 remains supported but does not have to be the newest runtime; upgrading Python should have its own compatibility checkpoint.

## Official references

- https://github.blog/changelog/2026-09-23-node-20-is-no-longer-available-in-github-actions/
- https://github.com/actions/checkout/releases
- https://github.com/actions/setup-python/releases
- https://github.com/aws-actions/setup-sam/releases
- https://starlette.dev/release-notes/
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html
