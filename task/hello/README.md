# The Rest Of This Document Is Pulled From Code Comments

# Python Scripts


## [/hello/run.py](/hello/run.py)

Handler that executes { "hello":{...}} task in recipe JSON.

This is meant as an example only, it executes no useful tasks. Use this as 
a template for how to connect a handler to a JSON recipe task.  It 
illustrates how to use JOSN variables, access constants in the system, and 
best practices for using this framework.  Credentials are not required for 
this recipe handler.

Call from the command line using:

`python all/run.py project/sample/say_hello.json`

### Notes

- See [/all/README.md](/all/README.md) to learn about running recipes.
- See [/cron/README.md](/cron/README.md) to learn about scheduling recipes.
- See [/auth/README.md](/auth/README.md) to learn about setting up credentials.


