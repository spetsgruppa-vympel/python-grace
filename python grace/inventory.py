import config


def holyWaterUse():  # called when holy water is used
    if config.playerTagged:
        print("used holy water, tag has been removed")
        config.playerTagged = False
    else:
        print("why did you waste this? you weren't tagged and now you aren't either")


class mainInventory: # define inventory class
    def __init__(self, spawnable, consumed, reuseTimer, useEffect = None):
        self.spawnable = spawnable  # does the item spawn naturally? if no, then it spawns at the beginning of the game
        self.consumed = consumed  # does the item get consumed after use?
        self.reuseTimer = reuseTimer  # how much do you wait before being able to use again? can be zero, consumables
                                      # don't have any cooldown
        self.useEffect = useEffect  # the function that executes whatever the item does when used

    def use(self):
        if self.useEffect:
            self.useEffect()

flashlight = mainInventory(False, False, 1, None)  # used versus rue and goatman
lamp = mainInventory(False, False, None, None)  # required to receive any room-related info
holyWater = mainInventory(True, True, None, holyWaterUse)  # removes slight/heed's tag


inventoryDictionary = {
    holyWater : "holy water",
    flashlight : "flashlight",
    lamp : "lamp",
}

def openCloseInventory():  # opens or closes the inventory when called
    if not config.inventoryOpen:  # if inventory is not open, open it, block movement and print current inventory
        config.inventoryOpen = True
        print("inventory opened")
    else:  # if inventory is open, close it
        config.inventoryOpen = False
        print("inventory closed")

