Cisco Secure Endpoint Certificate Validator
Authored by Rafa Castro (rafacast@cisco.com)

Overview

The script validates whether a specified endpoint has the necessary certificates installed to ensure the proper operation of Cisco Secure Endpoint. It adheres to the guidelines provided in Cisco's documentation: https://www.cisco.com/c/en/us/support/docs/security/amp-endpoints/216943-list-of-root-certificates-required-for-a.html. The script is Python-based and can be executed through the command line on an endpoint with Python installed or via Orbital if the Scripts feature is enabled. Refer to Orbital's documentation https://orbital.amp.cisco.com/help/orbital-settings-org-tab/#script_on for more details.

Requirements
- Python v3.9 or higher
- Windows 10 or later

How to Use:

Running the script via Orbital
- Open the Cisco Orbital console
- Navigate to the 'Investigate' tab
- Choose the Windows endpoints where you want to execute the script
- Select the 'Script' option
- Paste the contents of the "se_certificate_validator.py" script into the custom script text field
- Click 'Run script'

Running the script via command prompt
- C:\Users\<user>\Downloads\se_certificate_validator> python se_certificate_validator.py


Output

The script generates a list of certificates, prioritizing the absent certificates at the start of the list. It then follows with the list of required certificates that are already installed. An example of the output is as follows. For instructions on how to install a missing certificate, refer to this link: https://youtu.be/jc_b6rQpDMc?si=Jriywsp2cQyov_r9

[MISSING] F40042E2E5F7E8EF8189FED15519AECE42C3BFA2 with CN=Microsoft Identity Verification Root Certificate Authority 2020
[OK] 3B1EFD3A66EA28B16697394703A72CA340A05BD5 with name CN=Microsoft Root Certificate Authority 2010
...
You can install the missing certificates using the instructions in the provided link: https://youtu.be/jc_b6rQpDMc?si=Jriywsp2cQyov_r9