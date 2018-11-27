# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [Project IAM](/iam/script_iam.json)

Sets project permissions for an email.

Maintained and supported by: kenjora@google.com

### Fields

- role (string) projects/[project name]/roles/[role name]
- email (string) Email address to grant role to.

### Instructions

- Provide a role in the form of projects/[project name]/roles/[role name]
- Enter an email to grant that role to.
- This only grants roles, you must remove them from the project manually.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /iam/script_iam.json -h`

`python script/run.py /iam/script_iam.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


## [/iam/run.py](/iam/run.py)

 Handler that executes { "iam":{...}} task in recipe JSON.

Grants roles to users in Google Cloud Projects.  Typically you define a role
in the cloud project that grants a collection of permissions for assets in
that project.  Use this call to quickly grant a user a role.

Users who authenticate against your client credentials DO NOT automatically get
access permission.  That still needs to be granted on a case by case basis.  
Placing a call to this handler early in a recipe JSON ensures the user executing
the recipe has the right privileges.  

This handler should be called with "service" auth in the the JSON.  The service should
be able to assign roles. 

### Command Line COnvenience

Mostly a helper function, your service credential will already have a higher level
of role granting and you need it to grant the role to your user.  So there is
NO SECURITY benefit, just a conveniece.

### UI Security

In a UI environment such as a web application, where users DO NOT have access to
the service credentials, but the server does have access to user credentials, this
handler allows the service to securely grant additional roles to users.

### Good Practice

Using roles is a better practice than assigning permissions to user accounts
individually because it allows for better tracking and quicker revocation. 
Changing a role permission changes all user at once without having to track 
down individuals.  We highly recommend using roles.


