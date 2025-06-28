# i hate circular imports
import asyncio
import random
import time
from threading import Thread
import config
from config import randSleep
def startTimerInThread():
    from controls import timer
    def run_timer():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(timer())
        loop.close()
    t = Thread(target=run_timer, daemon=True)
    t.start()

def startInputLoop():
    import controls
    async def Main():
        await controls.inputLoop()

    def RunLoop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(Main())
        loop.close()

    thread = Thread(target=RunLoop)
    thread.start()
    return thread

def mainGameplayLoop():  # active while you are not in a saferoom and alive
    from room import generateRoom
    from entity import entitySpawner
    config.timeRemaining = config.SFTime
    config.roomsRemaining = 15 + min(40, config.saferoom * 3)  # set roomsRemaining to a maximum of 55
    config.gameOn = True  # sets gameOn to true
    t = Thread(target=startInputLoop, daemon=False)  # input async loop in a thread
    t.start()
    config.currentRoomType = list(generateRoom(1))[0]
    config.nextThreeRooms.append(config.currentRoomType)
    config.nextThreeRooms.extend(generateRoom(2))
    print(f"current room type is {config.currentRoomType}")
    print(f"the next rooms are: {config.nextThreeRooms[0].roomIdentifier}, {config.nextThreeRooms[1].roomIdentifier} and {config.nextThreeRooms[2].roomIdentifier}")
    startTimerInThread()  # starts timer
    while config.gameOn:  # loop for entity spawning
        time.sleep(random.randint(1,10))
        entitySpawner()

def main():
    from inventory import flashlight, lamp
    print("heres how this works")
    randSleep(10, 100)
    print("\n \n \n \n \n \n")
    print(f"controls: \ncrouch: c\nforward: w\nleft: a\nback: s\nright: d\nrun: r\ncheck your current information: "
          f"info\nenter/exit inventory: i\nselect an inventory item: press the key according to the slot"
          f"\nuse selected item: f\n pick up an item: p")
    randSleep(10, 100)
    print("you need to move from room to room and go through as many saferooms until you inevitably die")
    randSleep(10, 100)
    print("walking in a direction makes you look in that direction")
    randSleep(10, 100)
    print("type the letter twice if you want to move in a direction without looking in that direction")
    randSleep(10, 100)
    print("walking forward has a dedicated key for it, which is the run key")
    randSleep(10, 100)
    print("running has the same speed as walking forward")
    randSleep(10, 100)
    print("you must be in the middle of the room to move on to the next one")
    randSleep(10, 100)
    print("you can't go to passed rooms")
    randSleep(10, 100)
    print("you can't move while your inventory is open")
    randSleep(10, 100)
    print("you will start with the lamp equipped and a flashlight in your inventory")
    randSleep(10, 100)
    print("you can't receive room information without the lamp equipped")
    randSleep(10, 100)
    print("you will find holy water in rooms that have hiding spots in them, press p to pick it up.")
    randSleep(10, 100)
    print("it will help you against heed or slight if you get hit by them")
    randSleep(10, 100)
    print("")
    print("entities:")
    randSleep(10, 100)
    print("1. tosleepforgood: stay down, don't move a muscle.")
    randSleep(10, 100)
    print("2. soulfulgratitude: the water withers the soul, stay still and it won't sense you.")
    randSleep(10, 100)
    print("3. jabłoń: run onwards, you'll find a spot.")
    randSleep(10, 100)
    print("4. eyeforaneye: don't stare.")
    randSleep(10, 100)
    print("5. STAREDOWN: do stare.")
    randSleep(10, 100)
    print("6. peerpressure: move to the side, out of its way.")
    randSleep(10, 100)
    print("7. ALWAYSSUFFER: good luck.")
    randSleep(10, 100)
    print("8. lefttowander: watch your back from time to time, it's scared of light")
    randSleep(10, 100)
    input("press enter to start the game")
    print("starting game. . .")
    # initial game setup
    config.inventory.append(lamp)  # add lamp and flashlight to the starting player inventory
    config.inventory.append(flashlight)
    config.currentItem = lamp  # set current item to lamp
    mainGameplayLoop()  # starts main gameplay loop


if __name__ == "__main__":
    main()
