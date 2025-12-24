### GENERATE FUNCTION
import ollama
response = ollama.generate(model="llama3.2:1b",prompt="why is plant leaves green in color")

print(response)
print(type(response))
print(response.model_dump().keys())
print(response.response)

#FOR MODELS WITH THINKING CAPABILITIES
response = ollama.generate(model="qwen3:8b",prompt="why is plant leaves green in color")
import re
response_text= response.response
actual_response= re.sub(r"<think>.*?</think>","",response_text,flags=re.DOTALL).strip()
print(actual_response)


#STREAM PARAMETER
import ollama
stream = ollama.generate(model="llama3.2:1b",prompt="why is plant leaves green in color", stream=True)
print(stream)

for i in stream:
    print(i)
    print("**")

for i in stream:
    print(i["response"], end="")


# GIVING MULTIMODEL INPUT TO MODEL
import base64
import ollama

image_path= "img.png"

with open(image_path,"rb") as f:
    image_bytes= f.read()
image_64= base64.b64encode(image_bytes).decode("utf-8")

response= ollama.generate(model="llava:7b", images=[image_64], prompt="Describe the image  in a short paragraph")
print(response.response)


# multiple images  as an input
image_paths = ["img.png","img_1.png", "img_2.png", "img_3.png"]

images_base64=[]
for i in image_paths:
    with open(i , "rb") as f:
        image_bytes= f.read()
        images_base64.append(base64.b64encode(image_bytes).decode("utf-8"))




response= ollama.generate(model="llava:7b", images=images_base64,
                          prompt="Generate an story based on these images, make sure you take context from each and every image in sequential order.")
print(response.response)




# STRUCTURED OUTPUT
paragraph = """There are ten individuals in the group. Alex Johnson, a 28-year-old male from California, 
enjoys hiking. Priya Singh,
 a 34-year-old female from Texas, works as a graphic designer. Michael Brown, 
 a 45-year-old male from New York, loves cooking.
  Sara Lopez, a 29-year-old female from Florida, is an aspiring writer. David Kim,
   a 38-year-old male from Illinois, practices photography.
   Anita Patel, a 26-year-old female from Arizona, volunteers at animal shelters.
    James Wilson, a 50-year-old male from Ohio,
    collects vintage records. Emily Davis, a 31-year-old female from Washington,
     runs marathons. Robert Martinez,
     a 42-year-old male from Georgia, enjoys woodworking. Finally, Neha Sharma,
      a 27-year-old female from Colorado, is passionate about
     environmental conservation."""

response= ollama.generate(
    model="qwen3:8b",
    prompt=f"Extract the name, age, gender, and state of each person mentioned in the paragraph below. Return the information in JSON format according to the schema.\n\nParagraph:\n{paragraph}",
    format={
    "type": "object",
    "properties": {
        "people": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                    "state": {"type": "string"}
                },
                "required": ["name", "age", "gender", "state"]
            }
        }
    },
    "required": ["people"]
})


print(response.response)





#SYSTEM INSTRUCTION
response = ollama.generate(model="llama3.2:1b",prompt="why is the ocean blue", system="You are an funny assistant , you explain things in funny way")
print(response.response)


# OPTIONS PARAMETER
response = ollama.generate(model="llama3.2:1b",prompt="why is the ocean blue",
                           options={
                               "temperature":0.3,
                               "top_p":0.5,
                               "top_k":45
                           })


print(response.response)






#---------------------------------****************-----------------------
#GENERATE VS CHAT FUNCTION
#CHATBOT USING GENERATE FUNCTION

while True:
    user_input= input("You: ")


    if user_input.lower()=="quit":
        print("Assistant: Goodbye")
        break

    response= ollama.generate(model="llama3.2:1b",prompt=user_input)
    print("Assistant:", response.response)



# CHATBOT USING OLLAMA CHAT
messages=[]
messages.append({"role":"system", "content":"You are a funny assistant, you tell joke in every output"})

while True:
    user_input = input("You: ")

    if user_input.lower()=="quit":
            print("Assistant: Goodbye")
            break

    messages.append({"role":"user", "content":user_input})

    response= ollama.chat(model="llama3.2:1b",messages=messages)
    print("Assistant",response["message"]["content"])

    messages.append({"role":"assistant","content":response["message"]["content"]})


print(messages)

# PASSING IMAGE IN CHAT FUNCTION
image_path= "img.png"

with open(image_path,"rb") as f:
    image_bytes= f.read()
image_64= base64.b64encode(image_bytes).decode("utf-8")


messages=[]
messages.append({"role":"system","content":"YOu are  a funny assistant"})

# lets attach the image
messages.append(
    {"role":"user",
     "content":"Here is the image , I want to talk about",
     "images":[image_64]}
)


while True:
    user_input = input("You: ")

    if user_input.lower()=="quit":
            print("Assistant: Goodbye")
            break

    messages.append({"role":"user", "content":user_input})

    response= ollama.chat(model="llava:7b",messages=messages)
    print("Assistant:",response["message"]["content"])

    messages.append({"role":"assistant","content":response["message"]["content"]})


print(messages)


# OPTIONS PARAMETERS USING OLLAMA
import ollama

messages=[{"role":"user","content":"Tell me short story about dragons"}]


response=ollama.chat(
    model="llama3.2:1b",
    messages=messages,
    options={
        "temperature":1.0,
        "top_p":0.9,
        "num_predict":100,
        "repeat_penalty":1.2
    }
)


print(response["message"]["content"])




#BASICS OLLAMA COMMANDS
#OLLAMA LIST
local_models= ollama.list()
print(local_models)


for i in local_models["models"]:
    print(i["model"])
    print(i["size"])


#OLLAMA PULL
model_name="deepseek-r1"
progess = ollama.pull(model_name, stream=True)

for i in progess:
    print(i)


#OLLAMA SHOW
models_details = ollama.show("llama3.2:1b")
print(models_details)

model_dict= models_details.dict()
print(model_dict["capabilities"])
print(model_dict["parameters"])



#OLLAMA DELETE
ollama.delete("embeddinggemma:latest")