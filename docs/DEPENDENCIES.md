# Dependency management — Shift101 (Python 3.12)

This repository uses **two fully pinned dependency lock files**. The application and its Docker/AWS Lambda builds consume the same production lock.

| File | Purpose |
| --- | --- |
| `requirements.in` | Direct production dependencies; edit this file to add/change runtime packages. |
| `requirements-dev.in` | Direct test/development dependencies and the production input. |
| `requirements.txt` | **Production lock** (25 direct + transitive packages pinned with `==`); used by Docker and AWS SAM. |
| `requirements-dev.txt` | **Development lock** (33 direct + transitive packages pinned with `==`); used by GitHub Actions and local tests. |

## Install

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
python -m pytest -q
```

For runtime-only installations use `python -m pip install -r requirements.txt`.

## Update a dependency intentionally

1. Edit `requirements.in` or `requirements-dev.in` only, as appropriate.
2. Use **Python 3.12** and the pinned resolver **uv 0.10.0**.
3. Recompile both locks and review the changes:

```bash
python -m pip install uv==0.10.0

uv pip compile requirements.in \
  --python-version 3.12 \
  --exclude-newer '2026-10-29T18:00:00Z' \
  --output-file requirements.txt

uv pip compile requirements-dev.in \
  --python-version 3.12 \
  --exclude-newer '2026-10-29T18:00:00Z' \
  --constraint requirements.txt \
  --output-file requirements-dev.txt

python -m pip install -r requirements-dev.txt
python -m pip check
python -m pytest -q
```

The cutoff above is **intentional**: it prevents new upstream releases from silently changing a future resolution. To take security updates or newer packages, explicitly advance the cutoff in the commands **and** in `.github/workflows/generate-lockfiles.yml`, regenerate, and review the diff in a dedicated pull request.

## CI gate

`Generate Python dependency locks` regenerates both lock files from the inputs using uv 0.10.0 / Python 3.12 and runs `git diff --exit-code`. A mismatch fails CI. The normal CI installs `requirements-dev.txt` and runs tests, and AWS SAM builds the Lambda using the pinned `requirements.txt`. There is **no automated update or deployment**.

**Limitations:** pins protect against unreviewed version drift but are not artifact hashes. Full byte-level reproducibility would require `--generate-hashes` plus controlled platform/base-image tags; Docker's `python:3.12-slim` tag and AWS's Python 3.12 patch runtime can receive platform/security updates. The project currently targets Linux x86_64 / Python 3.12 in CI and Lambda.
