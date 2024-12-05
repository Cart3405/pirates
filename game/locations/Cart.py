####################################################################################################
# Imports
####################################################################################################

from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random
import time

####################################################################################################
# Events and supporting classes
####################################################################################################

class Cart (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Cart"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "east" or verb == "west"):
            display.announce ("You walk all the way around the island on the beach and find a door in the side of a mountian.")

####################
# Player and NPC
####################

class Player:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
    
    def attack():
        return random.randint(1, self.attack_power) # type: ignore
    
    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self, health):
        return self.health > 0

class Golem(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["smash"] = ["smash",random.randrange(70,101), (30,60)]
        #75 to 100 hp, smash attack, 45 to 75 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        self.type_name = "Rock Golem"

class Golem2(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["smash"] = ["smash",random.randrange(90,110), (70,90)]
        #90 to 110 hp, smash attack, 50 to 100 speed (100 is "normal")
        super().__init__(name, random.randrange(8,25), attacks, 250 + random.randrange(-20,21))
        self.type_name = "Cave Golem"

class Boss(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["Slash"] = ["Slash",random.randrange(120,150), (90,110)]
        #100 to 150 hp, slash attack, 100 to 150 speed (100 is "normal")
        super().__init__(name, random.randrange(10,30), attacks, 550 + random.randrange(-20,21))
        self.type_name = "Cave Boss"

###########################
# Rock Golem Room 1
###########################

class RockGolem (event.Event):
    '''
    A combat encounter with a Rock Golem.
    When the event is drawn, creates a combat encounter with a Rock Golem, kicks control over to the combat code to resolve the fight.
    '''

    def __init__ (self):
        self.name = "Rock Golem"

    def process (self, world):
        result = {}
        result["message"] = "Rock Golem has collapsed to rubble!"
        monsters = []
        n_appearing = random.randrange(1,2)
        n = 1
        while n <= n_appearing:
            monsters.append(Golem("Rock Golem "+str(n)))
            n += 1
        display.announce ("The crew is attacked by a Rock Golem!")
        combat.Combat(monsters).combat()

        return result
    
def enter (self):
        #The description has a base description, followed by variable components.
        description = "You enter the door being guarded by the Golem. Upon entering, you find yourself in a large cave."
    
        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_on_floor != None:
            description = description + f" You see a bunch of {self.item_on_floor.name} scatered around the cave floor."
        if self.item_in_clothes != None:
            description = description + f" You see a {self.item_in_clothes.name} in a pile of armour and bones laying on the cave's floor."
        display.announce (description)

def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["cave"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_on_floor == None and self.item_in_clothes == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_on_floor
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the pile of bones.")
                    config.the_player.add_to_inventory([item])
                    self.item_on_floor = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the pile of armour and bones. ...It looks like someone was slain here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")

def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north"):
            display.announce ("You enter a tunnel in the wall. You ventuer deeper into the cave.")
            config.the_player.next_loc = self.main_location.locations["Magic Door"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You walk around the cave avoiding the tunnel. It's not very interesting.")

########################
# Magic Door Room 2
########################

class SecretDoor(location.SubLocation):
    def enter (self):
        description = "After exploring the tunnel, you find yourself at a magic door with a puzzle. In order to continue, you must solve the door's puzzle."

    def __init__(self):
        self.room_number = 1
    
    def fibonacci_sequence(self, length):
        fib = [0, 1]
        while len(fib) < length:
            fib.append(fib[-1] + fib[-2])
        return fib

    def get_hint(self):
        return "The sequence follows the Fibonacci numbers."

    def check_player_guess(self, correct_sequence, player_guess):
        if correct_sequence == player_guess:
            print("\nThe door creaks open... You've unlocked the Enchanted Door!")
            return True
        else:
            print("\nThe door remains closed... The code is incorrect.")
            return False

    def transition_to_next_room(self):
        self.room_number += 1
        print(f"\nYou've entered Room {self.room_number}. A new challenge awaits!")

    def play_game(self):
        print(f"Welcome to Room {self.room_number}: The Enchanted Door Puzzle!")

        length = random.randint(3, 5)
        correct_sequence = self.fibonacci_sequence(length)
        
        print(f"\nHint: {self.get_hint()}")
        print(f"The sequence has {length} numbers. Enter them in order, separated by commas.")
        
        player_input = input("Enter your guess (numbers separated by commas): ").strip()
        
        try:
            player_guess = [int(x.strip()) for x in player_input.split(',')]
        except ValueError:
            print("\nInvalid input. Please enter only numbers separated by commas.")
            return
        
        if self.check_player_guess(correct_sequence, player_guess):
            self.transition_to_next_room()

############################
# Rock Golem pt.2 Room 3
############################

class CaveGolem (event.Event):
    '''
    A combat encounter with a Cave Golem. Similar to the Rock Golem, but stronger and bigger.
    When the event is drawn, creates a combat encounter with a Cave Golem, kicks control over to the combat code to resolve the fight.
    '''

    def __init__ (self):
        self.name = "Cave Golem"

    def process (self, world):
        result = {}
        result["message"] = "Cave Golem has collapsed to rubble!"
        monsters = []
        n_appearing = random.randrange(1,2)
        n = 1
        while n <= n_appearing:
            monsters.append(Golem2("Cave Golem "+str(n)))
            n += 1
        display.announce ("The crew is attacked by a Cave Golem!")
        combat.Combat(monsters).combat()

        return result
    
def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You leave the cave.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Boss"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You explore the the small area where you fought the Golme. There is nothing around you.")

############################
# Boss of the cave Room 4
############################

class Boss(event.Event):
    '''
    A combat encounter with the Cave Boss.
    When the event is drawn, creates a combat encounter with the Cave Boss, kicks control over to the combat code to resolve the fight.
    '''

    def __init__ (self):
        self.name = "Cave Boss"

    def process (self, world):
        result = {}
        result["message"] = "The Cave Boss has been defeated!"
        monsters = []
        n_appearing = random.randrange(1,2)
        n = 1
        while n <= n_appearing:
            monsters.append(Boss("Cave Boss "+str(n)))
            n += 1
        display.announce ("The crew is attacked by the Cave Boss!")
        combat.Combat(monsters).combat()

        return result
    
def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You leave the cave.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Treasure"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You explore the arena where you fought the boss. There is nothing around you.")

####################
# Treasure Room 5
####################

class TreasureRoom(location.SubLocation):
    def __init__(self):
        self.treasure_taken = False
        self.trap_triggered = False
        self.treasure = "Shillings"
    
    def enter_room(self):
        print("You have entered the treasure room!")
        time.sleep(1)
        print("You see a shiny treasures")
        self.ask_to_take_treasure()

    def ask_to_take_treasure(self):
        choice = input("Do you want to take the treasure? (yes/no): ").lower()
        
        if choice == "yes":
            self.take_treasure()
        elif choice == "no":
            print("You leave the treasure untouched. Safe, for now.")
        else:
            print("Invalid choice. Try again.")
            self.ask_to_take_treasure()

    def take_treasure(self):
        print("\nYou reach out and grab the treasure!")
        time.sleep(2)

        self.trap_triggered = random.choice([True, False])
        
        if self.trap_triggered:
            print("A trap is triggered! You are caught in a deadly snare!")
            self.activate_trap()
        else:
            self.treasure_taken = True
            print("You take the shillings. The room seems to calm down.")

    def activate_trap(self):
        trap_type = random.choice(["poison darts", "falling spikes", "fire burst"])
        print(f"The trap releases {trap_type}! You fail to escape!")
        self.game_over = True
        