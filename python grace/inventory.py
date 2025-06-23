import config
class mainInventory: # define inventory class
    def __init__(self, spawnable, consumed, reuseTimer):
        self.spawnable = spawnable  # does the item spawn naturally? if no, then it spawns at the beginning of the game
        self.consumed = consumed  # does the item get consumed after use?
        self.reuseTimer = reuseTimer  # how much do you wait before being able to use again? can be zero, consumables
                                      # don't have any cooldown

flashlight = mainInventory(False, False, 0)  # used versus rue and goatman
lamp = mainInventory(False, False, None)  # required to receive any room-related info
holyWater = mainInventory(True, True, None)  # removes slight/heed's tag

inventoryDictionary = {
    holyWater : "holy water",
    flashlight : "flashlight",
    lamp : "lamp",
}