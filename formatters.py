import subprocess


def formatter():
    cmd = ["echo", "Running black..."]
    subprocess.run(cmd, check=True)

    cmd = ["black", "."]
    subprocess.run(cmd, check=True)

    cmd = ["echo", "Running docformatter..."]
    subprocess.run(cmd, check=True)

    cmd = ["docformatter", "-i", "-r", "."]
    subprocess.run(cmd, check=True)


def check():
    cmd = ["echo", "Running black check..."]
    subprocess.run(cmd, check=True)

    cmd = ["black", ".", "--check"]
    subprocess.run(cmd, check=True)

    cmd = ["echo", "Running docformatter check..."]
    subprocess.run(cmd, check=True)

    cmd = ["docformatter", "-c", "-r", "."]
    subprocess.run(cmd, check=True)
