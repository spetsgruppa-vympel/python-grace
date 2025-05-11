import random
import time
import config
import entityStorageClass
import roomStorageClass
from entityStorageClass import dozer, sorrow, rue, heed, slight, slugfish, goatman, carnation, entityTypes, \
    carnationSpawned
from movementClass import inputListener, startTimerInThread, resetTimer
from roomStorageClass import longRoom, normalHidingSpot, normalSafeRoom, longHidingSpot, longSafeRoom, \
    randomlyGeneratedRooms


def dozerSpawn():  # dozer spawn function
    if not entityStorageClass.dozerSpawned and dozer.spawnsFrom >= config.saferoom:
        entityStorageClass.dozerSpawned = True
        print("stay down, don't move")
        randSleep(80, 200)
        time.sleep(dozer.checkTime)  # wait the time specified
        if config.mainInput != "c":  # kill check, kills if the player is not crouching
            playerDead("dozer")  # calls playerDead with the death method dozer
        entityStorageClass.dozerSpawned = False
        if config.gameOn:
            print("dozer has despawned")
    else:
        entitySpawner()


def sorrowSpawn():  # sorrow spawn function
    if not entityStorageClass.sorrowSpawned and sorrow.spawnsFrom >= config.saferoom:
        entityStorageClass.sorrowSpawned = True
        config.mainInput = False  # if sorrowSpawned is true, inputlistener stops
        config.mainInput = input("stay silent, don't make one sound")  # this is done to make sure you can't input anything
        randSleep(80, 200)  # between spawn and the kill check and get away with it
        time.sleep(sorrow.checkTime)  # wait the time specified
        if config.mainInput:  # kill check, checks if the player has moved at all during the interval
            playerDead("sorrow")  # calls playerDead with the death method sorrow
        if config.gameOn:
            print("sorrow has despawned, you can move now")
            entityStorageClass.sorrowSpawned = False
            inputListener()  # restarts input listener
    else:
        entitySpawner()


def heedSpawn():  # heed spawn function
    if not entityStorageClass.heedSpawned and entityStorageClass.slightSpawned:
        entityStorageClass.heedSpawned = True
        heedDirection = 3 * random.randint(0, 3)
        print("look into the eye, it's in a few rooms")
        while config.heedRoom > config.currentRoom:
            time.sleep(0.1)
        if config.heedRoom == config.currentRoom and heedDirection != config.direction:  # kill check, if the player isn't looking in
            if config.playerTagged:
                playerDead("slight")  # calls playerDead by slight
            else:
                config.playerTagged = True
                print("you were tagged by heed, look into the eye, next time you will die")
            if config.gameOn:
                print("heed has despawned")
                entityStorageClass.heedSpawned = False
    else:
        entitySpawner()



def slightSpawn():  # slight spawn function
    if not entityStorageClass.slightSpawned and entityStorageClass.heedSpawned:
        entityStorageClass.slightSpawned = True
        slightDirection = 3 * (random.randint(0, 3))  # the location of the eye
        print("don't look into the eye, it's in a few rooms")
        if config.slightRoom == config.currentRoom and slightDirection == config.direction:
            if config.playerTagged:
                playerDead("slight")
            else:
                config.playerTagged = True
                print("you were tagged by slight, don't look into the eye, next time you will die")
        if config.gameOn:
            print("slight has despawned")
            entityStorageClass.slightSpawned = False
    else:
        entitySpawner()


def slugfishSpawn():  # slugfish spawn function
    if not entityStorageClass.slugfishSpawned:
        print("slugfish has spawned, hug the wall")
        time.sleep(slugfish.checkTime)
        if config.location == 0:  # kills the player if they are in the middle of the room
            playerDead("slugfish")
        if config.gameOn:
            print("slugfish has despawned")
            entityStorageClass.slugfishSpawned = False
    else:
        entitySpawner()


def goatmanSpawn():  # goatman spawn function
    if not entityStorageClass.goatmanSpawned:
        entityStorageClass.goatmanSpawned = True
        print("HIdeNOw")
        while not config.inSaferoom:
            print("HIdeNOw")
            time.sleep(goatman.checkTime)
            #TODO: implement kill check


def rueSpawn():  # rue spawn function
    if not config.rueSpawned:
        config.rueSpawned = True
        print("rue has spawned, watch your back and flash it when it gets close")
        for i in range(rue.recAmount):
            pass  # TODO: implement kill check
    if config.gameOn:
        print("rue has despawned")
        config.rueSpawned = False


