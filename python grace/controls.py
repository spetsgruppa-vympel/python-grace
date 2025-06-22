# stores movement-related stuff, it's not an actual class tho no reason for me to make one lol
# good thing this class contains only functions omc i hate circular imports i want to kill myself
import asyncio
import threading

import config


async def timer():
    print(
        f"the timer has started, you have 40 seconds to get to the saferoom and {config.roomsRemaining} rooms. good luck.")
    config.timeRemaining = config.SFTime
    while config.timeRemaining > 0:
        await asyncio.sleep(1)
        config.timeRemaining -= 1


def crouch():  # manages crouching
    if config.crouching:  # if already crouching, uncrouch
        config.crouching = False
    else:  # otherwise crouch
        config.crouching = True


def forward():  # manages moving forward
    from room import longRoom, longSafeRoom, longHidingSpot, normalSafeRoom
    from room import nextRoom
    config.direction = 0
    if config.currentRoomType in [longRoom, longSafeRoom, longHidingSpot]:
        if not config.currentRoomType == longSafeRoom:  # for non-saferoom rooms, put longRoomTicked to True or advance
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
    if config.longRoomTicked:  # if in the second part of a long room, go back to the first part
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
    from room import nextRoom
    from room import longRoom, longSafeRoom, longHidingSpot, normalSafeRoom
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


async def inputLoop():
    listenerTask = asyncio.create_task(inputListener())
    while config.gameOn:
        userInput = await asyncio.to_thread(input, "")
        await config.setMainInput(userInput)
    await listenerTask


async def inputListener():  # listens for input
    # print("movement inputListener activated")
    from config import gameOn, mainInputCondition
    from entity import sorrowSpawned
    while gameOn and not sorrowSpawned:
        # print("movement inputlistener goodCheck")
        async with mainInputCondition:
            # print("movement inputListener async with mainInput")
            # print(mainInputCondition.locked())
            await mainInputCondition.wait()  # wait for input to change
            # print("mainInputCondition awaited")
            await inputHandler()
            # print("inputHandler awaited")


async def inputHandler():  # handles game input and redirects to the adequate function
    # print("inputHandler")
    import config
    if config.mainInput == "w":
        if not config.crouching:
            forward()
            # print("MOVED FORWARD YAY")
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
        print(f"you have {config.roomsRemaining} rooms remaining until saferoom {config.saferoom + 1},")
        print(f"you are facing {directionDictionary[config.direction]}, current room type is {config.currentRoomType}")
        print(
            f"you are in the {locationDictionary[config.location]} of the room and have {config.timeRemaining} time remaining")
        if config.roomsRemaining >= 3:
            print(
                f"the next rooms are: {config.nextThreeRooms[0].roomIdentifier}, {config.nextThreeRooms[1].roomIdentifier} and {config.nextThreeRooms[2].roomIdentifier}")
        elif config.roomsRemaining == 2:
            print(f"the next rooms are: {config.nextThreeRooms[0]} and the saferoom")
        else:
            print(f"you have one more room, the saferoom")
    elif config.mainInput == 0:
        pass
    else:
        print("that's not a valid input")
        config.mainInput = 0


def saferoomEnter():
    from main import mainGameplayLoop
    config.timeRemaining = config.SFTime
    config.inSaferoom = True
    config.currentRoom = 0
    config.roomsRemaining = min(3 * config.saferoom, 25) + 20  # max rooms is 55
    config.saferoom += 1  # increment saferoom
    config.location = 0  # reset location
    config.direction = 0  # reset direction
    config.currentRoomType = 0  # reset current room type
    resetTimer()  # reset timer
    print(
        f"you have entered saferoom number {config.saferoom}, you are at {config.roomsPassed} rooms passed, press enter to move on")
    config.mainInput = input("")
    mainGameplayLoop()  # restarts main gameplay loop


timerTask = None  # stores the timer task


def resetTimer():
    from main import startTimerInThread
    global timerTask
    if timerTask is not None and timerTask.is_alive():
        # start new thread
        timerTask = threading.Thread(target=startTimerInThread, daemon=True)

# meow
