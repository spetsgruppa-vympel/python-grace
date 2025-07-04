# stores movement-related stuff, it's not an actual class tho no reason for me to make one lol
# good thing this class contains only functions omc i hate circular imports i want to kill myself
import asyncio
import time

import config


async def timer():
    from entity import goatmanSpawn
    print(
        f"the timer has started, you have 60 seconds to get to the saferoom and {config.roomsRemaining} rooms. good luck.")
    config.timeRemaining = config.SFTime
    while config.timeRemaining > 0 and config.gameOn:
        await asyncio.sleep(1)
        config.timeRemaining -= 1
    if config.gameOn:
        goatmanSpawn()


def crouch():  # manages crouching
    if config.crouching:  # if already crouching, uncrouch
        config.crouching = False
    else:  # otherwise crouch
        config.crouching = True


def forward():  # manages moving forward
    from room import longRoom, longSafeRoom, longHidingSpot, normalSafeRoom, nextRoom
    config.direction = 0
    if config.roomsRemaining >= 1:
        if config.currentRoomType in [longRoom, longSafeRoom, longHidingSpot]:
            if not config.currentRoomType is longSafeRoom:  # for non-saferoom rooms, put longRoomTicked to True or advance
                # print("not longSafeRoom")
                if not config.longRoomTicked:  # sets longRoomTicked to True, else advances
                    config.longRoomTicked = True
                    # print("longRoomTicked = True")
                elif config.longRoomTicked:  # advances to next room
                    config.longRoomTicked = False
                    # print("advance long room")
                    nextRoom()
            else:  # if longSafeRoom and longRoomTicked is True, enters saferoom, otherwise sets longRoomTicked to True
                if config.longRoomTicked:  # enter saferoom
                    config.longRoomTicked = False
                    saferoomEnter()
                else:
                    # print("longRoomTicked = True for saferoom")
                    config.longRoomTicked = True
        elif config.currentRoomType is normalSafeRoom:
            saferoomEnter()
        else:
            # print("not long room")
            nextRoom()
    else:
        saferoomEnter()


def backwards():
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
    from room import longRoom, longSafeRoom, longHidingSpot, normalSafeRoom
    from room import nextRoom
    if config.roomsRemaining >= 1:
        if config.currentRoomType in [longRoom, longSafeRoom, longHidingSpot]:
            if not config.currentRoomType is longSafeRoom:  # for non-saferoom rooms, put longRoomTicked to True or advance
                # print("not longSafeRoom")
                if not config.longRoomTicked:  # sets longRoomTicked to True, else advances
                    config.longRoomTicked = True
                    # print("longRoomTicked = True")
                elif config.longRoomTicked:  # advances to next room
                    config.longRoomTicked = False
                    # print("advance long room")
                    nextRoom()
            else:  # if longSafeRoom and longRoomTicked is True, enters saferoom, otherwise sets longRoomTicked to True
                if config.longRoomTicked:  # enter saferoom
                    config.longRoomTicked = False
                    saferoomEnter()
                else:
                    # print("longRoomTicked = True for saferoom")
                    config.longRoomTicked = True
        elif config.currentRoomType is normalSafeRoom:
            saferoomEnter()
        else:
            # print("not long room")
            nextRoom()
    else:
        saferoomEnter()


def moveBackwards():
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
    # start the listener
    listenerTask = asyncio.create_task(inputListener())
    while True:
        # read user input forever
        userInput = await asyncio.to_thread(input, "")
        await config.setMainInput(userInput)


async def inputListener():  # listens for input
    # print("movement inputListener activated")
    import entity
    from config import mainInputCondition
    while True:  # outer loop to ensure restart
        # print("movement inputlistener goodCheck")
        async with mainInputCondition:
            # print("movement inputListener async with mainInput")
            # print(mainInputCondition.locked())
            await mainInputCondition.wait()  # wait for input to change
            # print("mainInputCondition awaited")
            await inputHandler()
            # print("inputHandler awaited")


