# i hate circular imports
import asyncio
import config
from config import randSleep


def startTimerInThread():
    from controls import timer
    asyncio.run(timer())


def mainGameplayLoop():  # active while you are not in a saferoom and alive
    from room import roomGenerator
    from room import generateRoom
    from controls import inputLoop
    config.timeRemaining = config.SFTime
    config.roomsRemaining = 15 + min(40, config.saferoom)
    config.gameOn = True
    roomGenerator()  # generate the first three rooms
    config.currentRoomType = config.nextThreeRooms.pop(0)
    # ^ gens the first room type and removes it from next three rooms
    config.nextThreeRooms.extend(list(generateRoom(1)))  # gens another room to compensate for the first room's removal
    asyncio.run(inputLoop())
    startTimerInThread()  # starts timer
    while config.gameOn:
        pass  # TODO: entity spawn


def main():
    print("heres the tutorial")
    randSleep(10, 100)
    print("\n \n \n \n \n \n")
    print("controls: \ncrouch: c\nforward: w\nleft: a\nback: s\nright: d\nrun: r\ncheck information: info")
    randSleep(10, 100)
    print("walking in a direction makes you look in that direction")
    randSleep(10, 100)
    print("type the letter twice if you want to move in a direction without looking in it")
    randSleep(10, 100)
    print("walking forward has a dedicated key for it, which is run")
    randSleep(10, 100)
    print("running has the same speed as walking forward")
    randSleep(10, 100)
    print("you must be in the middle of the room to move on to the next one")
    randSleep(10, 100)
    print("you can't go to passed rooms")
    randSleep(10, 100)
    randSleep(10, 100)
    print("")
    print("entities:")
    randSleep(10, 100)
    print("1. tosleepforgood: stay down, don't move a muscle.")
    print("2. soulfulgratitude: the water withers the soul, stay still and it won't sense you.")
    print("3. jabłoń: run onwards, you'll find a spot.")
    print("4. eyeforaneye: don't stare.")
    print("5. STAREDOWN: do stare.")
    print("6. peerpressure: move to the side, out of its way.")
    print("7. ALWAYSSUFFER: good luck.")
    randSleep(10, 100)
    print("8. lefttowander: watch your back from time to time, it's scared of light")
    randSleep(10, 100)
    mainInput = str(input("press enter to start the game"))
    print("starting game. . .")
    # initial game setup
    mainGameplayLoop()

if __name__ == "__main__":
    main()

# TODO LIST: inputHandler to handle and validate inputs received: DONE
# TODO LIST: finish room generation system: DONE
# TODO LIST: implement currentRoom and currentRoomType: DONE
# TODO LIST: implement entity spawning system: NEEDS SPAWN CONDITION
# TODO LIST: kill all entities when saferoom is entered (they can still kill the player): DELAYED FK THAT
# TODO LIST: finish controls: done but real men play without look controls
# TODO LIST: put in more files AND FIX THE CIRCULAR IMPORTS: done
# TODO LIST: implement inventory and rue (ily rue)
# TODO LIST: comment code better (typing benchmark go brrr)
# TODO LIST: playtest
# TODO LIST: ability to go back to previous rooms (prevRoom)
# TODO LIST: kill myself: in preparation

# meow

