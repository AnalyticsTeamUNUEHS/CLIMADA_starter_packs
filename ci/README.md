# CI Notebook Testing

This folder contains configuration for automated notebook execution checks in GitHub Actions.

## What this CI does

The workflow at [.github/workflows/notebook-ci.yml](../.github/workflows/notebook-ci.yml) runs notebook tests when:

- Code is pushed to the main branch.
- A pull request targets the main branch.
- A run is started manually from the Actions tab.

It executes [test_build.sh](../test_build.sh), which runs all notebooks in starter pack notebook folders and fails the job if any notebook fails.

The workflow has two lanes:

- Fast lane (push to main): Python 3.11 + CLIMADA 6.1.* on Ubuntu and Windows.
- Full lane (pull requests and manual runs): Python 3.11 and 3.12 with CLIMADA 6.1.* and 5.* on Ubuntu and Windows.

## Operating systems covered

The workflow runs in a matrix on:

- ubuntu-latest
- windows-latest

## Where results are stored

The workflow uploads executed notebook outputs from build/test_notebooks as GitHub Actions artifacts.

To access them:

1. Open your repository on GitHub.
2. Go to Actions.
3. Open a specific run of Notebook CI.
4. In the run summary, find Artifacts.
5. Download the artifacts for the lane and matrix combination you want.

Artifact naming:

- Fast lane: executed-notebooks-fast-<os>-py<python>-climada<major_minor>
- Full lane: executed-notebooks-full-<os>-py<python>-climada<major_minor>

## Caching behavior

The workflow uses micromamba with environment and package download caching.

For each job, the workflow generates a temporary environment file from matrix values (Python and CLIMADA version).

- First run on each OS is usually slower because the environment is created.
- Later runs are faster when the same OS + Python + CLIMADA combination is reused.
- Changing matrix versions or package definitions causes that combination to rebuild.

## Notes

- Concurrency cancellation is enabled in the workflow to cancel older in-progress runs for the same branch when a newer run starts.
