# Assignment grading
## Prerequisite
Verify that the [assignment deadline workflow](assignment_deadline.md) has already created a submission branch in student repositories.
* The submission branches contain all commits up till the assignment deadline
* The master branches will contain all commits before and after the assignment deadline
## Usage
Start the grading process
1. Remove student repository write access
2. Remove submission branch protection (branch protection can prevent some workflows from working properly)
3. Change default branch to grading branch (avoid interchanging master/submission branches)
4. Update students repos
5. Create new grading branch and a pull request for reviewing student code/commits.
6. Trigger other grading workflows in student repos. This only concerns workflows with:
    ```
    on:
      repository_dispatch:
    ```

**Important**:
* You must specify these variables within **settings/variables.txt**
    in order to properly select the student repositories to update
    ```
    org_name=""
    repo_filter=""
    ``` 

## Steps
All classroom workflows use GitHub Actions and Personal Access Tokens

1. Go to actions panel
2. In the left sidebar, click the workflow you want to run.
3. Above the list of workflow runs, select Run workflow.
4. Select the branch where the workflow will run and type the input parameters used by the workflow. Click Run workflow.

## Troubleshooting
 * Verify that the repository has access to the required [GitHub Secrets](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)
 * Verify all the [Personal Access Tokens (PAT) used are still valid and have the required scopes](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) 
 * Validate the values set in **settings/variables.txt**

## Workflow
**Path**
```
.github/workflows/assignment_grading.yml
```
**Contents**
```
name: Assignment grading

on:
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Remove student write permissions
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          python3 -m classroom_tools.student_repositories.access_permissions \
            --token=${{ secrets.REPO_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --new_permission_level=pull

      - name: Remove submission branch protection
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          python3 -m classroom_tools.student_repositories.change_branch_protection \
            --token=${{ secrets.REPO_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --branch="remise" \
            --protect="False"

      - name: Change default branch to grading branch
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          python3 -m classroom_tools.student_repositories.change_default_branch \
            --token=${{ secrets.REPO_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --branch="remise"

      - uses: actions/checkout@v2
      - name: Update students repos
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+"${{ secrets.CLASSROOM_TOOLS_URL }}"

          python3 -m classroom_tools.student_repositories.delete_workflows \
            --token=${{ secrets.REPO_WORKFLOW_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --branch="remise"

          python3 -m classroom_tools.student_repositories.sync_with_template_repository \
            --template_repo_fullname="$GITHUB_REPOSITORY" \
            --token="${{ secrets.REPO_WORKFLOW_PAT }}" \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --branch="remise"

      - uses: actions/checkout@v2
      - name: Create pull requests
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          pull_request_body="La correction du TP est effectuer avec un Pull Request Review. "
          pull_request_body+="La branch master contient les commits effectués avant et après la date de remise. "
          pull_request_body+="La branch remise contient les commits effectués uniquement avant la date de remise. "
          pull_request_body+="La branch correction contient uniquement le premier commit et est utilisée comme branch de base pour le Pull Request. "
          pull_request_body+="Lisez les commentaires des correcteurs/trices. "
          pull_request_body+="Pour plus d'information consulter: "
          pull_request_body+="https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request"

          python3 -m classroom_tools.student_repositories.create_grading_branch_and_pull_request \
          --token=${{ secrets.REPO_PAT }} \
          --org_name="$org_name" \
          --repo_filter="$repo_filter" \
          --head="remise" \
          --base="correction" \
          --pull_request_title="Correction" \
          --pull_request_body="$pull_request_body"

      - uses: actions/checkout@v2
      - name: Trigger workflows
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          python3 -m classroom_tools.student_repositories.trigger_workflows \
            --token=${{ secrets.REPO_WORKFLOW_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --event_type="Assignment grading"
```