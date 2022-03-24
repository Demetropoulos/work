import paramiko
import time
from getpass import getpass


localkey = "/home/user/.ssh/id_rsa.pub"
remotekey = "id_rsa.pub"

conft = 'conf t'
shrun = 'sh run'
space = ' '
breakcommand = 'q'

command = 'username awxuser password 0 awxpassword role network-admin'
command2 = 'username awxuser sshkey xxxHASHxxx'

# Test commands
#command = "sh ver"
#command2 = "do sh ver"

# Pulls username and pw from file because I'm lazy
with open('config.txt') as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
#    print(f"user: {username}, pass: {password}")

# Opens file with IP list of devices to configure
with open('dclist.txt') as file:
    for line in file:
        ip = line.strip()
#        print("scp " + localkey + " awxuser@" + ip + ":/" + remotekey)

# Create object of SSHClient and
# connecting to SSH
        ssh = paramiko.SSHClient()
        print(ip)

# Adding new host key to the local
# HostKeys object(in case of missing)
# AutoAddPolicy for missing host key to be set before connection setup.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect via SSH
        ssh.connect(ip, port=22, username=username, password=password, timeout=3)

# Open Interactive Shell
        connection = ssh.invoke_shell()

# Send commands, takes an ssh.invoke_shell object and
# a list of commands to be run. \r\n is sent after each command
# Returns full buffer of returned data
        def send_command(connection, commands):
            for command in commands:
                connection.send(command)
                connection.send('\n')
                time.sleep(2)
            while not connection.recv_ready():
                time.sleep(1)
            lbuff = ""
            while connection.recv_ready():
                buff = connection.recv(65536).decode('utf-8')
                lbuff += buff
            return lbuff

        data = send_command(connection, [conft,command,command2,shrun,space,breakcommand])
        print(data)

# Enter config terminal mode on SSH terminal using exec_command
#        stdin, stdout, stderr = ssh.exec_command(conft)
#        print(stdout.readlines())

# Execute command and print output
#        stdin, stdout, stderr = ssh.exec_command(command)
#        print(stdout.readlines())

# Execute another command and print output
#        stdin, stdout, stderr = ssh.exec_command(command2)
#        print(stdout.readlines())

# Close ssh session
        ssh.close()

# Break from loop while testing
#        break
