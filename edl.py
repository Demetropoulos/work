import requests

# Set the API endpoint URL
url = "https://www.edlmanager.com/api/v1/sources/manual/1111/"

# Set the authorization header with the appropriate API key
headers = {'Authorization': 'Api-Key <KEY>'}

# Read IP addresses from the file and strip any extra whitespace/newlines
ip_file_path = "edl.lst"
with open(ip_file_path, "r") as f:
    ips = [line.strip() for line in f]

# Create the payload with the action and the list of IP addresses
payload = {
    "action": "add",
    "manual_entries": ips  # This is where the list of IP addresses is inserted
}

# Perform the GET request
r = requests.put(url, headers=headers, json=payload)

# Print the response text (JSON data, HTML content, or plain text, depending on the API endpoint)
#print(r.text)

# Optionally, check the HTTP status code for successful response
if r.status_code == 200:
    print("Request was successful.")
else:
    print(f"Request failed with status code: {r.status_code}")
