import lmstudio as lms

model = lms.llm("llama-2-13b-chat")
result = model.respond("How is the phone s24 ultra?")

print(result)
