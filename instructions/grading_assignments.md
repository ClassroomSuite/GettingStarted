# Graphs and statistics
View [repository graphs](https://docs.github.com/en/github/visualizing-repository-data-with-graphs/about-repository-graphs)
## Contributor graphs
* View different types of contributions over a selected period of time with [GitHub Insights/Contributors](https://docs.github.com/en/github/visualizing-repository-data-with-graphs/viewing-a-projects-contributors):
    * additions
    * deletions
    * commits
* View how much work was done across time
* Compare each student's contributions
* View all commits from a specific student
    * This is can also be accomplished by appending the following to a repository URL: <br>[/commits?author=username]()
    * e.g [https://github.com/OrgName/RepoName/commits?author=student_username]()
# Grading using pull requests
Pull requests are a great way to request feedback for code you worked on. Pull request reviewers can view file changes and commits, they can comment on specific lines of code with code suggestions commentsGitHub makes it easy to review code. You can view all the commits changes, view commits, Pull requests

##Help
* [Collaborating with issues and pull requests](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests)
* [Commenting on a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request#about-pull-request-comments)
* [About pull request reviews](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-request-reviews)

## Steps
1. Students work on a branch (usually the master branch) of their respective repository until the assignment deadline.
2. Set access permissions to pull (read-only) to prevent students from pushing changes after the deadline. This will also prevent students from merging or closing pull requests.
3. Update students repositories workflows and files to ensure testing/grading files are up-to-date and can be trusted (as some students may have modified them).
2. After the deadline, create a new branch from the first commit of the master branch for each student repository on GitHub.
4. Create a pull request to merge the student's branch with all the student's commits into your new "grading" branch.
5. Ensure that tests are ran on the desired branch if using automated testing.
6. Provide feedback by reviewing the pull request using GitHub.
7. Add a grading report in the student's repository.

Note: For students with more experience with git and GitHub, it's possible to [protect the master branch](https://docs.github.com/en/github/administering-a-repository/configuring-protected-branches) (this can be accomplished on the assignment template repository beforehand) and require students to work on their own unprotected branches. Students will then have to create pull requests (to merge their branch into the master branch). The teacher will able to review and provide feedback on these requests. This way of giving feedback is closer to how GitHub is used in the workplace.
