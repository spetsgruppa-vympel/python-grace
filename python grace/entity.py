# stores the entities and spawned variables
# i hate circular imports now i have to make 23823840843084023840 files
# the class is called mainEntity because everything was in a single file and i thought >
# > that that was cringe and it in fact is it looks much better now and i seem smarter than i actually am
import random
import time

import config


class mainEntity:  # define main entity class to store entities

    def __init__(self, oneShots, spawnsFrom, checkTime, recursive, recAmount, spawnsWhere):
        self.oneShots = oneShots  # dictates whether the entity kills instantly, heed and slight need to tag you first
        self.spawnsFrom = spawnsFrom  # dictates which saferoom the entity spawns from (inclusive)
        self.checkTime = checkTime  # time in which the entity does the kill check, in seconds
        self.recursive = recursive  # does the entity come back after the attack?
        self.recAmount = recAmount  # how many times does it come back?
        self.spawnsWhere = spawnsWhere  # does it spawn in the current room (0), behind (-1), or in the front (1)?


dozer = mainEntity(True, 3, 3, False, 0, 0)  # kills if not crouching
sorrow = mainEntity(True, 3, 2, False, 0, 0)  # kills if you move
rue = mainEntity(True, 0, 5, True, 1, -1)  # kills if you don't flash it
heed = mainEntity(False, 3, 2, False, 0, 1)  # tags if you don't look at it
slight = mainEntity(False, 1, 2, False, 0, 1)  # tags if you look at it
slugfish = mainEntity(True, 2, 2, False, 0, -1)  # kills if you are in its way
goatman = mainEntity(True, 0, 4, True, 99999, -1)  # it's over nine thousand
carnation = mainEntity(True, 0, 5, False, 0, -1)  # kills if not in hiding spot
entityTypes = [dozer, sorrow, heed, slight, slugfish, goatman, carnation]

dozerSpawned = False  # stores whether the entity dozer has spawned (duplicate spawns are not allowed)
sorrowSpawned = False  # stores whether the entity sorrow has spawned (duplicate spawns are not allowed)
heedSpawned = False  # stores whether the entity heed has spawned (duplicate spawns are not allowed)
slightSpawned = False  # stores whether the entity slight has spawned (duplicate spawns are not allowed)
slugfishSpawned = False  # stores whether the entity slugfish has spawned (duplicate spawns are not allowed)
goatmanSpawned = False  # stores whether the entity goatman has spawned (duplicate spawns are not allowed)
carnationSpawned = False  # stores whether the entity carnation has spawned (duplicate spawns are not allowed)


def dozerSpawn():  # dozer spawn function
    global dozerSpawned, dozer
    from config import playerDead
    from config import randSleep
    if not dozerSpawned and dozer.spawnsFrom >= config.saferoom:
        dozerSpawned = True
        print("stay down, don't move")
        randSleep(80, 200)
        time.sleep(dozer.checkTime)  # wait the time specified
        if config.mainInput != "c":  # kill check, kills if the player is not crouching
            playerDead("dozer")  # calls playerDead with the death method dozer
        dozerSpawned = False
        if config.gameOn:
            print("dozer has despawned")
    else:
        entitySpawner()


def sorrowSpawn():  # sorrow spawn function
    from config import randSleep, playerDead
    from movementClass import inputListener
    global sorrowSpawned, sorrow
    if not sorrowSpawned and sorrow.spawnsFrom >= config.saferoom:
        sorrowSpawned = True
        config.mainInput = False  # if sorrowSpawned is true, inputlistener stops
        config.mainInput = input("stay silent, don't make one sound")  # this is done to make sure you can't input anything
        randSleep(80, 200)  # between spawn and the kill check and get away with it
        time.sleep(sorrow.checkTime)  # wait the time specified
        if config.mainInput:  # kill check, checks if the player has moved at all during the interval
            playerDead("sorrow")  # calls playerDead with the death method sorrow
        if config.gameOn:
            print("sorrow has despawned, you can move now")
            sorrowSpawned = False
            inputListener()  # restarts input listener
    else:
        entitySpawner()


def heedSpawn():  # heed spawn function
    from config import playerDead
    global heedSpawned
    if not heedSpawned and slightSpawned:
        heedSpawned = True
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
                heedSpawned = False
    else:
        entitySpawner()


def slightSpawn():  # slight spawn function
    global slightSpawned, heedSpawned
    from config import playerDead
    if not slightSpawned and heedSpawned:
        slightSpawned = True
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
            slightSpawned = False
    else:
        entitySpawner()


def slugfishSpawn():  # slugfish spawn function
    global slugfish, slugfishSpawned
    from config import playerDead
    if not slugfishSpawned:
        print("slugfish has spawned, hug the wall")
        time.sleep(slugfish.checkTime)
        if config.location == 0:  # kills the player if they are in the middle of the room
            playerDead("slugfish")
        if config.gameOn:
            print("slugfish has despawned")
            slugfishSpawned = False
    else:
        entitySpawner()


def goatmanSpawn():  # goatman spawn function
    global goatman, goatmanSpawned
    if not goatmanSpawned:
        goatmanSpawned = True
        print("HIdeNOw")
        while not config.inSaferoom:
            print("HIdeNOw")
            time.sleep(goatman.checkTime)
            #TODO: implement kill check


def rueSpawn():  # rue spawn function
    global rue
    if not config.rueSpawned:
        config.rueSpawned = True
        print("rue has spawned, watch your back and flash it when it gets close")
        for i in range(rue.recAmount):
            pass  # TODO: implement kill check
    if config.gameOn:
        print("rue has despawned")
        config.rueSpawned = False


def carnationSpawn():  # carnation spawn function
    global carnationSpawned, dozerSpawned, sorrowSpawned
    if not carnationSpawned and not dozerSpawned and not sorrowSpawned:
        carnationSpawned = True
        print("carnation has spawned, run forwards, you will find a hiding room")
        if config.gameOn:
            print("carnation has despawned")
            carnationSpawned = False
    else:
        entitySpawner()


def entitySpawner():  # main entity spawner function
    global slight, heed, entityTypes
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


spawnDictionary = {
    dozer: dozerSpawn,
    rue: rueSpawn,
    heed: heedSpawn,
    slight: slightSpawn,
    slugfish: slugfishSpawn,
    goatman: goatmanSpawn,
    carnation: carnationSpawn
}
