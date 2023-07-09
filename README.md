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
3. Make a config file in a new folder named '.dts' in the root directory of your system, configuring the values respectively.

> Note: `FRONTEND_DIR_PATH` and `FRONTEND_DIST_PATH` must not contain a trailing slash.

```bash
[aws]
AWS_USER=ubuntu

[main]
FRONTEND_DIR_PATH=<path_to_dir>
FRONTEND_DIST_PATH=<path_to_dir>
SSH_KEY_PATH=<path_to_dir>/ssh-key.pem
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
