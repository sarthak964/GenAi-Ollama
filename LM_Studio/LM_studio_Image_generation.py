import lmstudio as lms

# Load model
model = lms.llm("qwen/qwen3-vl-4b")

# Prepare image
image_path = "img.png"
image_handle = lms.prepare_image(image_path)

# Create chat and add user message + image
chat = lms.Chat()  # chat class object
chat.add_user_message(
    "What programming languages are mentioned in this image?",
    images=[image_handle]
)

# Generate response using model.response
result = model.respond(chat)
print(result)

