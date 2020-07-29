# Firebase
Firebase is Google's mobile platform that helps you quickly develop high-quality apps and grow your business.

The Firebase Realtime Database is a cloud-hosted NoSQL database that lets you store and sync data between your users in realtime.

## Usage
Firebase Realtime Database is used to host and sync data regarding automated tests in student repositories.

During class exercises:
1. Students push changes to their repositories.
    * Student repositories must be public
2. On each push, a repository workflow should start that will:
    * run tests
    * show the results to the students
    * sync the results with the database
    
3. The teacher can view students submissions and test results in realtime using the [SubmissionsViewer](https://github.com/ClassroomSuite/SubmissionsViewer) that connects to the database.

The database has the following format:
```
{
    "first-student-repo": {
        "Name of first test": {
            "passing": true,
            "points": 1
        },
        "Name of second test": {
            "passing": false,
            "points": 1
        }
    },
    "second-student-repo": {
        "Name of first test": {
            "passing": true,
            "points": 1
        },
        "Name of second test": {
            "passing": false,
            "points": 1
        }
    }
}

```

## Recommendations
* You can keep the same Firebase project for across semesters
* You should empty your database at least after each semester to reduce download size 
* You should only have to use the free plan
* Avoid using the database for collecting assignment results as their is currently no safe way to used it.
    * Student's have access to repository secrets. Therefore, it's impossible to prevent a student from using said secrets to change their results in the database (even if additional authentication is used for the database).

## Steps
1. [Create a project](https://console.firebase.google.com/)
2. Add a Realtime Database
    * https://firebase.google.com/products/realtime-database/
    * https://firebase.google.com/docs/database
3. Read about [pricing](https://firebase.google.com/pricing)
and [FAQ](https://firebase.google.com/support/faq#pricing)
4. Change Realtime Database [Rules](https://firebase.google.com/docs/database/security/quickstart#public) to the following
    * This will allow public access to the database
    ```
    {
      "rules": {
        ".read": true,
        ".write": true
      }
    }
    ```
5. Find your Realtime Database link
    * It will have the following format: https://%yourproject%.firebaseio.com/
    * e.g.: [https://inf1007.firebaseio.com/]()
6. Append the following to your link: .json?
    * e.g.: [https://inf1007.firebaseio.com/.json?]()
7. Test your link in a web browser
    * You should see the contents of your database
8. Save your link, you'll need it later
9. For each GitHub organization used to store student repositories, create a new [organization secret](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets#creating-encrypted-secrets-for-an-organization) with:
   * Name: FIREBASE_DB_URL
   * Value: your saved link
   * Repository access: public repositories
