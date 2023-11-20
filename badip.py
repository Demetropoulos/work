def remove_duplicates(ip_addresses):
    "Remove duplicate IPs."
    return list(set(ip_addresses))

def remove_bad_ip_entries(unique_ips):
    "Remove 'BadIP (never expire)' entries from the list."
    return [ip for ip in unique_ips if ip != '"BadIP (never expire)"']

def format_unique_ips(unique_ips):
    "Format unique IPs by removing special characters."
    return [ip.replace('*', '').replace('#', '') for ip in unique_ips if ip.strip()]

def format_sw_result(unique_ips):
    "Format SW result."
    return ["host {}".format(ip) for ip in unique_ips]

def format_mm_result(unique_ips):
    "Format MineMeld result."
    return ["#DTS-9537\n{}".format(ip) for ip in unique_ips]

def remove_ips_from_panexport(panexport_ips, ip_ips):
    "Remove IPs from panexport_ips that are present in ip_ips."
    return [ip for ip in panexport_ips if ip not in ip_ips]

def write_to_file(file_path, data):
    "Write data to a file and print contents to the screen."
    try:
        with open(file_path, 'w') as output_file:
            output_file.write('\n'.join(data))
        print("Contents of {}: \n{}".format(file_path, '\n'.join(data)))
    except IOError:
        print("Error writing to file: {}".format(file_path))

def write_no_print(file_path, data):
    "Write data to a file and DO NOT print contents to the screen."
    try:
        with open(file_path, 'w') as output_file:
            output_file.write('\n'.join(data))
    except IOError:
        print("Error writing to file: {}".format(file_path))

# Read IP addresses from a file
input_file_path = "panexport.lst"
previous_list_path = "previous.lst"
sw_output_file_path = "sw.lst"
mm_output_file_path = "mm.lst"
jira_output_file_path = "jira.lst"

try:
    with open(previous_list_path, 'r') as previous_file:
        previous_list = [line.strip() for line in previous_file.readlines()]
except IOError:
    print("Error reading file: {}".format(previous_list_path))
    previous_list = []

try:
    with open(input_file_path, 'r') as panexport_file:
        ip_addresses_list = [line.strip() for line in panexport_file.readlines()]
except IOError:
    print("Error reading file: {}".format(input_file_path))
    ip_addresses_list = []

# Process duplicate IPs and remove 'BadIP (never expire)' entries
unique_ips = remove_duplicates(ip_addresses_list)
filtered_ips = remove_bad_ip_entries(unique_ips)
formatted_ips = format_unique_ips(filtered_ips)
filtered_panexport_list = remove_ips_from_panexport(formatted_ips, previous_list)
write_to_file(jira_output_file_path, filtered_panexport_list)
write_no_print(previous_list_path, filtered_panexport_list)

# Format SW result and write to file
sw_result = format_sw_result(filtered_panexport_list)
write_to_file(sw_output_file_path, sw_result)

# Format bad IP result and write to file
mm_result = format_mm_result(filtered_panexport_list)
write_to_file(mm_output_file_path, mm_result)
