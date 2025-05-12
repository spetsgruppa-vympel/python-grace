# stores movement-related stuff
# good thing this class contains only functions omc i hate circular imports i want to kill >
# > whoever invented them

import asyncio
import threading
import config
from config import roomsRemaining
from roomGen import nextRoom, saferoomEnter
from roomStorageClass import longRoom, normalSafeRoom, longHidingSpot, longSafeRoom
from entityStorageClass import sorrowSpawned
timerTask = None  # stores the timer task

def inputListener():  # reads input and redirects the player input to inputHandler()
    def listen():
        while config.gameOn and not sorrowSpawned:  # listen for input while gameOn is active
            config.mainInput = input("")
            inputHandler()  # redirects input to be interpreted by inputHandler()

    listenerThread = threading.Thread(target=listen, daemon=True)
    listenerThread.start()


async def timer():
    print(f"the timer has started, you have 40 seconds to get to the saferoom and {roomsRemaining} rooms. good luck.")
    config.timeRemaining = config.SFTime
    while config.timeRemaining > 0:
        await asyncio.sleep(1)
        config.timeRemaining -= 1


def startTimerInThread():
    asyncio.run(timer())


def resetTimer():
    global timerTask
    if timerTask is not None and timerTask.is_alive():
        # start new thread
        timerTask = threading.Thread(target=startTimerInThread, daemon=True)


def inputHandler():  # handles game input and redirects to the adequate function
    if config.mainInput == "w":
        if not config.crouching:
            forward()
    elif config.mainInput == "a":
        if not config.crouching:
            left()
    elif config.mainInput == "s":
        if not config.crouching:
            backwards()
    elif config.mainInput == "d":
        if not config.crouching:
            right()
    elif config.mainInput == "ww":
        if not config.crouching:
            moveForward()
    elif config.mainInput == "aa":
        if not config.crouching:
            moveLeft()
    elif config.mainInput == "ss":
        if not config.crouching:
            moveBackwards()
    elif config.mainInput == "dd":
        if not config.crouching:
            moveRight()
    elif config.mainInput == "c":
        crouch()
    elif config.mainInput == "info":
        print(f"you have {roomsRemaining} rooms remaining until saferoom {config.saferoom + 1},")
        print(f"you are facing {directionDictionary[config.direction]}, current room type is {config.currentRoomType}")
        print(f"you are in the {locationDictionary[config.location]} of the room and have {config.timeRemaining} time remaining")
    else:
        print("that's not a valid input")


def crouch():  # manages crouching
    if config.crouching:  # if already crouching, uncrouch
        config.crouching = False
    else:  # otherwise crouch
        config.crouching = True


def forward():  # manages moving forward
    config.direction = 0
    if config.currentRoomType in [longRoom, longSafeRoom, longHidingSpot]:
        if not longSafeRoom:  # for non-saferoom rooms, put longRoomTicked to True or advance
            if not config.longRoomTicked:  # sets longRoomTicked to True, else advances
                config.longRoomTicked = True
            else:  # advances to next room
                config.longRoomTicked = False
                nextRoom()
        else:  # if longSafeRoom and longRoomTicked is True, enters saferoom, otherwise sets longRoomTicked to True
            if config.longRoomTicked:  # enter saferoom
                config.longRoomTicked = False
                saferoomEnter()
            else:
                config.longRoomTicked = True
    elif config.currentRoomType == normalSafeRoom:
        saferoomEnter()
    else:
        nextRoom()


def backwards():  # TODO: implement going to previous rooms
    if config.longRoomTicked: # if in the second part of a long room, go back to the first part
        config.longRoomTicked = False
    config.direction = 6


def left():  # manages moving left, sets direction and location
    config.direction = 9
    if config.location != -1:
        config.location -= 1
    else:
        print("you are already on the left side of the room")


def right():  # manages moving right, sets direction and location
    config.direction = 3
    if config.location != 1:
        config.location += 1
    else:
        print("you are already on the right side of the room")


def moveForward():  # manages moving forward without looking
    if config.currentRoomType in [longRoom, longSafeRoom, longHidingSpot]:
        if not longSafeRoom:  # for non-saferoom rooms, put longRoomTicked to True or advance
            if not config.longRoomTicked:  # sets longRoomTicked to True, else advances
                config.longRoomTicked = True
            else:  # advances to next room
                config.longRoomTicked = False
                nextRoom()
        else:  # if longSafeRoom and longRoomTicked is True, enters saferoom, otherwise sets longRoomTicked to True
            if config.longRoomTicked:  # enter saferoom
                config.longRoomTicked = False
                saferoomEnter()
            else:
                config.longRoomTicked = True
    elif config.currentRoomType == normalSafeRoom:
        saferoomEnter()
    else:
        nextRoom()


def moveBackwards():  # TODO: implement going to previous rooms
    if config.longRoomTicked:  # if in the second part of a long room, go back to the first part
        config.longRoomTicked = False
    else:
        print("you can't go to previous rooms")


def moveLeft():
    if config.location != -1:
        config.location -= 1
    else:
        print("you are already on the left side of the room")


def moveRight():
    if config.location != 1:
        config.location += 1
    else:
        print("you are already on the right side of the room")


locationDictionary = {
    0: "middle",
    1: "right side",
    -1: "left side"
}
directionDictionary = {
    0: "forward",
    3: "right",
    6: "back",
    9: "left"
}
