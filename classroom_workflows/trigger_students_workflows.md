# Trigger students workflows
## Usage
Create a repository dispatch event in student repositories to trigger all workflows with:
```
on:
  repository_dispatch:
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
     

## Workflow
**Path**
```
.github/workflows/trigger_students_workflows.yml
```
**Contents**
```
# IMPORTANT: Only students workflows with repository_dispatch will be triggered
# You may specify an event_type to trigger specific workflows:
# on:
#   repository_dispatch:
#     types: [your_event_type] # optional. Will capture all types if not specified
#

name: Trigger students workflows

on:
  workflow_dispatch:
    inputs:
      org_name:
        description: "Name of organization with student repositories"
        required: true
      repo_filter:
        description: "Prefix to filter repositories for a given assignment or exercise"
        required: true
      event_type:
        description: "Event type shown in Actions (may be used to select specific workflows)"
        required: false
        default: "Manual trigger"

jobs:
  trigger_workflows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Trigger workflows
        run: |
          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}
          python3 -m classroom_tools.student_repositories.trigger_workflows \
            --token=${{ secrets.REPO_WORKFLOW_PAT }} \
            --org_name=${{ github.event.inputs.org_name }} \
            --repo_filter=${{ github.event.inputs.repo_filter }} \
            --event_type="${{ github.event.inputs.event_type }}"
```