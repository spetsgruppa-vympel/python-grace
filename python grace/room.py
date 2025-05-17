import random
import config
from entity import carnationSpawned


class mainRoom:  # define main room class used to generate room types
    def __init__(self, hidingSpot, isLongRoom, isSaferoom, heedSlightSpawns, roomIdentifier, roomNumber):
        self.hidingSpot = hidingSpot  # does the room contain a hiding spot to avoid carnation?
        self.isLongRoom = isLongRoom  # is the room a long room? (needs two forwards to cross)
        self.isSaferoom = isSaferoom  # is the room the entrance to a saferoom?
        self.heedSlightSpawns = heedSlightSpawns  # can heed or slight spawn?
        self.roomIdentifier = roomIdentifier  # the name of the room that is shown to the player
        self.roomNumber = roomNumber  # number of the room


normalRoom = mainRoom(False, False, False, True, "room", None)
longRoom = mainRoom(False, True, False, True, "long room", None)
normalHidingSpot = mainRoom(True, False, False, False, "hiding spot", None)
normalSafeRoom = mainRoom(False, False, True, False, "safe room", None)
longHidingSpot = mainRoom(True, True, False, False, "long hiding spot", None)
longSafeRoom = mainRoom(False, True, True, False, "long safe room", None)
roomTypes = [normalRoom, longRoom, normalHidingSpot, normalSafeRoom, longHidingSpot, longSafeRoom]  # stores all rooms
randomlyGeneratedRooms = [normalRoom, longRoom]  # stores the rooms that can be generated randomly, all other rooms >
mainInput = "press enter to continue"


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
    if specificRoom1 and mainRoom:
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
    if specificRoom2 and mainRoom:
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


