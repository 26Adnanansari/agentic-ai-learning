import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Ensure the API key is set, otherwise raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# ========================== Customization Options ==========================

# Set the company or chatbot name
COMPANY_NAME = "YourCompany"  # You can change this to customize
ASSISTANT_NAME = f"{COMPANY_NAME} AI Assistant"
WELCOME_MESSAGE = f"Welcome to {COMPANY_NAME} AI Assistant! How can I help you today?"

# ========================== Chatbot Initialization ==========================

@cl.on_chat_start
async def start():
    """Initialize the chatbot when a user starts a new chat session."""

    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # Define the AI model to be used (Gemini 2.0 Flash)
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    # Configure the chatbot's execution settings
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True  # Tracing is disabled to improve performance
    )

    # Store an empty chat history for the session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    # Define the chatbot agent with name and instructions
    agent: Agent = Agent(
        name=ASSISTANT_NAME,
        instructions="You are a helpful AI assistant, designed to provide intelligent and short or normal not too large for engaging responses.",
        model=model
    )

    # Save the agent in the session storage
    cl.user_session.set("agent", agent)

    # Send a welcome message to the user
    await cl.Message(content=WELCOME_MESSAGE).send()

# ========================== Message Handling ==========================

@cl.on_message
async def main(message: cl.Message):
    """Process user messages and generate chatbot responses."""

    # Indicate to the user that the bot is processing the response
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieve agent and configuration from session storage
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the existing chat history from the session
    history = cl.user_session.get("chat_history") or []

    # Append the latest user message to chat history
    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")

        # Run the chatbot using the streaming method
        result = Runner.run_streamed(
            starting_agent=agent,
            input=history,
            run_config=config
        )

        # Stream the chatbot's response back to the user in real-time
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)  # Send tokens as they arrive

        # Store the final chatbot response
        response_content = result.final_output

        # Update the user message with the bot's response
        msg.content = response_content
        await msg.update()

        # Update chat history with the new response
        cl.user_session.set("chat_history", result.to_input_list())

        # Log the interaction for debugging
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        # Handle and display any errors
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
