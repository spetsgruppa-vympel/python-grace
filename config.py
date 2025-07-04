# configuration file
# stores things that don't need to be imported from other files
import asyncio
import random
import time

# general bools
gameOn = False  # active while the game is running
devMode = True  # dictates whether devmode is activated or not, devmode makes you unkillable and disables randsleep
playerTagged = False  # dictates whether the player was tagged by heed or slight
inSaferoom = False  # whether the player is in the saferoom or not
crouching = False  # whether the player is crouching

# room-related variables
direction = 0  # stores the direction the player is looking based on last movement: 0/12 = forward, 3 = right, 6 = back, 9 = left
location = 0  # stores whether the player is located on the left (-1), middle (0) or right (1)
saferoom = 0  # number of saferooms passed
SFTime = 60  # time in seconds the player has after leaving the saferoom to reach the next saferoom before goatman spawns
timeRemaining = 0  # the remaining time of the player
currentRoom = 0  # the room you are between the saferooms
roomsRemaining = 0  # the remaining rooms until the next saferoom
roomsPassed = 0  # the rooms that have been passed in total
slightRoom = 0  # room slight spawned in
heedRoom = 0  # room heed spawned in
longRoomTicked = False  # stores if you are in the first or second part of a long room
currentRoomType = 0  # stores the current room type of the player
nextThreeRooms = []  # stores the next three rooms
firstTime = True  # first time setup?

# entity related bools
dozerOn = True  # dictates whether the entity dozer is activated
sorrowOn = True  # dictates whether the entity sorrow is activated
heedOn = True  # dictates whether the entity heed is activated
slightOn = True  # dictates whether the entity slight is activated
slugfishOn = True  # dictates whether the entity slugfish is activated
goatmanOn = True  # dictates whether the entity goatman is activated
carnationOn = True  # dictates whether the entity carnation is activated
rueOn = True  # dictates whether the entity rue is activated
rueRemainingTime = 0  # stores how much more time before rue attacks
goatmanRemainingTime = 0  # ditto for goatman
rueDirection = 0  # the direction rue has
goatmanDirection = 0  # the direction goatman has
rueFlashed = False  # stores whether rue is flashed
goatmanFlashed = False  # stores whether goatman is flashed

# inventory stuff
inventory = []  # stores the current inventory of the player
currentItem = 0  # stores the current item held by the player
inventoryOpen = False  # stores whether the inventory is open. you can't move if it is.
holywaterPicked = False  # stores whether holy water was picked in the saferoom


# mainInput stuff
mainInput = None  # manages the player chat input
mainInputLock = asyncio.Lock()
mainInputCondition = asyncio.Condition(lock=mainInputLock)


async def setMainInput(recInput):
    # print("setMainInput run")
    global mainInput
    # print(mainInputCondition.locked())
    async with mainInputCondition:  #
        # print("async with mainInputCondition (setMainInput)")
        mainInput = recInput  # set recInput (receivedInput) to mainInput
        mainInputCondition.notify_all()  # wake up the threads


def randSleep(a, b):  # randomized sleep function
    if not devMode:
        time.sleep(float(random.randint(a, b) / 100))

def slowPrint(text, delay=0.2):
    global gameOn
    gameOn = False
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def playerDead(deathBy):  # manages the player's death and ends the game
    global gameOn
    gameOn = False
    slowPrint(f"you died to {deathBy}. \nyou can always try again,\ni am here to help you,\ni know it's really hard but you will succeed eventually,\nand what awaits you when you do is great,\nbut i won't force you to do anything.\ngoodbye for now, i will always be here for you\nwhen you need and want me.")
    exit("dead")

