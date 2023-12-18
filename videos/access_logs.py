#access_logs.py


import re

def extract_log_details(log_entry):
    # Define a regular expression pattern based on your log format
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\S+) (\S+) (\d{3}) (\d+\.\d+\.\d+\.\d+)'

    # Use re.match to extract details from the log entry
    match = re.match(log_pattern, log_entry)
    if match:
        timestamp = match.group(1)
        request_details = match.group(2)
        status_code = match.group(4)
        client_ip = match.group(5)

        return {
            'timestamp': timestamp,
            'request_details': request_details,
            'status_code': status_code,
            'client_ip': client_ip
        }
    else:
        return None

# Read log entries from a file
log_file_path = 'logfile.txt'

with open(log_file_path, 'r') as file:
    for line in file:
        log_details = extract_log_details(line.strip())

        if log_details:
            print("Timestamp:", log_details['timestamp'])
            print("Request Details:", log_details['request_details'])
            print("Status Code:", log_details['status_code'])
            print("Client IP:", log_details['client_ip'])
            print('-' * 40)
        else:
            print("Invalid log entry format.")
