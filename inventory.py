import config


def holyWaterUse():  # called when holy water is used
    if config.playerTagged:  # if player was tagged by slight or heed
        print("used holy water, tag has been removed")
        config.playerTagged = False
    else:
        print("why did you waste this? you weren't tagged and now you aren't either")
    config.inventory.remove(holyWater)


def flashlightUse():  # flashlight use function
    from entity import goatmanSpawned, rueSpawned
    # if the proper conditions are fulfilled, flash rue
    if rueSpawned and config.rueRemainingTime <= 1.5 and config.direction == config.rueDirection:
        config.rueFlashed = True
        print("you flashed rue, don't move until i tell you it's safe")
    # if only time is correct, inform the player
    elif rueSpawned and config.rueRemainingTime <= 1.5 and config.direction != config.rueDirection:
        print("wrong direction, TURN FAST")
    # if only direction is correct, inform the player
    elif rueSpawned and config.direction == config.rueDirection and config.rueRemainingTime > 1.5:
        print("too soon")
    # if rue spawned but nothing else is good, inform the player
    elif rueSpawned and not config.direction == config.rueDirection and not config.rueRemainingTime <= 1.5:
        print("wrong direction and too soon")
    # if the proper conditions are fulfilled, flash goatman
    if goatmanSpawned and config.direction == config.goatmanDirection:
        config.goatmanFlashed = True
        print("you flashed goatman")
    # if goatman spawned but missed, inform the player
    elif goatmanSpawned and config.direction != config.goatmanDirection:
        print("wrong direction")
    else:  # if nothing spawned, inform the player
        print("you didn't flash anything and neither rue nor goatman spawned, why did you waste time?")


class mainInventory:  # define inventory class
    def __init__(self, spawnable, consumed, reuseTimer, item, useEffect=None):
        self.spawnable = spawnable  # does the item spawn naturally? if no, then it spawns at the beginning of the game
        self.consumed = consumed  # does the item get consumed after use?
        self.reuseTimer = reuseTimer  # how much do you wait before being able to use again? can be zero, consumables
                                      # don't have any cooldown
        self.useEffect = useEffect  # the function that executes whatever the item does when used
        self.item = item  # stores the name of the item so i dont print the memory address :(

    def use(self):  # mainInventory use method, redirects to the adequate useEffect function of each instance
        if self.useEffect:
            if self.consumed:  # if the item is consumed on use, remove from inventory
                config.inventory.remove(self)
            self.useEffect()

    def __str__(self):
        return str(self.item)

    def __repr__(self):
        return str(self.item)


flashlight = mainInventory(False, False, 1, "flashlight", flashlightUse)  # used versus rue and goatman
lamp = mainInventory(False, False, None, "lamp", None)  # required to receive any room-related info
holyWater = mainInventory(True, True, None, "holy water", holyWaterUse)  # removes slight/heed's tag

inventoryDictionary = {
    holyWater: "holy water",
    flashlight: "flashlight",
    lamp: "lamp",
}


def openCloseInventory():  # opens or closes the inventory when called
    if not config.inventoryOpen:  # if inventory is not open, open it, block movement and print current inventory
        config.inventoryOpen = True
        print("inventory opened")
        print(config.inventory)
    else:  # if inventory is open, close it
        config.inventoryOpen = False
        print("inventory closed")