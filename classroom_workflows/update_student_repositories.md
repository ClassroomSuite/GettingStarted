# Update student repositories
## Usage
Update all student repositories by triggering this workflow.

**Important**:
* All student repositories will be created identical to the template repository used for GitHub Classroom Assignments
* Once triggered this workflows will:
    * erase all workflows from student repositories (in order to prevent cheating)
    * update/overwrite all student files specified in: **settings/files_to_update.txt**
      
      Here is an example of settings/files_to_update.txt
        ```
        file1.txt
        file2.txt
        README.md
        ```
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
.github/workflows/update_student_repositories.yml
```
**Contents**
```
name: Update students repos

on:
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Update students repos
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+"${{ secrets.CLASSROOM_TOOLS_URL }}"

          python3 -m classroom_tools.student_repositories.delete_workflows \
            --token=${{ secrets.REPO_WORKFLOW_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter"

          python3 -m classroom_tools.student_repositories.sync_with_template_repository \
            --template_repo_fullname="$GITHUB_REPOSITORY" \
            --token="${{ secrets.REPO_WORKFLOW_PAT }}" \
            --org_name="$org_name" \
            --repo_filter="$repo_filter"
```