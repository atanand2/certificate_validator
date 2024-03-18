import requests
from bs4 import BeautifulSoup
import base64

BASE_URL = "https://crt.sh/"


def download_certificate(thumbprint):
    try:
        response = requests.get(BASE_URL + "/?q=" + thumbprint)
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all table cells with class 'text'
            cells = soup.find_all('td', class_='text')
            span = soup.find('span', class_='small')

            if span:
                # Find all anchor elements (a) within the span
                links = span.find_all('a')

            # Iterate through links to find the download link
            download_link = None
            for link in links:
                if "PEM" in link.text:
                    download_link = link['href']
                    break
            if download_link:
                # Construct the full download URL
                download_url = f"{BASE_URL}+{download_link}"
                # Download the certificate
                certificate_response = requests.get(download_url)
                if certificate_response.status_code == 200:
                    # Save the certificate to a file
                    certificate_content = certificate_response.text
                    return certificate_content
                else:
                    print("Failed to download certificate")
            else:
                print("Download link not found")
        else:
            print(f"Failed to download certificate. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def run_powershell_command(remote_host, username, password, powershell_command):
    session = winrm.Session(remote_host, auth=(username, password), server_cert_validation='ignore', transport='ntlm')
    result = session.run_ps(powershell_command)

    # Access the captured output
    output = result.std_out.decode('utf-8')