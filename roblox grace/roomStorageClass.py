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