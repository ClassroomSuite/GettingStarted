# Assignments
## Steps 
1. Create a new assignment template repository
    * [create from an existing assignment template](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template)
2. [Turn the repository into a template](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-template-repository)
3. Create/add all the files relevant to your assignment within your template repository
   * This may include but may not be limited to:
        * README.md
        * .gitignore
        * settings/files_to_update.txt
        * settings/variables.txt 
        * .py files
        * .github/workflows/*.yml files
4. Setup classroom workflows
    * [Update student workflows](../classroom_workflows/update_student_repositories.md)
    * [Pylint](../classroom_workflows/pylint.md)
    * [Verifications](../classroom_workflows/verifications.md)
    * [Assignment autograding](../classroom_workflows/assignment_autograding.md)
5. Add your assignment to [GitHub classrooms](./classrooms.md)
    1. Create the assignment
        * [Create individual assignment (tutorial)](https://classroom.github.com/help/creating-an-individual-assignment)
        * [Create individual assignment (video tutorial)](https://classroom.github.com/videos#rTsfBAV7sOo)
        * [Create group assignment (tutorial)](https://classroom.github.com/help/create-group-assignments)
        * [Create group assignment (cideo tutorial)](https://classroom.github.com/videos#-52quDR2QSc)
    2. Add an assigment title
    3. Add a custom repository prefix
    4. Leave the deadline option empty
    5. Make repository visibility
        * Public for in class exercises (as it's required for many features)
        * Private for graded assignments
    6. Never grant students admin access to their repository
    7. Select the template repository you created previously
    8. No need to select an online IDE for students
    9. Don't use autograding tests (as it's an incomplete feature)
    10. No need to enable feedback pull requests
6. Share the GitHub Classroom assignment link with your students
7. (optional) Run workflow **Update student repositories**
8. Verify the deadline workflow within the template repository for the assignment
    * This will create a protected branch with student submissions once the deadline is over
9. After the deadline, run the grading workflow from the template repository for the assignment
    * This will remove student write access
    * View the workflow file to see what else it does 
