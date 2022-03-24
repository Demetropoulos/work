################################################################################
##                                                                            ##
##    This script will iterate through a file called maclist.csv,looking for  ##
##  switchports connected to MAC Addresses. If the found interface is a Port- ##
##  Channel, it will also grab the Member Ports. The show run interface       ##
##  output will also be saved within the appropriatecell, while cleaning up   ##
##  the output before saving it.                                              ##
##                                                                            ##
################################################################################

import pandas as pd
import paramiko

# Read csv into a pandas dataframe
macfile = pd.read_csv('maclist.csv')

# Assign csv row and columns
c0 = 'MAC'
c4 = 'Switch-GTWY'
c5 = 'Port-GTWY'
c6 = 'Port Configuration'
c11 = 'Port-Channel Members'

### Function to SSH ###
# Connects to device via SSH.
# Also enters a single command and returns output.
def sshconnect(ip,command):
    with paramiko.SSHClient() as ssh:
        # print("Open SSH.")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='awxuser',
                    key_filename='/home/user/.ssh/id_rsa.pub', timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command)
        # print("Closing SSH.")
        return stdout.readlines()

### Function Hostname to IP ###
# Grab hostname and parse IP from it.
# Used for a specific subnet
def nametoip(hostname):
    ipoctet =  hostname.split('-')[-1:]
    ipfull = f"10.10.0.{ipoctet[0]}"
    return ipfull

### Function Cleanup Port-Channel Output ###
# Reads 3 lines and cleans anything before the Member Ports,
# using LACP as the splitter from the output.
def pocleanup(output):
    lacpcleanup = "".join(output).split('LACP')
    if len(lacpcleanup) >=2:
        return "\n".join([line.strip() for line in lacpcleanup[1].splitlines()])

### Function Cleanup Show Run ###
# Reads 7 lines and cleans anything before 'interface' on the output.
# Also removes empty lines.
def shruncleanup(output):
    trimoutput = ''
    startkeep = False
    for line in output:
        if 'interface' in line:
            startkeep = True
        if startkeep:
            trimoutput += line.strip() + '\n'
    trimoutput = trimoutput[:-2]
    #print(f"{trimoutput}")
    return trimoutput

# Iterate through csv per row. Grab row dataframe, and row_index.
# Then, paste output of to each cell.
# Output includes: Switch port the MAC Address is connected to,
# Port-channel member ports, if it's a port-channel,
# and the show run of that interface
for row_index, row in macfile.iterrows():

    #Assign row variables
    devicemac = row[c0]
    swname = row[c4]

    print(f"Working on {row_index}, {devicemac}, {swname}...")

    # If no MAC Address, skip
    if pd.isna(devicemac):
        print(f"skipping {row_index}, no mac...\n")

    # If no switch hostname, skip
    elif pd.isna(swname):
        print(f"skipping {row_index}, no switch...\n")

    # If device MAC Address and switch hostname is present, continue
    else:

        # Assign variables to commands
        shmac = 'show mac add add ' + devicemac
        shportchannel = 'show port-channel summary interface '
        shrun = 'show run int '

        # Call Hostname to IP Function in order to SSH to a valid IP Address
        ip = nametoip(swname)
        print(f"Now SSHing into {ip}...")

        # Call SSH Function with shmac command
        readport = sshconnect(ip,shmac)[-1].split()[-1]
        # print(readport)

        # Write output to associated cell on csv
        macfile.loc[row_index,c5] = readport
        print(f"Switchport added to csv...")

        # Check if port is a port-channel
        if 'Po' in readport:
            print(f"This is a port-channel...")

            # Add port to show command
            shpc = shportchannel + readport

            # Save last 3 lines of output.
            readmemberports = sshconnect(ip,shpc)[-3:]
            # print(readmemberports)

            # Call Function to Cleanup Port-Channel Member Port output,
            # then pasting in correct cell
            macfile.loc[row_index,c11] = pocleanup(readmemberports)
            print("Port-channel member ports added to csv...")

            # Setup show run with port-channel interface
            shrunint = shrun + readport

            # Save last 7 lines of output.
            readshrun = sshconnect(ip,shrunint)[-7:]

            # Call Function to Cleanup Show Run, and place in correct cell
            macfile.loc[row_index,c6] = shruncleanup(readshrun)
            print(f"Port-channel configuration added to csv...")

            # Save new dataframe to original file
            macfile.to_csv('maclist.csv')
            print("SAVED. Moving onto next MAC...\n")

        # If no port-channel, copy the interface and paste it into the
        # appropriate cell for port configuration
        else:
            print(f"This is not a port-channel...")
            shint = shrun + readport
            readshrun = sshconnect(ip,shint)[-7:]
            macfile.loc[row_index,c6] = shruncleanup(readshrun)
            print(f"Switchport configuration added to csv...")
            macfile.to_csv('maclist.csv')
            print("SAVED. Moving onto next MAC...\n")

        # Break for test
        # break

# END Of SCRIPT
print('END OF SCRIPT')
