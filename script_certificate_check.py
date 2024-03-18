import json
import re
import subprocess
import requests
import winrm
from bs4 import BeautifulSoup
from tabulate import tabulate

remote_host = "10.106.32.109"
username = "atul.anand"
password = "Techno1234@#"
powershell_command = "Get-ChildItem -Path Cert:LocalMachine\\Root"


def fetch_certificates_from_url(url, log_function=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    certificates = []
    certificate_table = soup.find('table', class_='sptable')

    for row in certificate_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 2:
            thumbprint = columns[0].text.strip()
            cn = columns[1].text.split(',')[0].strip()
            certificates.append({"Details": cn, "Thumbprint": thumbprint})
    log_function(f'The required ROOT CA certificates for Connector \n{format_cert_output(certificates)}')
    return certificates


def run_powershell_command(remote_host, username, password, powershell_command):
    session = winrm.Session(remote_host, auth=(username, password), server_cert_validation='ignore', transport='ntlm')
    result = session.run_ps(powershell_command)

    # Access the captured output
    output = result.std_out.decode('utf-8')

    # Pattern for extracting Thumbprint and Details
    pattern = re.compile(r'^\s*(?P<Thumbprint>[0-9A-Fa-f]+)\s+(?P<Details>[^,]+)', re.MULTILINE)

    # Dictionary to store parsed data
    certificates_list = []

    # Extract data using regex
    matches = re.finditer(pattern, output)
    for match in matches:
        thumbprint = match.group('Thumbprint')
        Details = match.group('Details').strip()
        # Store data in the dictionary
        certificates_list.append({'Thumbprint': thumbprint, 'Details': Details})

    return certificates_list


def certificates(existing_certificates, log_function=None):
    system_certificates = run_powershell_command(remote_host, username, password, powershell_command)

    # Format system certificates as a table
    table_headers = ["Thumbprint", "Details"]
    table_data = [(cert["Thumbprint"], cert["Details"]) for cert in system_certificates]
    certificates_table = tabulate(table_data, headers=table_headers, tablefmt="pretty", stralign="center")

    log_function(
        f"The System contains these certificates: \n{certificates_table}\nStarting the comparison of the certificates on the current system")

    # Extract thumbprints from existing_cert into a set
    system_thumbprints = [cert['Thumbprint'] for cert in system_certificates]

    # Find missing certificates from system_cert
    missing_certificates = []
    for cert in existing_certificates:
        thumbprint = cert['Thumbprint']
        details = cert['Details']
        if thumbprint not in system_thumbprints:
            missing_certificates.append({"Details": details, "Thumbprint": thumbprint})

    # Format missing certificates as a table
    if missing_certificates:
        missing_certificates_table = format_cert_output(missing_certificates)
        # missing_table_headers = ["Thumbprint", "Details"]
        # missing_table_data = missing_certificates
        # missing_certificates_table = tabulate(missing_table_data, headers=missing_table_headers, tablefmt="pretty")

        # Log missing certificates
        log_function(f"Missing certificates:\n{missing_certificates_table}")
        return missing_certificates
    else:
        log_function("No missing certificates found.")


def format_cert_output(certificate_list):
    table_headers = ["Thumbprint", "Details"]
    table_data = [[cert["Thumbprint"], cert["Details"].split(",")[0].strip()] for cert in certificate_list]
    missing_certificates_table = tabulate(table_data, headers=table_headers, tablefmt="pretty")
    return missing_certificates_table
