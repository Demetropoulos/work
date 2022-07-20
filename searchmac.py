import paramiko
import yaml

def sshconnectcampus(ip,command):
    with paramiko.SSHClient() as ssh:
        # print("Open SSH.")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='ansibleUSERcampus',
                    key_filename='/home/USER/.ssh/id_rsa.pub', timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command)
        # print("Closing SSH.")
        return stdout.readlines()

def sshconnectdc(ip,command):
    with paramiko.SSHClient() as ssh:
        # print("Open SSH.")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='ansibleUSERdc',
                    key_filename='/home/USER/.ssh/id_rsa.pub', timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command)
        # print("Closing SSH.")
        return stdout.readlines()

print("\nThis will help you locate a switch and port from a MAC Address.\n",
        "Please ensure you're searching for a wired device.\n",
        "If wireless, please search Cisco DNAC.\n")

siteknown = input("Do you know the site where this MAC Address is located? y/n: ")
if siteknown == 'y':
    siteknown = True
else:
    siteknown = False

if siteknown == True:
    print("\nHere is our site list: \n")
    
    with open('sites.yml','r') as s:
        listsites = yaml.safe_load(s)
        sites_dict = listsites['sites']
        for site in sites_dict:
            singlesite = sites_dict[site]
            print(f"{singlesite['siteID']} - {singlesite['siteName']} - {singlesite['siteAddress']}")
            #print(item + '\n')
        picksite = input("\nPlease choose the number corresponding to your site: ")
    mac = input("\nPlease enter the MAC Address (abcd.ef12.3456, or ab-cd-ef-12-34-56, or ab:cd:ef:12:34:56): ")
    shmac = 'sh mac add add ' + mac

    selection = int(picksite)
    if selection <= 9:
        ip = singlesite['siteRouterA']
        print(f"\nThis is the router IP: {ip}\n")
        macoutput = sshconnectdc(ip,shmac)
    else:
        macoutput = sshconnectcampus(ip,shmac)
    
    print(macoutput)

else:
    print("\nSearching for a MAC Address throughout the campus?\n",
          "Please provide the MAC Address and sit tight.\n",
          "This might take a few minutes.\n\n")
    mac = input("Please enter the MAC Address (abcd.ef12.3456, or ab-cd-ef-12-34-56, or ab:cd:ef:12:34:56): ")
    shmac = 'sh mac add add ' + mac
    with open('sites.yml','r') as s:
        sites = yaml.safe_load(s)
        for site in sites:
            print(f"Trying {site}...")
            if picksite <= 9:
                macoutput = sshconnectdc(site['siteRouterA'],shmac)
            else:
                macoutput = sshconnectcampus(site['siteRouterA'],shmac)
            if mac in macoutput:
                print(f"MAC is at {site}\n")
            else:
                print(f"MAC not at {site}\n")
