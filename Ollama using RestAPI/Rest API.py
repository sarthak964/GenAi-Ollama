import requests
import json


# rest api
url = "http://localhost:11434/api/generate"

#pyaload
payload = {
    "model":"llama3.2:1b",
    "prompt":"Explain what is machine leanring."
}

response = requests.post(url,json=payload, stream=True)

# for i in response.iter_lines():
#     print(i)



output= ""

for i in response.iter_lines():
    if i:
        data = json.loads(i.decode("utf-8"))
        if "response" in data:
            output+=data["response"]
        if data.get("done"):
            break


print(output)