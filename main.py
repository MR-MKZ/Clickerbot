import time
import json
import pyautogui
import threading
from pynput import mouse

# Constants
POSITIONS_FILE = 'positions.json'
CLICK_INTERVAL = 3 * (60 * 60)
# Global variables
positions = []


def load_positions():
    """Load positions from a file."""
    try:
        with open(POSITIONS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_positions(positions):
    """Save positions to a file."""
    with open(POSITIONS_FILE, 'w') as file:
        json.dump(positions, file)


def add_position(position):
    """Add a new position to the list and save it."""
    positions.append(position)
    save_positions(positions)
    print(f"Position {position} saved.")


def on_click(x, y, button, pressed):
    """Callback function for mouse click events."""
    if pressed and button == mouse.Button.middle:
        add_position((x, y))


def click_positions():
    """Click on each saved position at intervals."""
    while True:
        for position in positions:
            pyautogui.click(position)
            print(f"Clicked at {position}")
            time.sleep(0.5)
        time.sleep(CLICK_INTERVAL)


def main():
    """Main function to run the program."""
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


if __name__ == "__main__":
    main()
