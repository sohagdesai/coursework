#!/usr/local/bin/python2.7
import sys
import paramiko

try:
    hostname, username, password, targetpath = sys.argv[1:5]
except ValueError:
    print("Failed, call with hostname username password targetpath")

command = "ls {}".format(targetpath)
print("Command to send: {}".format(command))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)
stdin, stdout, stderr = ssh.exec_command("ls {}".format(targetpath))
print(stdout.read())
ssh.close()
