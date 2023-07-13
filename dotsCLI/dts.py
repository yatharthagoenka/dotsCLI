import os
import yaml
import click
import shutil
import paramiko

from dotsCLI.config import settings
from dotsCLI.docker.parser import node_dockercompose_input, node_dockerfile_input


@click.group()
def cli():
    """
    Try `dts {command-name} --help` for more help.
    """
    pass


@cli.command()
@click.option(
    "--address",
    "-a",
    required=True,
    help="Public IP of the remote machine to connect",
)
def remote_ssh(address):
    """
    Launch a session of remote machine on local.
    """
    ssh_pem_file_path = os.path.join(
        settings.SSH_DIRECTORY, os.path.basename(settings.PEM_KEY_PATH)
    )
    if not os.path.exists(ssh_pem_file_path):
        os.system(f"cp {settings.PEM_KEY_PATH} {settings.SSH_DIRECTORY}")
        click.echo("Added PEM key to SSH directory")
    else:
        print("The PEM key already exists in the SSH directory, skipping.")

    host_configuration = [
        f"\nHost {address}\n",
        f"  HostName {address}\n",
        "  User ubuntu\n",
        f'  IdentityFile "{ssh_pem_file_path}"\n',
    ]
    with open(f"{settings.SSH_DIRECTORY}/config", "r") as file:
        ssh_config_file = file.readlines()
    if not any(
        host_configuration[0].strip() == line.strip() for line in ssh_config_file
    ):
        with open(f"{settings.SSH_DIRECTORY}/config", "a") as file:
            file.writelines(host_configuration)
    click.echo("Added host to SSH config.\nConnecting to remote server...")

    os.system(f"code --folder-uri vscode-remote://ssh-remote+{address}/home/ubuntu/")


@cli.command()
@click.option(
    "--address",
    "-a",
    type=click.STRING,
    required=True,
    help="Public IP of the remote server",
)
@click.option(
    "--conf-nginx",
    "-cf",
    type=click.Choice(["yes", "no"]),
    default="no",
    help="Install and configure nginx",
)
@click.option(
    "--build",
    "-bu",
    type=click.Choice(["yes", "no"]),
    default="no",
    help="Build frontend app before deployment",
)
@click.option(
    "--path",
    "-p",
    type=click.Choice(["yes", "no"]),
    default="no",
    help="Specify path of frontend directory",
)
def frontend(address, conf_nginx, build, path):
    """
    Deploy frontend app to remote server.
    """
    dist_path = settings.FRONTEND_DIST_PATH
    if path == "yes":
        dist_path = input("Enter dist folder path: ")
    if build == "yes":
        click.echo("Building application for deployment")
        os.system(f"cd {settings.FRONTEND_DIR_PATH}")
        os.system("npm run build")
    click.echo(f"Connecting to remote {address}")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        pem_key = paramiko.RSAKey.from_private_key_file(settings.SSH_KEY_PATH)
        client.connect(address, username=settings.AWS_USER, pkey=pem_key)
    except paramiko.AuthenticationException as e:
        print("Authentication failed:", str(e))
    except paramiko.SSHException as e:
        print("SSH connection failed:", str(e))
    click.echo("Deleting existing files and copying to /var/www/html")
    client.exec_command("sudo rm -rf /var/www/html/*")
    os.system(
        f"sudo scp -i {settings.SSH_KEY_PATH} -r {dist_path}/* {settings.AWS_USER}@{address}:/var/www/test/"
    )


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
    Setup configurations files for docker.
    """
    click.echo(f"Building container with env: {base}")
    if base == "node":
        dockerize_node()
        build_flag = input(
            "Dockerfiles configured. Do you want to build the image? (y/N): "
        )
        if build_flag.lower() == "y":
            os.system(f"docker-compose build")
    else:
        click.echo("Base image not supported")


def dockerize_node():
    project_dir = os.getcwd()
    try:
        dockerfile_config = node_dockerfile_input()
        with open(project_dir + "/dockerfile", "w") as dockerfile:
            dockerfile.writelines(
                [
                    f"FROM node:{dockerfile_config['version']}\n\n",
                    f"WORKDIR {dockerfile_config['working_dir']}\n\n",
                    f"COPY package.json {dockerfile_config['working_dir']}/package.json\n\n",
                    f"RUN npm install\n\n",
                    f"COPY . {dockerfile_config['working_dir']}\n\n",
                    f"EXPOSE {dockerfile_config['container_port']}\n\n",
                    f"CMD [\"{dockerfile_config['run_script'][0]}\", \"{dockerfile_config['run_script'][1]}\", \"{dockerfile_config['run_script'][2]}\"]",
                ]
            )
            click.echo("Dockerfile created.\n")
    except Exception as e:
        click.echo(f"Error creating dockerfile: {e}\n")

    try:
        user_config = node_dockercompose_input(
            dockerfile_config["local_port"], dockerfile_config["container_port"]
        )
        network_name = user_config["network_name"]
        service_name = user_config["service_name"]

        try:
            click.echo(f"\nCreating a new bridge network: {network_name}")
            os.system(f"docker network create {network_name}")
            click.echo(
                f"Network {network_name} created. Check network stats using `docker network inspect {network_name}`\n"
            )
        except Exception as e:
            click.echo(f"Error creating network: {e}")

        dockercompose_path = project_dir + "/docker-compose.yml"
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "./samples/docker-compose.yml"),
            dockercompose_path,
        )
        with open(dockercompose_path) as file:
            config_file = yaml.safe_load(file)

        config_file["version"] = user_config["version"]
        config_file["networks"][network_name] = config_file["networks"]["app_network"]
        del config_file["networks"]["app_network"]
        config_file["services"][service_name] = config_file["services"]["app_service"]
        del config_file["services"]["app_service"]
        config_file["services"][service_name]["image"] = user_config["service_config"][
            "image"
        ]
        config_file["services"][service_name]["container_name"] = user_config[
            "service_config"
        ]["container_name"]
        config_file["services"][service_name]["ports"] = user_config["service_config"][
            "ports"
        ]
        config_file["services"][service_name]["environment"] = user_config[
            "service_config"
        ]["environment"]
        config_file["services"][service_name]["networks"] = user_config[
            "service_config"
        ]["networks"]

        with open(dockercompose_path, "w") as file:
            yaml.dump(config_file, file, sort_keys=False)
        click.echo("docker-compose.yml created.\n")

    except Exception as e:
        click.echo(f"Error creating docker-compose.yml: {e}")