# noinspection PyUnresolvedReferences
async def inputHandler():  # handles game input and redirects to the adequate function
    # print("inputHandler")
    from inventory import openCloseInventory, mainInventory, holyWater, lamp, flashlight
    from room import mainRoom
    from config import currentItem
    if config.mainInput == "w":  # move forward
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            forward()
            # print("MOVED FORWARD")
    elif config.mainInput == "a":  # move left
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            left()
    elif config.mainInput == "s":  # move back
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            backwards()
    elif config.mainInput == "d":  # move right
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            right()
    elif config.mainInput == "ww":  # move forward without looking
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            moveForward()
    elif config.mainInput == "aa":  # move left without looking
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            moveLeft()
    elif config.mainInput == "ss":  # move back without looking
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            moveBackwards()
    elif config.mainInput == "dd":  # move right without looking
        if not config.crouching or config.inventoryOpen:
            config.rueFlashed = False
            moveRight()
    elif config.mainInput == "i":  # open/close inventory
        config.rueFlashed = False
        openCloseInventory()
    elif config.mainInput in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:  # select inventory slot
        config.rueFlashed = False
        print(config.inventoryOpen)
        if config.inventoryOpen:  # if inventory is open
            index = int(config.mainInput) - 1  # convert to int in order to prevent typeError
            config.currentItem = config.inventory[index]
            print(f"equipped {config.currentItem}")
    elif config.mainInput == "f":  # use selected inventory item
        config.rueFlashed = False
        if getattr(config.currentItem, "useEffect",
                   False) and config.inventoryOpen:  # run the useEffect if the currentItem has it
            config.currentItem.use()
    elif config.mainInput == "p":  # pick up item in room
        config.rueFlashed = False
        if getattr(config.currentRoomType, "hidingSpot",
                   False) and config.inventoryOpen:  # if currentRoomType is not a hiding spot
            print("there's nothing here to pick up")
        else:  # print
            if config.holywaterPicked:
                print("you already took the holy water here")
            else:
                config.inventory.append(holyWater)
                config.holywaterPicked = False
    elif config.mainInput == "info":
        config.rueFlashed = False
        if currentItem == lamp:
            print(f"you have {config.roomsRemaining} rooms remaining until saferoom {config.saferoom + 1},")
            print(
                f"you are facing {directionDictionary[config.direction]}, current room type is {config.currentRoomType}")
            print(
                f"you are in the {locationDictionary[config.location]} of the room and have {config.timeRemaining} time remaining")
            if config.roomsRemaining >= 3:
                print(
                    f"current room type is -{config.currentRoomType}- and the next rooms are: {config.nextThreeRooms[0].roomIdentifier}, {config.nextThreeRooms[1].roomIdentifier} and {config.nextThreeRooms[2].roomIdentifier}")
            elif config.roomsRemaining == 2:
                print(f"the next rooms are: {config.nextThreeRooms[0]} and {config.nextThreeRooms[1]}")
            else:
                print(f"you have one more room, the {config.nextThreeRooms[0]}")
        print()
    elif config.mainInput == 0:
        pass
    else:
        print("that's not a valid input")
        config.mainInput = 0


def saferoomEnter():
    from main import mainGameplayLoop
    config.timeRemaining = config.SFTime
    config.gameOn = False
    config.currentRoom = 0
    config.roomsRemaining = 30 + min(40, config.saferoom * 3)  # max rooms is 55
    config.saferoom += 1  # increment saferoom
    config.location = 0  # reset location
    config.direction = 0  # reset direction
    config.currentRoomType = 0  # reset current room type
    config.timeRemaining = 60  # reset timer
    print(f"you have entered saferoom number {config.saferoom}, you are at {config.roomsPassed} rooms passed,  "
          f"you'll move on in 5 seconds")
    time.sleep(1)
    mainGameplayLoop()  # restarts main gameplay loop
    print(config.gameOn)


timerTask = None  # stores the timer task

# meow
