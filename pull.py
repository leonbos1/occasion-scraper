import paramiko
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

credentials = json.load(open(os.path.join(basedir, 'credentials.json')))

VM_IP = credentials["VM_IP"]
VM_USER = credentials["VM_USER"]
VM_PASSWORD = credentials["VM_PASSWORD"]
REPO_PATH = credentials["REPO_PATH"]

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(VM_IP, username=VM_USER, password=VM_PASSWORD)

commands = [
    f"cd {REPO_PATH}",
    "sudo git pull"
]

stdin, stdout, stderr = ssh_client.exec_command("\n".join(commands))

print(stdout.read().decode())
print(stderr.read().decode())

ssh_client.close()
