# stores the entities and spawned variables
# i hate circular imports now i have to make 23823840843084023840 files
# the class is called mainEntity because everything was in a single file and i thought >
# > that that was cringe and it in fact is it looks much better now and i seem smarter than i actually am

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
