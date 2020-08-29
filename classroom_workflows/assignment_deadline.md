# Assignment deadline
## Usage
Create a protected branch with student submissions at time of deadline specified with cron

**Important**:
* You must specify these variables within **settings/variables.txt**
    in order to properly select the student repositories to update
    ```
    org_name=""
    repo_filter=""
    ``` 

## Steps
All classroom workflows use GitHub Actions and Personal Access Tokens


1. Verify that REPO_PAT secret has repo permissions and is accessible by this repository
2. Verify that your organization holding student repos has GitHub Pro, GitHub Team,
GitHub Enterprise Cloud or GitHub Enterprise Server
3. Edit the workflow file by setting the schedule cron to the deadline date.
```
  schedule:
    - cron: 'x x x x x' 
```

## Troubleshooting
 * Try editing the workflow with "on: push:" if the workflow doesn't show in the actions panel
    ```
    on:
        push:
    ```
   The workflow should now be visible in the actions panel. Edit the workflow again to remove "push:"
 * Verify that the repository has access to the required [GitHub Secrets](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets)
 * Verify all the [Personal Access Tokens (PAT) used are still valid and have the required scopes](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) 
 * Validate the values set in **settings/variables.txt**
     

## Workflow
**Path**
```
.github/workflows/assignment_deadline.yml
```
**Contents**
```
# on:
#   schedule:
#      * is a special character in YAML so you have to quote this string
#     - cron:  '*/15 * * * *'
# 
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
# │ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)
# │ │ │ │ │                                   
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
# 
# Operator	Description	Example
# *	Any value	* * * * * runs every minute of every day.
# ,	Value list separator	2,10 4,5 * * * runs at minute 2 and 10 of the 4th and 5th hour of every day.
# -	Range of values	0 4-6 * * * runs at minute 0 of the 4th, 5th, and 6th hour.
# /	Step values	20/15 * * * * runs every 15 minutes starting from minute 20 through 59 (minutes 20, 35, and 50).

# Get notified when this runs:
#     https://docs.github.com/en/github/managing-subscriptions-and-notifications-on-github/configuring-notifications#github-actions-notification-options

# Verify your cron at:
#     https://crontab.guru/

# IMPORTANT: Use Coordinated Universal Time (UTC)

# Protected branches are available in public repositories with GitHub Free and GitHub Free for organizations,
# and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server.
# For more information, see GitHub's products in the GitHub Help documentation.

# Steps
# 1. Verify that REPO_PAT secret has repo permissions and is accessible by this repository
# 2. Verify that your organization holding student repos has GitHub Pro, GitHub Team, GitHub Enterprise Cloud or GitHub Enterprise Server
# 3. Set the schedule cron

name: Assignment deadline

on:
  workflow_dispatch:
  schedule:
    - cron: ''

jobs:
  apply_deadline:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      - name: Create protected branches
        run: |
          source settings/variables.txt

          python3 -m pip install -q setuptools
          python3 -m pip install -q git+${{ secrets.CLASSROOM_TOOLS_URL }}

          python3 -m classroom_tools.student_repositories.create_protected_branch_from_master \
            --token=${{ secrets.REPO_PAT }} \
            --org_name="$org_name" \
            --repo_filter="$repo_filter" \
            --branch="remise"
```