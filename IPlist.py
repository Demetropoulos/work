def process_ip_addresses(ip_addresses):
    unique_ips = list(set(ip_addresses))  # Remove duplicates
    sw_result = ["host {}".format(ip) for ip in unique_ips]
    bad_ip_result = ["#DTS-9537\n{}".format(ip) for ip in unique_ips]
    return sw_result, bad_ip_result

# Read IP addresses from a file
input_file_path = "ip.lst"
sw_output_file_path = "sw.lst"
bad_ip_output_file_path = "mm.lst"

try:
    with open(input_file_path, 'r') as file:
        ip_addresses_list = [line.strip() for line in file.readlines()]
except IOError:
    print("Error reading file: {}".format(input_file_path))
    ip_addresses_list = []

sw_result, bad_ip_result = process_ip_addresses(ip_addresses_list)

try:
    with open(sw_output_file_path, 'w') as sw_output_file:
        sw_output_file.write('\n'.join(sw_result))
except IOError:
    print("Error writing to file: {}".format(sw_output_file_path))

try:
    with open(bad_ip_output_file_path, 'w') as bad_ip_output_file:
        bad_ip_output_file.write('\n'.join(bad_ip_result))
except IOError:
    print("Error writing to file: {}".format(bad_ip_output_file_path))
