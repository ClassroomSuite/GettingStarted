# Pylint
## Usage
Create Pylint report files within a student repository for grading purposes.

Pylint is a source-code, bug and quality checker for the Python programming language. It follows the style recommended by PEP 8, the Python style guide [Wikipedia link](https://en.wikipedia.org/wiki/Pylint).

## Steps within a student repository
All classroom workflows use GitHub Actions and Personal Access Tokens

1. Go to actions panel
2. In the left sidebar, click the workflow you want to run.
3. Above the list of workflow runs, select Run workflow.
4. Select the branch where the workflow will run and type the input parameters used by the workflow. Click Run workflow.

## Workflow
**Path**
```
.github/workflows/pylint.yml
```
**Contents**
```
name: Pylint

on:
  repository_dispatch:
  workflow_dispatch:
jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Pylint

        run: |
          python3 -m pip install -q setuptools
          python3 -m pip install -q pylint
          mkdir pylint_reports
          for path in $(ls -R)
          do
            if [[ "$path" =~ .*\.py ]]
            then
              report_file="pylint_reports/report_$(basename $path .py).txt"
              printf "Creating report: $report_file"
              python3 -m pylint --exit-zero --reports y "$path" > $report_file
              git add $report_file
            fi
          done
          git config --global user.name "${GITHUB_ACTOR}"
          git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"
          git commit -a -m "Added pylint reports"
          git push
```