def carnationSpawn():  # carnation spawn function
    if not entityStorageClass.carnationSpawned and not entityStorageClass.dozerSpawned and not entityStorageClass.sorrowSpawned:
        entityStorageClass.carnationSpawned = True
        print("carnation has spawned, run forwards, you will find a hiding room")
        if config.gameOn:
            print("carnation has despawned")
            entityStorageClass.carnationSpawned = False
    else:
        entitySpawner()

def entitySpawner():  # main entity spawner function
    #TODO: finish(ed?)
    def entityOperator(): # decides the entity to be spawned
        candidateEntity = random.choice(entityTypes) # randomly chooses an entity
        if candidateEntity.mainEntity.spawnsFrom >= config.saferoom: # checks if the entity is allowed to spawn
            return candidateEntity # yields the entity
        else:
            entityOperator() # reruns if spawn is not allowed
    spawningEntity = entityOperator()
    if spawningEntity.spawnsWhere <= 0: # if the spawning entity spawns in the back or current room, >
        spawnDictionary.get(spawningEntity, lambda: None)() # > fetch the spawn function from the entity dictionary
    else:
        if spawningEntity == slight:
            config.slightRoom = min(config.roomsRemaining, 3)
            spawnDictionary.get(spawningEntity, lambda: None)()
        elif spawningEntity == heed:
            config.heedRoom = min(config.roomsRemaining, 3)
            spawnDictionary.get(spawningEntity, lambda: None)()


# > need to be specified when calling roomGenerator to be generated


def randSleep(a, b):  # randomized sleep function
    if not config.devMode:
        time.sleep(float(random.randint(a, b) / 100))


def playerDead(deathBy):  # manages the player's death and ends the game
    print(f"you died to {deathBy}")
    print(f"you can always try again. \ni gave you free will, although\nit's probably in your best interest to do so,\n"
          f"better to suffer while you're still alive,\nand not for eternity after.")
    exit("dead")  # TODO: will be replaced later with replayability feature and entity jumpscares


def nextRoom():
    if config.location == 0: # checks first whether in the middle of the room
        if len(config.nextThreeRooms) >= 1: # checks if nextThreeRooms has one or more rooms left
            config.currentRoomType = config.nextThreeRooms.pop(0)
        else: # else generates another set and reruns the function
            roomGenerator()
            nextRoom()
        config.roomsPassed += 1 # increases roomsPassed
        config.roomsRemaining -= 1 # increases roomsRemaining
        config.currentRoom += 1 # increases currentRoom
    else:
        if config.currentRoomType == [longRoom, longSafeRoom, longHidingSpot]:
            config.longRoomTicked = True
        print("you need to be in the middle to move to the next room")


def generateRoom(amount, specificRoom1=None, specificRoom2=None):  # yields (amount) rooms>
    for i in range(amount):  # > specificRoom1 will always be generated before 2>
        yield random.choice(randomlyGeneratedRooms)  # > and they both generate after the random rooms
    # sorts out the specified room to be generated from mainRoom for specificRoom1
    if specificRoom1 and roomStorageClass.mainRoom:
        if specificRoom2.roomStorageClass.mainRoom.isLongRoom and specificRoom2.roomStorageClass.mainRoom.isSaferoom:
            yield longSafeRoom  # check the properties of the object and yield longsaferoom
        elif specificRoom2.roomStorageClass.mainRoom.isLongRoom and specificRoom2.roomStorageClass.mainRoom.hidingSpot:
            yield longHidingSpot  # check the properties of the object and yield longhidingspot
        elif specificRoom2.roomStorageClass.mainRoom.hidingSpot:
            yield normalHidingSpot  # check the properties of the object and yield hidingspot
        elif specificRoom2.roomStorageClass.mainRoom.isLongRoom:
            yield longRoom  # check the properties of the object and yield longroom
        elif specificRoom2.roomStorageClass.mainRoom.isSaferoom:
            yield normalSafeRoom  # check the properties of the object and yield normalsaferoom
        else:
            print("specificroom1 received undefined input")
    # yeah this kinda sucks i dont like long lines either >
    # > but not much i can do the other option was to have everything in one file
    # ditto for specificRoom2
    if specificRoom2 and roomStorageClass.mainRoom:
        if specificRoom2.mainRoom.isLongRoom and specificRoom2.roomStorageClass.mainRoom.isSaferoom:
            yield longSafeRoom
        elif specificRoom2.roomStorageClass.mainRoom.isLongRoom and specificRoom2.roomStorageClass.mainRoom.hidingSpot:
            yield longHidingSpot
        elif specificRoom2.roomStorageClass.mainRoom.hidingSpot:
            yield normalHidingSpot
        elif specificRoom2.roomStorageClass.mainRoom.isLongRoom:
            yield longRoom
        elif specificRoom2.roomStorageClass.mainRoom.isSaferoom:
            yield normalSafeRoom
        else:
            print("specificroom2 received undefined input")



