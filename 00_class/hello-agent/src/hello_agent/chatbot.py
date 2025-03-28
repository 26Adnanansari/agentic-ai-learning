import chainlit as cl

@cl.on_message
async def main(message: cl.message):
    #our costom logic goes here

    #send a fake responese to the user
    await cl.Message(
        content=f"Received : {message.content}",
        ).send()
    