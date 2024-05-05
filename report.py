import requests
import json

def report_phishing_url( phishing_url):
    api_key = 'AIzaSyALPlq1q2FVg3LF1WGHvAUUyKz6QamwJ6k'

    # Safe Browsing API endpoint for reporting phishing URLs
    report_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'

    # Construct the request payload
    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": phishing_url}]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send a POST request to report the phishing URL
        response = requests.post(report_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Phishing URL successfully reported to Google Safe Browsing.")
            return True
        else:
            print("Error: Unable to report the phishing URL. HTTP Status Code:", response.status_code)
            print("Error response:", response.text)
            return False
        

    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))
        return False

# Replace 'YOUR_API_KEY' with your actual Google Safe Browsing API key
api_key = 'AIzaSyALPlq1q2FVg3LF1WGHvAUUyKz6QamwJ6k'

# URL you want to report as phishing
phishing_url = 'https://att-subdomaccesssignin.square.site/'

# print(report_phishing_url(api_key, phishing_url))