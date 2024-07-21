import time
import json
import pyautogui
import threading
from pynput import mouse

# Constants
POSITIONS_FILE = 'positions.json'
CLICK_INTERVAL = 3 * 60 * 60
# Global variables
positions = []

from datetime import datetime  

def now():  
    # Get the current date and time  
    now = datetime.now()  
    
    # Format the date and time  
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")  
    
    return formatted_now  


def load_positions():
    """Load positions from a file."""
    try:
        with open(POSITIONS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_positions(positions):
    """Save positions to a file."""
    try:
        with open(POSITIONS_FILE, 'w') as file:
            json.dump(positions, file)
    except Exception as error:
        save_log(error)

def save_log(error):  
    with open("logs.txt", 'a') as file:  # Change 'w+' to 'a'  
        file.write(f"\n-- Log [{now()}]: \n" + error)


def add_position(position):
    """Add a new position to the list and save it."""
    try:
        positions.append(position)
        save_positions(positions)
        print(f"Position {position} saved.")
    except Exception as error:
        save_log(error)

def on_click(x, y, button, pressed):
    """Callback function for mouse click events."""
    try:
        if pressed and button == mouse.Button.middle:
            add_position((x, y))
    except Exception as error:
        save_log(error)


def click_positions():
    """Click on each saved position at intervals."""
    try:
        while True:
            for position in positions:
                pyautogui.click(position)
                print(f"Clicked at {position}")
                time.sleep(0.5)
            time.sleep(CLICK_INTERVAL)
    except Exception as error:
        save_log(error)
       


def main():
    """Main function to run the program."""
    try:
        global positions
        positions = load_positions()

        choice = input("Choose 'clicker' or 'add position': ").strip().lower()

        if choice == 'add position':
            print("Click the middle mouse button to add a position.")
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
        elif choice == 'clicker':
            if not positions:
                print("No positions found. Please add positions first.")
                return
            click_thread = threading.Thread(target=click_positions)
            click_thread.start()
            click_thread.join()
        else:
            print("Invalid choice. Please choose 'clicker' or 'add position'.")
    except Exception as error:
        save_log(error)

if __name__ == "__main__":
    main()
