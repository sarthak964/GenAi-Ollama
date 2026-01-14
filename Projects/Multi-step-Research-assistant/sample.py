#%%
import ollama

#step1

user_input=input("Enter your question here: ")
print("Generating the ans...")

prompt=f"Answer this question : {user_input}"

response1=ollama.chat( model='llama3.2:1b',
                  messages=[{'role':'system','content':"You are a helpful teaching assistant"},
                           {'role':'user','content':prompt}])

print(response1['message']['content'])
#%%

#step2-->review the ans
print("Reviewing the ans....")
draft1=response1['message']['content']

prompt2=f"""
     You are a harsh reviewer,
     who is reviewing the question asked:{user_input} and the answer 
     provided is:{draft1},now you provide a feedback summary identifying the mistakes of the ans generated"""

response2=ollama.chat( model='qwen3:1.7b',
                       messages=[{'role':'system','content':"You are a harsh reviewer"},
                                 {'role':'user','content':prompt2}])
print(response2['message']['content'])

#step3-->Generate the final ans...

print("ReGenerating the final output...")
draft2=response2['message']['content']
prompt3=f"""
      You are an Experienced Teaching assistant,
     who is answering the question asked:{user_input} with also keeping in mind 
     the review :{draft2} on the answer provided is:{draft1}
     and provide a well structured full detailed ans on the question asked:{user_input}"""

finalResponse=ollama.chat( model='deepseek-r1:1.5b',
                           messages=[{'role':'system','content':'You are an Experienced Teaching assistant'},
                                     {'role':'user','content':prompt3}])
print(finalResponse['message']['content'])