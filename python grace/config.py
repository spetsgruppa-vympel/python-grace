# configuration file
# stores essential variables
import asyncio
import random
import time

gameOn = False  # active while the game is running
devMode = True  # dictates whether devmode is activated or not, devmode makes you unkillable and disables randsleep
playerTagged = False  # dictates whether the player was tagged by heed or slight
inSaferoom = False  # whether the player is in the saferoom or not
crouching = False  # whether the player is crouching
rueSpawned = False  # stores whether the entity rue has spawned (duplicate spawns are not allowed)

direction = 0  # stores the direction the player is looking based on last movement: 0/12 = forward, 3 = right, 6 = back, 9 = left
location = 0  # stores whether the player is located on the left (-1), middle (0) or right (1)
saferoom = 0  # number of saferooms
SFTime = 80  # time in seconds the player has after leaving the saferoom to reach the next saferoom before goatman spawns
timeRemaining = 0  # the remaining time of the player
currentRoom = 0  # the room you are between the saferooms
roomsRemaining = 0  # the remaining rooms until the next saferoom
roomsPassed = 0  # the rooms that have been passed in total
slightRoom = 0  # room slight spawned in
heedRoom = 0  # room heed spawned in

currentRoomType = 0  # stores the current room type of the player
nextThreeRooms = []  # stores the next three rooms
inventory = []  # manages the inventory

longRoomTicked = None  # stores if you are in the first or second part of a long room
dozerOn = False  # dictates whether the entity dozer is activated
sorrowOn = False  # dictates whether the entity sorrow is activated
heedOn = False  # dictates whether the entity heed is activated
slightOn = False  # dictates whether the entity slight is activated
slugfishOn = False  # dictates whether the entity slugfish is activated
goatmanOn = False  # dictates whether the entity goatman is activated
carnationOn = False  # dictates whether the entity carnation is activated
mainInput = None  # manages the player chat input
mainInputCondition = asyncio.Condition()

async def setMainInput(recInput):
    global mainInput
    async with mainInputCondition:
        mainInput = recInput
        mainInputCondition.notify_all()  # wake up

def randSleep(a, b):  # randomized sleep function
    if not devMode:
        time.sleep(float(random.randint(a, b) / 100))


def playerDead(deathBy):  # manages the player's death and ends the game
    print(f"you died to {deathBy}")
    print(f"you can always try again. \ni gave you free will, although\nit's probably in your best interest to do so,\n"
          f"better to suffer while you're still alive,\nand not for eternity after.")
    exit("dead")  # TODO: will be replaced later with replayability feature and entity jumpscares
