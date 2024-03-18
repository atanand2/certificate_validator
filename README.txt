Cisco Secure Endpoint Certificate Validator
Authored by Atul Anand (atanand2@cisco.com)

Overview

The script validates whether a specified endpoint has the necessary certificates installed to ensure the proper operation of Cisco Secure Endpoint. It adheres to the guidelines provided in Cisco's documentation: https://www.cisco.com/c/en/us/support/docs/security/amp-endpoints/216943-list-of-root-certificates-required-for-a.html. The script is Python-based and can be executed through the command line on an endpoint with Python installed or via Orbital if the Scripts feature is enabled. Refer to Orbital's documentation https://orbital.amp.cisco.com/help/orbital-settings-org-tab/#script_on for more details.

Requirements
- Python v3.9 or higher
- Windows 10 or later

How to Use:

This GUI based tool presents two buttons
Check certificate - this is used to check if the required certificates are present
Update certificate - if one or more certificate is missing, this will automatically download the certificate and install it in the local machine