def roomGenerator():  # generates the next three rooms
    config.nextThreeRooms = []
    if config.roomsRemaining > 3 and not carnationSpawned:  # randomly generate three rooms
        config.nextThreeRooms.extend(list(generateRoom(3)))
        config.roomsRemaining -= 3
    elif config.roomsRemaining <= 3:  # if there are 3 or fewer rooms, generate roomsRemaining-1 rooms
        config.nextThreeRooms.extend(list(generateRoom(config.roomsRemaining - 1)))  # and then the saferoom
        config.nextThreeRooms.extend(list([normalSafeRoom]))
        config.roomsRemaining -= len(config.nextThreeRooms)
    elif config.roomsRemaining > 3 and carnationSpawned:  # if carnation spawned, forcespawns a hiding room on the 3rd room
        config.nextThreeRooms.extend(list(generateRoom(2)))
        config.nextThreeRooms.extend(list(random.choice([longHidingSpot, normalHidingSpot])))
    if config.roomsRemaining >= 3:
        print(f"the next three rooms are: {config.nextThreeRooms[0].roomIdentifier}, {config.nextThreeRooms[1].roomIdentifier} and {config.nextThreeRooms[2].roomIdentifier}")
    elif config.roomsRemaining == 2:
        print(f"the next two rooms are: {config.nextThreeRooms[0]} and {config.nextThreeRooms[1]}")
    else:
        print(f"you have one more room, the saferoom")


def saferoomEnter():
    config.timeRemaining = config.SFTime
    config.inSaferoom = True
    config.currentRoom = 0
    config.roomsRemaining = min(3 * config.saferoom, 25) + 20  # max rooms is 55
    config.saferoom += 1  # increment saferoom
    config.location = 0  # reset location
    config.direction = 0  # reset direction
    config.currentRoomType = 0  # reset current room type
    resetTimer()  # reset timer
    print(f"you have entered saferoom number {config.saferoom}, you are at {config.roomsPassed} rooms passed, press enter to move on")
    config.mainInput = input("")
    mainGameplayLoop()  # restarts main gameplay loop


def mainGameplayLoop(): # active while you are not in a saferoom and alive
    config.gameOn = True
    roomGenerator()  # generates the first three rooms
    config.currentRoomType = config.nextThreeRooms.pop(0)  # gens the first room type and removes it from next three rooms
    config.nextThreeRooms.extend(list(generateRoom(1)))  # gens another room to compensate for the first room's removal
    inputListener()  # starts input listener
    startTimerInThread()  # starts timer
    while config.gameOn: #
        pass  # TODO: implement entity spawning

spawnDictionary = {
    sorrow: sorrowSpawn,
    dozer: dozerSpawn,
    rue: rueSpawn,
    heed: heedSpawn,
    slight: slightSpawn,
    slugfish: slugfishSpawn,
    goatman: goatmanSpawn,
    carnation: carnationSpawn
}

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
print("optional entities:")
print("8. lefttowander: watch your back from time to time, it's scared of light")
rueOn = bool(input("do you want rue on?"))  # sets entity number 8 (rue) to true or false depending on the player
if rueOn:
    entityTypes.append(rue)
randSleep(10, 100)
mainInput = str(input("press enter to start the game"))
print("starting game. . .")
# initial game setup
mainGameplayLoop()

# TODO LIST: inputHandler to handle and validate inputs received: DONE
# TODO LIST: finish room generation system: DONE
# TODO LIST: implement currentRoom and currentRoomType: DONE
# TODO LIST: implement entity spawning system: NEEDS SPAWN CONDITION
# TODO LIST: kill all entities when saferoom is entered (they can still kill the player): DELAYED FK THAT
# TODO LIST: finish controls (real men play without look controls): done, needs prevRoom implementation
# TODO LIST: implement config class (90 lines of variables is making me cringe): config file created, not class tho
# TODO LIST: put in more files (i'm going back to rust): in progress
# TODO LIST: implement inventory and rue (ily rue)
# TODO LIST: comment code better (typing benchmark go brrr)
# TODO LIST: playtest (we don't want to be like cs2 on release do we)
# TODO LIST: ability to go back to previous rooms (prevRoom)