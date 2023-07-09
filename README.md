# Dockrizer
A command-line tool to dockerize your applications in a jiffy.

> Supported enviroments: Node

PyPI: https://pypi.org/project/dockrizer/

<br>

## Installation
1. Install the package globally
```
pip install dockrizer
```
2. Run the entry command to show the full range of functions:
```
dts
```

## Functions
1. Dockerize your NodeJS application
    - Allows you to define the base image version
    - Easily define all dockerfile configurations
    - Automatically setup a new docker network with custom name
    - Customize docker-compose configurations 
    - Attaches the newly created docker network to the container

2. Cleanup docker image and files from an existing project


## Future Scope
1. Add support for more environments (like python, java etc)
2. More flexibility towards network configurations
    - Allow users to define the type of network created
