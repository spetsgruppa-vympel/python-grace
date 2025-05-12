# stores entity spawn functions
# did i tell you that i hate circular imports?

import random
import time
import config
import entityStorageClass
from entityStorageClass import dozer, sorrow, slugfish, goatman, rue, entityTypes, slight, heed, carnation
from main import randSleep, playerDead
from movementClass import inputListener


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
