import requests

# URL to send the POST request to
url = "http://127.0.0.1:5000/"
url = "https://johnnewto.pythonanywhere.com/"

# Message to send (modify as needed)
payload = {
    "message": "Hello, this is a test message! to https://johnnewto.pythonanywhere.com/"
}

try:
    # Send POST request with JSON payload
    response = requests.post(url, json=payload, timeout=5)

    # Check response status
    if response.status_code == 200 or response.status_code == 201:
        print("Message sent successfully!")
        print("Response:", response.text)
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print("Response:", response.text)

except requests.RequestException as e:
    print(f"Error sending message: {e}")