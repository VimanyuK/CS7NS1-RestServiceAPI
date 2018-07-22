# CS7NS1-RestServiceAPI
REST service that provides an interface for submitting a set of GitHub repositories (identified as a list of strings of the form  “username/repositoryname”).service should identify the set of GitHub developers who have contributed to any of these repositories in 2018, and for this user set:

1. Total number of commit contributions to any project to which a user has contributed.
2. Total number of commit contributions as above, but restricted to projects that are members of the original submitted set.
3. The number of known programming languages for each user (presuming that the languages of any repository committed to are known to the user)
4. The weekly commit rate of users (provide a weekly rank ordering) for the submitted project set, for 2018.
5. The average commit rate of each user to any project, for 2018.
6. The total number of collaborators in 2018 (ie. a count of other users who have contributed to any project that the user has contributed to).
