import os
import script_certificate_check
import script_certificate_fetch
import winrm

log_callback = None  # Reference to the logging function
certificates_file_path = "certificates.json"
cisco_certificates_url = "https://www.cisco.com/c/en/us/support/docs/security/amp-endpoints/216943-list-of-root" \
                         "-certificates-required-for-a.html"
remote_host = "10.106.32.109"
username = "atul.anand"
password = "Techno1234@#"
file_path = "certificate.pem"


def run_powershell_command(remote_host, username, password):
    session = winrm.Session(remote_host, auth=(username, password), server_cert_validation='ignore', transport='ntlm')

    # Transfer the certificate file to the target machine
    session.put_file(file_path, "C:\\Temp\\certificate.pem")

    # Construct the PowerShell command to import the certificate
    powershell_command = 'Import-Certificate -FilePath "certificate.pem" -CertStoreLocation "Cert:\\LocalMachine\\My\\"'

    # Execute the PowerShell command
    result = session.run_ps(powershell_command)


def set_log_callback(callback):
    global log_callback
    log_callback = callback


def append_log(log_message):
    if log_callback:
        log_callback(log_message)
    else:
        print(log_message)  # Fallback to print if GUI is not available


def check_certificates_gui(log_function):
    set_log_callback(log_function)
    missing_cert = script_certificate_check.certificates(
        script_certificate_check.fetch_certificates_from_url(cisco_certificates_url, log_function=append_log),
        log_function=append_log)
    return missing_cert


def fetch_certificates_gui(log_function, result):
    set_log_callback(log_function)
    for missing_certificate_attributes in result:
        certificate_string = script_certificate_fetch.download_certificate(missing_certificate_attributes['Thumbprint'])
        try:
            # Set default file name
            file_name = "certificate.pem"

            # Get current working directory
            current_dir = os.getcwd()

            # Construct full file path
            file_path = os.path.join(current_dir, file_name)
            run_powershell_command(remote_host, username, password)

            # Write certificate to file
            with open(file_path, 'w') as f:
                f.write(certificate_string)
            return file_path
        except Exception as e:
            return str(e)
