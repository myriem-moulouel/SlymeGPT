import asyncio
import websockets
import openai
from slyme import SlymeDriver
import time



async def handle_chatbot(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            # Process the message received from the client
            user_message = message.strip()

            # Call the GPT-3 API to get a response from the chatbot
            response = chat_with_gpt3(user_message)

            # Send the chatbot's response back to the client
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected.")




def chat_with_gpt3(user_message):
    # Make a request to the GPT-3 API
    slyme = SlymeDriver(pfname="Default")
    time.sleep(5)
    slyme.select_latest_chat()
    time.sleep(5)



    response = slyme.completion(user_message)
    time.sleep(5)

    slyme.end_session()
    return response




if __name__ == "__main__":
    server_host = "localhost"
    server_port = 8001  # Replace with your desired port number
    server = websockets.serve(handle_chatbot, server_host, server_port)
    
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
