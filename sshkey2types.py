import paramiko
import time

conft = 'conf t'
shrun = 'sh run'
space = ' '
quit = 'q'

nocommand1 = 'no username awxuser password 0 awxpass role network-admin'
nocommand2 = 'no username awxuser sshkey'

command0 = 'sh int desc | i 1/1'
idncommand1 = 'username awxuseridn password 0 awxpass role network-admin'
idncommand2 = 'username awxuseridn sshkey ssh-rsa xxxHASHxxx'
dccommand1 = 'username awxuserdc password 0 awxpass role network-admin'
dccommand2 = 'username awxuserdc sshkey ssh-rsa xxxHASHxxx'


# Pulls username and pw from file because I'm lazy
with open('config.txt') as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
    print(f"user: {username}, pass: {password}")


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
def sshinteractiveidn(ip,commands):
    with paramiko.SSHClient() as ssh:
        print(f"Connecting to {ip} via ssh...")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username=username,
                    password=password, timeout=3)
        connection = ssh.invoke_shell()
        data = send_command(connection,commands)
        return data

def sshinteractivedc(ip,commands):
    with paramiko.SSHClient() as ssh:
        print(f"Connecting to {ip} via ssh...")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username=username,
                    password=password, timeout=3)
        connection = ssh.invoke_shell()
        data = send_command(connection,commands)
        return data

# Opens file with IP list of devices to configure
with open('ansiblelist-idn.txt') as file:
    for line in file:
        ip = line.strip()
        #print("scp " + localkey + " awxuser@" + ip + ":/" + remotekey)
        print(sshinteractiveidn(ip,[conft,idncommand1,idncommand2,shrun,space,quit]))

with open('ansiblelist-dc.txt') as file:
    for line in file:
        ip = line.strip()
        #print("scp " + localkey + " awxuser@" + ip + ":/" + remotekey)
        print(sshinteractivedc(ip,[conft,dccommand1,dccommand2,shrun,space,quit]))

# End of Script
print("END OF SCRIPT")
