# dotsCLI
A command-line tool to automate deployment and containerization of your applications.

> Supported enviroments: Node

<br>

## Installation
1. Install the package globally
```
pip install dotsCLI
```
2. Run the entry command to show the full range of functions:
```
dts
```

## Functions
1. Easily deploy your frontend SPAs to remote linux servers
    - Hassle-free deployment
    - Automatic configuration of nginx request routing

2. Dockerize your NodeJS application
    - Allows you to define the base image version
    - Easily define all dockerfile configurations
    - Automatically setup a new docker network with custom name
    - Customize docker-compose configurations 
    - Attaches the newly created docker network to the container

## Future Scope
1. Add support for more environments (like python, java etc)
2. More flexibility towards docker network configurations
    - Allow users to define the type of network created
