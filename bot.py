from telethon import TelegramClient
from telethon.tl.types import InputPeerSelf  
import difflib
from asyncio import sleep

api_id = '23201402'
api_hash = 'ead5b4b88512c567e0ae55b617e81d0a'
phone_number = '+989154153732'
CLICK_INTERVAL = 3 * 60 * 60

from datetime import datetime  

def now():  
    # Get the current date and time  
    now = datetime.now()  
    
    # Format the date and time  
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")  
    
    return formatted_now  

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)
client.start(phone_number)

# Function to find the most similar button text
def find_most_similar_button(buttons, target_text):
    all_buttons = [(button, button.text) for row in buttons for button in row]
    # print(all_buttons)
    texts = [text for _, text in all_buttons]
    most_similar_text = difflib.get_close_matches(target_text, texts, n=1, cutoff=0.1)
    if most_similar_text:
        for button, text in all_buttons:
            if text == most_similar_text[0]:
                return button
    return None

# Function to click the button
async def click_keyboard_button(chat, target_text):
    # Get the dialog
    dialog = await client.get_entity(chat)
    saved_message_entity = InputPeerSelf()

    # Retrieve the messages to get the keyboard
    messages = await client.get_messages(dialog, limit=10)
    
    for message in messages:
        # print(message)
        if message.buttons:
            button = find_most_similar_button(message.buttons, target_text)
            
            if button:
                await button.click()
                await client.send_message(entity=saved_message_entity, message=f"{now()} :: Clicked button -> {button.text}")
                return

# Main function to perform the action
async def main():
    chat = 'B4U_ARABICBOT'
    target_text = '🎁 المكافأة اليومية'  # The text on the button you want to click
    
    while True:
        await click_keyboard_button(chat, target_text)
        await sleep(CLICK_INTERVAL)
    
       

with client:
    client.loop.run_until_complete(main())
