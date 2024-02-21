import subprocess
import time
import requests

def call_api():
    # Make sure to replace 'API_ENDPOINT' with the actual API endpoint you want to call
    api_endpoint = 'http://127.0.0.1:5000/send_reminder_emails'
    # Make a GET request to the API endpoint
    response = requests.get(api_endpoint)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # If successful, print the response content
        print(response.json())
    else:
        # If not successful, print an error message
        print("Error:", response.status_code)

while True:
    # Call the function to call the API
    call_api()
    # Sleep for 600 seconds (10 minutes)
    time.sleep(10)
