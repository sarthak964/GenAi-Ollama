📘 Ollama Using Ollama Library – Code Overview

This repository demonstrates how to use Ollama with the Ollama Python library to build text, chat, streaming, multimodal, and structured-output AI applications using local LLMs.

Below is a brief explanation of each topic covered in the code.

🔹 1. Basic Text Generation (ollama.generate)

Demonstrates how to generate text responses by providing a model and a prompt.
Also explores the response object to understand its structure and extract the generated text.

🔹 2. Handling Thinking Models

Some models return internal reasoning wrapped inside <think> tags.
This section shows how to remove those tags and extract only the final, clean response.

🔹 3. Streaming Responses

Uses the stream=True option to receive responses token by token instead of waiting for the full output.
Useful for real-time chat applications and interactive user interfaces.

🔹 4. Multimodal Input (Text + Image)

Demonstrates how to pass images to vision-capable models by converting image files into Base64 format.
Includes:

Single image description
Multiple image input for sequential story generation

🔹 5. Structured Output (JSON Schema)

Shows how to enforce structured responses using a JSON schema.
The model extracts specific fields (like name, age, gender, state) from unstructured text and returns valid JSON.

🔹 6. System Instructions

Uses system prompts to control the behavior and personality of the model, such as making responses humorous or changing explanation style.

🔹 7. Model Generation Options

Explores important generation parameters like:

1.temperature
2.top_p
3.top_k
4.num_predict
5.repeat_penalty

These options help control creativity, randomness, and repetition.

🔹 8. Generate vs Chat Function

Demonstrates:
Stateless chatbot using ollama.generate()
Stateful chatbot using ollama.chat() with conversation history
Helps understand when to use each approach.

🔹 9. Passing Images in Chat

Shows how to attach images directly inside chat messages and continue a conversation about the same image using vision models.

🔹 10. Ollama Model & CLI Operations

Covers essential model management operations:
Listing local models
Pulling new models
Viewing model details
Deleting unused models


🚀 Summary

This repository serves as a practical reference for building local LLM applications, multimodal systems, structured data extraction, and conversational AI using Ollama