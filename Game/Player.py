class player:
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.health = 100
        self.position = position

    def move(self, new_position):
        self.position = new_position
        print(f"{self.name} moved to {self.position}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {amount} damage and now has {self.health} health")

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.name} healed {amount} and now has {self.health} health")

    