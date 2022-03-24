import paramiko
import time

conft = 'conf t'
shrun = 'sh run'
space = ' '
quit = 'q'

nocommand1 = 'no username awxuser password 0 awxpass role network-admin'
nocommand2 = 'no username awxuser sshkey'

command0 = 'sh int desc | i 1/1'
command1 = 'username awxuser2 password 0 awxpass role network-admin'
command2 = 'username awxuser2 sshkey ssh-rsa xxxHASHxxx

# Pulls username and pw from file because I'm lazy
#with open('config.txt') as f:
#    lines = f.readlines()
#    username = lines[0].strip()
#    password = lines[1].strip()
#    print(f"user: {username}, pass: {password}")


def send_command(connection, commands):
            for command in commands:
                connection.send(command)
                connection.send('\n')
                print(f"Sent command: ...{command}...")
                time.sleep(2)
            while not connection.recv_ready():
                time.sleep(1)
            lbuff = ""
            while connection.recv_ready():
                buff = connection.recv(65536).decode('utf-8')
                lbuff += buff
                print("Receiving output...")
            return lbuff

### Function to SSH ###
# Connects to device via SSH.
# Also enters a single command and returns output.
def sshinteractive(ip,commands):
    with paramiko.SSHClient() as ssh:
        print(f"Connecting to {ip} via ssh...")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='awxuser2',
                    key_filename='/home/user/.ssh/id_rsa.pub', timeout=3)
        connection = ssh.invoke_shell()
        data = send_command(connection,commands)
        return data

# Opens file with IP list of devices to configure
with open('dclist.txt') as file:
    for line in file:
        ip = line.strip()
        #print("scp " + localkey + " awxuser@" + ip + ":/" + remotekey)
        print(sshinteractive(ip,[conft,nocommand1,nocommand2,shrun,space,quit]))

        # Enter config terminal mode on SSH terminal using exec_command
        #stdin, stdout, stderr = ssh.exec_command(command0)
        #print(stdout.readlines())

        # Execute command and print output
        #stdin, stdout, stderr = ssh.exec_command(command1)
        #print(stdout.readlines())  

        # Execute another command and print output
        #stdin, stdout, stderr = ssh.exec_command(command2)
        #print(stdout.readlines())

        # Break from loop while testing        
        #break

# End of Script
print("END OF SCRIPT")
