import click


def node_dockerfile_input():
    """
    Setup dockerfile for Node.
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
        click.echo(
            "\nEdit docker configurations:\nHit 'Enter' to select default values"
        )
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
    Setup docker-compose.yml for Node.
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
        },
    }
    return dockercompose_values
