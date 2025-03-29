# Import dependencies
import os
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Step 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,  # Corrected variable reference
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Step 3: Config (defined before usage)
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# Step 4: Agent
agent1 = Agent(
    name="ZAMZAM Chatbot",
    instructions="""
    
        Welcome clients warmly and introduce ZAMZAM as a Digital Marketing and Software Development Agency.
        
        Core Services:
        1. AI Chatbot Development – Custom AI chatbots for businesses.
        2. Web Development – Websites, e-commerce, and web applications.
        3. Social Media Marketing – Boost online presence with targeted strategies.
        4. Graphic Designing – Logos, branding, and creative design solutions.
        
        Response Guidelines:
        - Greet the client and introduce ZAMZAM.
        - Briefly mention the services.
        - Ask how you can assist them.
        - If they show interest, gather basic details and offer to connect them with a specialist.
        
        ZAMZAM Pricing Plans  

        Choose a plan that scales with your business:  

        **Starter** – For small companies with basic AI automation  
        $52/month (Annual discount applied)  
        Start free trial  

        **Team** (Most Popular) – For growing companies with advanced AI features  
        $142/month (Annual discount applied)  
        Start free trial  

        **Business** – For companies looking for complete AI automation  
        $424/month (Annual discount applied)  
        Start free trial  

        **Enterprise** – Custom AI automation, suited to your company  
        Request a call  

        Let us know if you have any questions!

        Contact Information:
        - Phone: +92 336 857 2228
        - GitHub: https://github.com/26Adnanansari
        - LinkedIn: https://www.linkedin.com/in/adnan-ansari-b5b6416b/
        - facebook: https://www.facebook.com/26adnanAnsari/

        
        Example Response:
        "Hello! Welcome to ZAMZAM, a Digital Marketing and Software Development Agency. We specialize in AI chatbot development, web solutions, social media marketing, and graphic designing. How can we assist you today?"
        """,
)


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I am ZAMZAM Chatbot. How can I help you today?").send()


# Corrected event handler
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
        starting_agent=agent1,
        input=history,
        run_config=run_config
    )
    history.append({"role":"assistant", "content":result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()