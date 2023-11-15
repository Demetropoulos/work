def remove_duplicates(ip_addresses):
    "Remove duplicate IPs."
    return list(set(ip_addresses))

def format_sw_result(unique_ips):
    "Format SW result."
    return ["host {}".format(ip) for ip in unique_ips]

def format_bad_ip_result(unique_ips):
    "Format bad IP result."
    return ["#DTS-9537\n{}".format(ip) for ip in unique_ips]

def write_to_file(file_path, data):
    "Write data to a file and print contents to the screen."
    try:
        with open(file_path, 'w') as output_file:
            output_file.write('\n'.join(data))
        print("Contents of {}: \n{}".format(file_path, '\n'.join(data)))
    except IOError:
        print("Error writing to file: {}".format(file_path))

# Read IP addresses from a file
input_file_path = "ip.lst"
sw_output_file_path = "sw.lst"
bad_ip_output_file_path = "mm.lst"
jira_output_file_path = "jira.lst"

try:
    with open(input_file_path, 'r') as file:
        ip_addresses_list = [line.strip() for line in file.readlines()]
except IOError:
    print("Error reading file: {}".format(input_file_path))
    ip_addresses_list = []

# Process duplicate IPs
unique_ips = remove_duplicates(ip_addresses_list)
write_to_file (jira_output_file_path, unique_ips)

# Format SW result and write to file
sw_result = format_sw_result(unique_ips)
write_to_file(sw_output_file_path, sw_result)

# Format bad IP result and write to file
bad_ip_result = format_bad_ip_result(unique_ips)
write_to_file(bad_ip_output_file_path, bad_ip_result)
