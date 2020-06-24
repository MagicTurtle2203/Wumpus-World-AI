from action import ActionType


class ManualAI:
    def __init__(self):
        self.text = [
                    "You smell the wumpus' stench.",
                    "You feel a breeze.",
                    "You see something glimmer.",
                    "You bump into a wall.",
                    "You hear the wumpus scream."
        ]

        self.actions = {
            "forward": ActionType.FORWARD,
            "left": ActionType.TURNLEFT,
            "right": ActionType.TURNRIGHT,
            "grab": ActionType.GRAB,
            "shoot": ActionType.SHOOT,
            "climb": ActionType.CLIMB
        }

    def get_action(self, sensors: [bool]) -> ActionType:
        for idx, sense in enumerate(sensors):
            if sense:
                print(self.text[idx])

        print()

        while True:
            action = input('Enter an action or enter "help" for the list of commands: ').lower()

            if action == "help":
                print(f"commands: {', '.join(self.actions.keys())}")
            elif action in self.actions:
                return self.actions[action]
            else:
                print("Invalid command!")
