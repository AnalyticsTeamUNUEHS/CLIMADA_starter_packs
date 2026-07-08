# CI Notebook Testing

This folder contains configuration for automated notebook execution checks in GitHub Actions.

## What this CI does

The workflow at [.github/workflows/notebook-ci.yml](../.github/workflows/notebook-ci.yml) runs notebook tests when:

- Code is pushed to the main branch.
- Code is pushed to the climada601 branch.
- Code is pushed to the climada5 branch.
- A pull request targets the main branch.
- A run is started manually from the Actions tab.

It executes [test_build.sh](../test_build.sh), which runs all notebooks in starter pack notebook folders and fails the job if any notebook fails.

## Job behavior by branch/event

- `main` job runs for:
	- Push to `main`
	- Pull requests targeting `main`
	- Manual dispatch (`workflow_dispatch`)

- `climada601` job runs only for:
	- Push to `climada601`

- `climada5` job runs only for:
	- Push to `climada5`

## Version matrix

- `main`:
	- OS: `ubuntu-latest`, `windows-latest`
	- Python: `3.10`, `3.11`, `3.12`
	- CLIMADA: `6.1.0`

- `climada601`:
	- OS: `ubuntu-latest`, `windows-latest`
	- Python: `3.10`, `3.11`, `3.12`
	- CLIMADA: `6.0.1`

- `climada5`:
	- OS: `ubuntu-latest`, `windows-latest`
	- Python: `3.10`, `3.11`
	- CLIMADA: `5.0.0`


## Where results are stored

The workflow uploads executed notebook outputs from build/test_notebooks as GitHub Actions artifacts.

To access them:

1. Open your repository on GitHub.
2. Go to Actions.
3. Open a specific run of Notebook CI.
4. In the run summary, find Artifacts.
5. Download the artifacts for the lane and matrix combination you want.

Artifact naming follows the convention: `executed-notebooks-<branch>-<os>-py<python>-climada<spec>`


## Runtime settings

All jobs execute notebooks with the same environment variables:

- `MODE=0`
- `EXECUTION_TIMEOUT=7200`
- `FAIL_FAST=1`

Each job creates `ci/environment.generated.yml` from its matrix values, then runs:

- `micromamba run -n starter-packs-ci bash -lc 'chmod +x ./test_build.sh && ./test_build.sh'`

## Caching behavior

The workflow uses micromamba with environment and package download caching.

For each job, the workflow generates a temporary environment file from matrix values (Python and CLIMADA version).

- First run on each OS is usually slower because the environment is created.
- Later runs are faster when the same OS + Python + CLIMADA combination is reused.
- Changing matrix versions or package definitions causes that combination to rebuild.

## Notes

- Concurrency cancellation is enabled in the workflow to cancel older in-progress runs for the same branch when a newer run starts.
