import os
import yaml
import click 
import shutil

from dotsCLI.config import settings

@click.group()
def cli():
    """
    Try `dts {command-name} --help` for more help
    """
    pass


@cli.command()
@click.option(
    '--address',
    '-a',
    type=click.STRING,
    required=True,
    help="Public IP of the remote server"
)
@click.option(
    '--conf-nginx',
    '-cf',
    type=click.Choice(["yes", "no"]),
    default="no",
    help="Install and configure nginx"
)
@click.option(
    '--build',
    '-bu',
    type=click.Choice(["yes", "no"]),
    default="no",
    help="Build frontend app before deployment"
)
def frontend(address, conf_nginx):
    """
    Deploy frontend app to remote server
    """
    click.echo(f"deploying frontend to remote {address}")
    click.echo(f"{settings.AWS_USER}")


@cli.command()
@click.option(
    "--base", 
    "-b", 
    type=click.Choice(["node"]),
    required=True,
    help="Base image for docker container",
)
def dockerize(base):
    """
    Setup configurations files for docker
    """
    click.echo(f"Building container with env: {base}")
    if base == "node":
        dockerize_node()
        build_flag = input("Dockerfiles configured. Do you want to build the image? (y/N): ")
        if build_flag.lower() == "y":
            os.system(f"docker-compose build")
    else:
        click.echo("Base image not supported")


def dockerize_node():
    project_dir = os.getcwd()
    try:
        dockerfile_config = node_dockerfile_input()
        with open(project_dir+"/dockerfile", "w") as dockerfile:
            dockerfile.writelines([
                f"FROM node:{dockerfile_config['version']}\n\n",
                f"WORKDIR {dockerfile_config['working_dir']}\n\n",
                f"COPY package.json {dockerfile_config['working_dir']}/package.json\n\n",
                f"RUN npm install\n\n",
                f"COPY . {dockerfile_config['working_dir']}\n\n",
                f"EXPOSE {dockerfile_config['container_port']}\n\n",
                f"CMD [\"{dockerfile_config['run_script'][0]}\", \"{dockerfile_config['run_script'][1]}\", \"{dockerfile_config['run_script'][2]}\"]"
            ])
            click.echo("Dockerfile created.\n")
    except Exception as e:
        click.echo(f"Error creating dockerfile: {e}\n")
    
    try:
        user_config = node_dockercompose_input(dockerfile_config['local_port'],dockerfile_config['container_port'])
        network_name = user_config['network_name']
        service_name = user_config['service_name']
        
        try:
            click.echo(f"\nCreating a new bridge network: {network_name}")
            os.system(f"docker network create {network_name}")
            click.echo(f"Network {network_name} created. Check network stats using `docker network inspect {network_name}`\n")
        except Exception as e:
            click.echo(f"Error creating network: {e}")
        
        dockercompose_path = project_dir+"/docker-compose.yml"
        shutil.copyfile(os.path.join(os.path.dirname(__file__), './samples/docker-compose.yml'), dockercompose_path)
        with open(dockercompose_path) as file:
            config_file = yaml.safe_load(file)

        config_file['version'] = user_config['version']
        config_file['networks'][network_name] = config_file['networks']['app_network']
        del config_file['networks']['app_network']
        config_file['services'][service_name] = config_file['services']['app_service']
        del config_file['services']['app_service']
        config_file['services'][service_name]['image'] = user_config['service_config']['image']
        config_file['services'][service_name]['container_name'] = user_config['service_config']['container_name']
        config_file['services'][service_name]['ports'] = user_config['service_config']['ports']
        config_file['services'][service_name]['environment'] = user_config['service_config']['environment']
        config_file['services'][service_name]['networks'] = user_config['service_config']['networks']

        with open(dockercompose_path, 'w') as file:
            yaml.dump(config_file, file, sort_keys=False)
        click.echo("docker-compose.yml created.\n")

    except Exception as e:
        click.echo(f"Error creating docker-compose.yml: {e}")


def node_dockerfile_input():
    """
    Setup dockerfile for Node
    """
    version = "latest"
    working_dir = "/app"
    local_port = 3000
    container_port = 3000
    run_script = ["npm", "run", "start"]
    default_config_prompt = f"""Dockerfile:\n
    Version: {version}
    Working_Directory: {working_dir}
    Local_PORT: {local_port}
    Container_PORT: {container_port}
    Run Script: {run_script}
    """
    click.echo(default_config_prompt)
    default_flag = input("Do you want to use the default configuration? (Y/N)")
    if default_flag.lower() == "n":
        click.echo("\nEdit docker configurations:\nHit 'Enter' to select default values")
        user_input = input("Version [latest]: ")
        if not user_input == "":
            version = user_input
        user_input = input("Working Directory [/app]: ")
        if not user_input == "":
            working_dir = user_input
        user_input = input("Local Port [3000]: ")
        if not user_input == "":
            local_port = user_input
        user_input = input("Container Port [3000]: ")
        if not user_input == "":
            container_port = user_input
        user_input = input("Run Script [npm run ___]: ")
        if not user_input == "":
            run_script[2] = user_input
        user_config_prompt = f"""Dockerfile:\n
            Version: {version}
            Working_Directory: {working_dir}
            Local_PORT: {local_port}
            Container_PORT: {container_port}
            Run Script: {run_script}
        """
    return {
        "version": version,
        "working_dir": working_dir,
        "local_port": local_port,
        "container_port": container_port,
        "run_script": run_script,
    }

def node_dockercompose_input(local_port, container_port):
    """
    Setup docker-compose.yml for Node
    """
    click.echo("Creating docker-compose.yml\nHit 'Enter' to select default values:\n")
    version = 3
    network = "app-net"
    service_name = "app"
    image_name = "app_image"
    container_name = "app_1"
    user_input = input("Compose File Version [3]: ")
    if not user_input == "":
        version = user_input
    user_input = input("Network [app-net]: ")
    if not user_input == "":
        network = user_input
    user_input = input("Service name [app]: ")
    if not user_input == "":
        service_name = user_input
    user_input = input("Image name [app_image]: ")
    if not user_input == "":
        image_name = user_input
    user_input = input("Container name [app_1]: ")
    if not user_input == "":
        container_name = user_input
    dockercompose_values = {
        "version": version,
        "network_name": network,
        "service_name": service_name,
        "service_config": {
            "image": image_name,
            "container_name": container_name,
            "ports": [f"{local_port}:{container_port}"],
            "environment": [f"PORT={container_port}"],
            "networks": [network],
        }
    }
    return dockercompose_values