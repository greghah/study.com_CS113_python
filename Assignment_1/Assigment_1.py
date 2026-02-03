import re
import json
from datetime import datetime

#json save function
def save_run(name, decisions, final_state):
    data = {
        "name": name,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "decisions": decisions,
        "outcome": final_state,
        "ending_text": OUTCOMES[final_state]
    }
    filename = f"alien_invasion_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nGame saved to file: {filename}")

#game segments
def display_title():
    print("=" * 60)
    print("        Welcome to Alien Invasion - A Text Adventure")
    print("=" * 60)
    print("=" * 60)
    print("Instructions:")
    print("- Type the number of your choice and press Enter.")
    print("- Your decisions affect the ending.")
    print("- Your run will be saved to a JSON file at the end.")
    print("=" * 60)
def game_start():

    #regex for input validation(starts with a letter, between 3 and 16 total chars)
    pattern = r"^[A-Za-z][A-Za-z0-9_]{2,15}$"

    while True:
        name = input("\nEnter your name/codename (3-16 chars, start with a letter): ").strip()
        if re.match(pattern, name):
            return name
        print("Invalid. Example valid names: Ghost, Neo_7, Raven99")
def scene_bedroom():
    print("\nYou wake up at 2:13 AM. The window screams. You feel someones presence.")
    print("1) Look out the window")
    print("2) Hide under the bed")

    while True:
        choice = input("Choose 1 or 2: ").strip()
     
        if choice == "1" or choice == "2":
            return choice
        else:
            print("Invalid input. Please try again.")
def scene_window_death():
    print("\nYou look out the window.")
    print("A green beam locks onto your eyes.")
    print("Your body goes cold. You drop instantly.\n")
    return "instant_death"    
def scene_under_bed():
    print("\nYou slide under the bed. Your heart is pounding.")
    print("The window SHATTERS. Something crawls in.")
    print("Claws scrape the floor. It sniffs the air like it's tasting fear.")
    print("It moves away for a second… distracted by a buzzing device.\n")

    print("1) Stay completely still and wait")
    print("2) Sneak out while it’s distracted")

    while True:
        choice = input("Choose 1 or 2: ").strip()
        if choice == "1" or choice == "2":
            return choice
        print("Invalid input. Please enter 1 or 2.")

OUTCOMES = {
    "instant_death": "You die instantly. Whatever it was… it didn’t hesitate.",
    "wait_death": "You wait too long. The monster’s breathing stops. It’s listening. It finds you.",
    "sneak_death": "You slip out and make it to the hallway… you survive longer, but it eventually tracks you down."
}

def main():
    #replay flag
    notDone = True

    while notDone:
        decisions = [] #decision list storage that reset every playthru
        display_title()
        name = game_start()

        choice1 = scene_bedroom() 
        decisions.append({"scene": "bedroom", "choice": choice1})
        
        if choice1 == "1":
            final_state = scene_window_death()
            decisions.append({"scene": "window", "choice": "look"})
        else: 
            choice2 = scene_under_bed()
            decisions.append({"scene": "under_bed", "choice": choice2})

            if choice2 == "1":
                final_state = "wait_death"
            else:
                final_state = "sneak_death"


        ending_text = OUTCOMES[final_state]

        print("\n" + "=" * 60)
        print("ENDING:")
        print(ending_text)
        print("=" * 60)

        print("\nDECISIONS LOG:")
        print(decisions)

        #save to json file
        save_run(name, decisions, final_state)

        print("\n\nWould you like to play again?")
        print("1) Keep playing")
        print("2) I'm too scared for more.")
        replayInput = input("Choose 1 or 2: ")
        if (replayInput == "1"):
            notDone = True
        else:
            notDone = False



main()
