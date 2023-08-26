# Quick-Guide

# Basic Platformer With BLACKFORGE2

*This framework assumes you have an understanding of the following: ( **python**, **pygame**, **Object Oriented Programming**, **Classes** and **Inheritance** )*

*This is meant to give you an understanding of how this framework was intended to be used while also showing you some attributes, classes and functions provided by BLACKFORGE2. There are many more tools included to help you out with making your game. You can find out more about them in the* [Documentation](https://www.notion.so/Documentation-0-1-3-40543d6137f84918bd900931ec93e02d?pvs=21)*.*

<aside>
💡 *I have provided comments within the code to explain whats going on.*

</aside>

### First we get our imports ready and our project settings

---

```python
from BLACKFORGE2 import *

""" Settings """
FPS = 60
SCREEN_SIZE = (1000,800) # x,y
GRAVITY = 0.62  # the gravity constant for our game

```

<aside>
💡 *The development branch of pygame, pygame-ce, is installed with BLACKFORGE2.
If you are experiencing issues/conflicts, it is reccomended to delete pygame by running the following command: `pip uninstall pygame`*

</aside>

---

### First lets create a simple Player class

<aside>
💡 *Within this Player class we will use the [Physics](https://www.notion.so/969eff6f2dd94aa8ba95f9f88be430b8?pvs=21) class, and the [Entity](https://www.notion.so/969eff6f2dd94aa8ba95f9f88be430b8?pvs=21) class along with their attributes to get our player set up quick and clean.*

</aside>

---

```python
class Player(Entity):
    def __init__(self, game, size:int, position:tuple, speed:int, group:pygame.sprite.Group()):
        super().__init__(size, position, speed, group)
        self.game = game  # passing an instance of your main game class can give you access to other classes without imports e.g(self.game.level.level_width)
        self.image.fill([255,0,255]) # the Entity() class has a default image attribute which is just a pygame surface
        self.jump_force = -13  # the force upwards the player has when jumping
        # go to definition on the Entity class to see what other useful attributes it has

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = self.speed  # the velocity attribute is used to control 
															#  the speed the player will move in a certain direction
        elif keys[pygame.K_a]:
            self.velocity.x = -self.speed
        else:
            self.velocity.x = 0

        # the Entity class has atttributes to verify where a collision is happening.
        if keys[pygame.K_SPACE] and self.collide_bottom:  # here we can implement a jump 
							#  by checking the key pressed and the player's bottom collision attribute
            self.velocity.y = self.jump_force

    def update(self, terrain):  # pass the sprite group containing sprites you want the collision methods to check
        self.move()  # call the players move method which alters its velocity
        self.rect.x += self.velocity.x  # move the player's rect according to its velocity (this is done for the y direction on any Entity() that calls the apply_gravity() method.)
        # the Entity class has a physics attribute by default which comes with gravity application, and 2d collision checks
        self.physics.horizontal_movement_collision(self, terrain)  # for the collision checks, you pass the entity to perform the checks on (as the Physics class can be used alone) and the sprites to check collisions with
        self.physics.apply_gravity(self, GRAVITY)  # for gravity application you pass the entity to apply gravity to as well as the gravity constant of your game
        self.physics.vertical_movement_collision(self, terrain)
```

---

<aside>
💡 *The entity class comes with a handful of attributes already set up. One of those attributes is physics. Check out the [Physics](https://www.notion.so/969eff6f2dd94aa8ba95f9f88be430b8?pvs=21) class to learn how it works.*

</aside>

---

### We can now set up a Level class which will handle creating the "layers" or sprite groups for our game, and drawing them at the correct position based on *level_data* that we pass it.

<aside>
💡 *In this class we will use the [StaticTile](https://www.notion.so/969eff6f2dd94aa8ba95f9f88be430b8?pvs=21) class to create some tiles for our player to interact with.*

</aside>

---

```python
class Level():
    def __init__(self, game, level_data, surface):
                        # here i pass the data for the level and the surface it should be drawn to
        self.game = game
        self.level_data = level_data
        self.display_surface = surface

        # sprite groups setup
        self.terrain = pygame.sprite.Group()  # terrain sprites group
        self.create_tile_group(self.level_data, 'terrain', 64)

    def create_tile_group(self, level_data, tile_type:str, tile_size:int):
        # create a group of tile sprites based on the data and type
        tile = pygame.Surface((tile_size, tile_size))  # tile graphics
        tile.fill((25,0,50))

        for row_index, row in enumerate(level_data):  # iterate over each row
            for col_index, value in enumerate(row):        # and then over each column
                if value != '0':  # here we check if a tile should be placed
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # use match case to handle different tile types 
										#  e.g(foreground/background tiles)
                    match tile_type:
                        case 'terrain':
                            sprite = StaticTile((x, y), [self.terrain], tile)  # here we use the StaticTile class to create a tile that has no special properties
                                # we pass the position, sprite group(s), and tile surface (the .image attribute)

    def draw_level(self, surface:pygame.Surface):
        self.terrain.draw(surface)
```

---

### Then we can set up a basic Game class that will contain our game loop.

<aside>
💡 This class is the home of our game loop, and acts as a medium between other classes.

</aside>

---

```python
class Game():
    def __init__(self):
        # pygame.init()  # no need to init all modules, the ones you will need have been initialized
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Example")
        self.clock = pygame.time.Clock()
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player = Player(self, 32, (200,150), 3, [self.player_sprite_group])  # create an instance of the player class
                          # (size, position, speed, sprite group(s))

        # sample game map (if your using tiled, you can use csv files the same way)
        game_map = [
            "1000000000000001",
            "1011110000111101",
            "1000000000000001",
            "1000000000000001",
            "1111000000001111",
            "1111111110000111",
            "1111111111000111",
            "1111111110000111",
            "1000000000001111",
            "1100000000000011",
            "1100000001100011",
            "1100000011111111",
            "1111111111111111",
        ]

        self.level = Level(self, game_map, self.screen)  # create an instance of the level class

    """ Main Game Loop """
    def run(self):
        running = True
        while running:
            self.screen.fill((180, 20, 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.level.draw_level(self.screen)  # call the level's draw method
            self.player.draw(self.screen)  # call the player's draw method
            self.player.update(self.level.terrain)  # call the player's update method and pass the terrain "layer"(sprite group)

            self.clock.tick(FPS)
            pygame.display.flip()
```

---

### Finally we can create an instance of our game class.

---

```
if __name__ == "__main__":
	game = Game()
	game.run()
```

---

### Save your project, and run the following command in the *root directiory* of said project:

---

```
python3 *filename*.py
```

---

### This is the end result.

---

https://github.com/setoyuma/BLACKFORGE2/assets/118138305/583399ea-3eb3-4988-92a4-4d0bbe29d083

Hopefully this tutorial provided some form of insight into some of the useful methods and classes that come with BLACKFORGE2 and how they are intended to be used. 

Feel free to check out the GitHub repo here: https://github.com/setoyuma/BLACKFORGE2

---

[Documentation](https://www.notion.so/Documentation-0-1-3-40543d6137f84918bd900931ec93e02d?pvs=21)