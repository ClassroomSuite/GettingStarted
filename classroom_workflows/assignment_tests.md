# Assignment autograding
## Usage
Run grading test files within all student repositories for a given assignment.
* Show test results in log files and README.md

**Important**:
* Verify that this worflows is specified in: **settings/files_to_update.txt**
    ```
    .github/workflows/assignment_tests.yml
    ```
* Only add the **test file** in the template repository after the deadline to prevent students from having access
    * [update student workflows](update_student_repositories.md) afterwards

## Steps to run within a student repository
All classroom workflows use GitHub Actions and Personal Access Tokens

1. Go to actions panel
2. In the left sidebar, click the workflow you want to run.
3. Above the list of workflow runs, select Run workflow.
4. Select the branch where the workflow will run and type the input parameters used by the workflow. Click Run workflow.

## Steps to run in all student repositories
1. Add the workflow path in **settings/files_to_update.txt**
    * View [update student repositories workflow](update_student_repositories.md)
2. Add repository_dispatch trigger event in workflow file
    ```
        on:
          repository_dispatch:
    ```
3. (optinal) [Update student repositories](update_student_repositories.md)
4. Create a repository dispatch event with either:
    * [assignment grading](assignment_grading.md)
    * [trigger students workflows](trigger_students_workflows.md)
## Troubleshooting
 * Verify that the repository has access to the required [GitHub Secrets](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)
 * Validate the values set in **settings/variables.txt**
     

## Workflow
**Path**
```
.github/workflows/assignment_tests.yml
```
**Contents**
```
# This workflow is intended for student repositories
name: Run assignment tests

on:
  repository_dispatch:
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          function run_tests() {
            python3 "$grading_tests_file"
            git add logs/tests_results.txt
          }

          function extract_grades() {
            python3 -m classroom_tools.grading.create_grades \
              --test_associations_path="$test_associations_path"
            git add logs/grades.json
          }

          function show_grades() {
            python3 -m classroom_tools.grading.show_grades_in_readme
            git add README.md
          }

          function push_changes() {
            git config --local user.email "action@github.com"
            git config --local user.name "GitHub Action"
            git commit -a -m "Updated autograding results"
            git pull -v --rebase=true
            git push -v
          }

          run_tests
          extract_grades
          show_grades
          push_changes
```