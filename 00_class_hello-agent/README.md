# OpenAI Agentic SDK - Learning Notes

## Introduction  
This repository contains learning notes and practical steps for using the OpenAI Agentic SDK with `uv`. It covers project initialization, dependency management, and running Chainlit-based applications.

---

## **Project Initialization**  

### **Without `--package` (Basic Structure)**  
```sh
uv init projectname
```
- Creates a basic project structure.  

### **With `--package` (Organized Structure)**  
```sh
uv init --package projectname
```
- Generates a structured project with a `src/` directory.  

---

## **Running the Project**  
```sh
uv run projectname
```
- If using `--package`, navigate to `src/projectname/` before running.  

---

## **Managing Dependencies**  
By default, `pyproject.toml` does not include any dependencies.  

To add **Chainlit**:  
```sh
uv add chainlit
```

---

## **Running the Project with Chainlit**  
```sh
uv run chainlit run projectname -w
```
- The `-w` flag enables hot-reloading, applying code changes without restarting the server.  

---

## **Example: Creating a Chatbot**  
To create a simple chatbot using Chainlit, follow these steps:

1. Create a new file named `chatbot.py`.
2. Add the following code:

```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Custom logic goes here
    
    # Send a response to the user
    await cl.Message(
        content=f"Received: {message.content}"
    ).send()
```

### **How It Works**  
- When a user sends a message (e.g., "Hi"), Chainlit receives it and responds with "Received: Hi".  

---

## **Conclusion**  
This guide serves as a structured reference for setting up and running projects with `uv` and Chainlit. It ensures a clean development process with minimal overhead.

