import requests
import json

# The URL of your local LM Studio server
url = "http://localhost:1234/v1/chat/completions"



# Request payload
data = {
    "model": "llama-2-13b-chat",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the three most popular programming languages?"}
    ],
    "temperature": 0.7

}
# Make the POST request
response = requests.post(url, json=data)

response_json = response.json()


print("--- Server Response ---")
print(response_json['choices'][0]['message']['content'])
