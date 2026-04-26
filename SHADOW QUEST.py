# Shadow Quest - Anime RPG Adventure
# Libraries used: pygame (v2.6.1) - pygame.org, sys (Python built-in)
import pygame
import sys

# ─── INITIALISE PYGAME ───────────────────────────────────────
pygame.init()

# ─── SCREEN SETTINGS ─────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Quest")

# ─── COLOURS ─────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
DARK_BLUE  = (10,  10,  40)
GOLD       = (255, 200, 50)
RED        = (200, 50,  50)
TEAL       = (50,  180, 150)
GREY       = (100, 100, 100)
LIGHT_GREY = (200, 200, 200)
PURPLE     = (150, 50,  200)
GREEN      = (50,  200, 50)

# ─── FONTS ───────────────────────────────────────────────────
font_large  = pygame.font.SysFont("consolas", 32, bold=True)
font_medium = pygame.font.SysFont("consolas", 20)
font_small  = pygame.font.SysFont("consolas", 16)

# ─── CLOCK ───────────────────────────────────────────────────
clock = pygame.time.Clock()
FPS   = 60

# ─── ITEM CLASS ──────────────────────────────────────────────
class Item:
    def __init__(self, name, description, required_in):
        self.name        = name
        self.description = description
        self.required_in = required_in

    def __str__(self):
        return self.name

# ─── CREATE ALL GAME ITEMS ───────────────────────────────────
torch  = Item("Torch",  "A flickering torch to light dark places.", "Dark Forest")
coin   = Item("Coin",   "A shiny gold coin.",                       "Haunted Inn")
herb   = Item("Herb",   "A strange glowing herb.",                  "River Crossing")
key    = Item("Key",    "An ancient iron key.",                     "Castle Bridge")
scroll = Item("Scroll", "A scroll covered in mystic symbols.",      "Shrine Room")

# ─── PLAYER CLASS ────────────────────────────────────────────
class Player:
    def __init__(self, name):
        self.name         = name
        self.health       = 100
        self.bag          = []
        self.current_room = "Village Gate"

    def pick_up(self, item):
        # Only pick up if bag has space (max 4 items)
        if len(self.bag) < 4:
            self.bag.append(item)
            return f"You picked up the {item.name}!"
        else:
            return "Your bag is full! Press D to drop an item."

    def drop(self, index):
        # Drop item by index from bag
        if 0 <= index < len(self.bag):
            dropped = self.bag.pop(index)
            return f"You dropped the {dropped.name}."
        return "Invalid item!"

    def use_item(self, item_name, room_name):
        # Check if player has item and if it works in this room
        for item in self.bag:
            if item.name.lower() == item_name.lower():
                if item.required_in == room_name:
                    self.bag.remove(item)
                    return f"You used the {item_name}! The way is now open!"
                else:
                    return f"The {item_name} doesn't work here."
        return "You don't have that item!"

    def show_bag(self):
        # Display everything currently in the bag
        if len(self.bag) == 0:
            return "Your bag is empty."
        contents = ", ".join([item.name for item in self.bag])
        return f"Bag ({len(self.bag)}/4): {contents}"

    def __str__(self):
        return f"{self.name} | HP: {self.health} | {self.show_bag()}"

# ─── ROOM CLASS ──────────────────────────────────────────────
class Room:
    def __init__(self, name, description, exits, item=None,
                 is_locked=False, required_item=None):
        self.name          = name
        self.description   = description
        self.exits         = exits
        self.item          = item
        self.is_locked     = is_locked
        self.required_item = required_item

    def get_exits_text(self):
        # Returns exits as readable string
        return ", ".join(self.exits.keys())

# ─── CREATE ALL 11 ROOMS ─────────────────────────────────────
# FIX 1: Herb moved to Dark Forest (not River Crossing)
# FIX 3: Haunted Inn now has west exit back to Mystic Cave
rooms = {
    "Village Gate": Room(
        "Village Gate",
        "You stand at the entrance of a quiet village.",
        {"north": "Market Square", "east": "Old Temple"},
        item=torch
    ),
    "Market Square": Room(
        "Market Square",
        "A bustling market. A coin glints on the cobblestones.",
        {"south": "Village Gate", "east": "Dark Forest"},
        item=coin
    ),
    "Old Temple": Room(
        "Old Temple",
        "An ancient temple covered in vines. A key hangs on the wall.",
        {"west": "Village Gate", "north": "Mystic Cave"},
        item=key
    ),
    "Dark Forest": Room(
        "Dark Forest",
        "A dark eerie forest. A glowing herb grows nearby.",
        {"west": "Market Square", "south": "River Crossing"},
        item=herb,
        is_locked=True,
        required_item="Torch"
    ),
    "Mystic Cave": Room(
        "Mystic Cave",
        "A glowing cave full of strange symbols. A scroll floats in the air.",
        {"south": "Old Temple", "west": "Haunted Inn"},
        item=scroll
    ),
    "River Crossing": Room(
        "River Crossing",
        "A rushing river. A guard eyes you suspiciously.",
        {"north": "Dark Forest", "west": "Haunted Inn"},
        is_locked=True,
        required_item="Herb"
    ),
    "Haunted Inn": Room(
        "Haunted Inn",
        "A creepy inn with flickering candles. The innkeeper wants payment.",
        {"east": "River Crossing", "north": "Mystic Cave", "south": "Shrine Room"},
        is_locked=True,
        required_item="Coin"
    ),
    "Shrine Room": Room(
        "Shrine Room",
        "A sacred shrine. Strange writing covers the walls.",
        {"north": "Haunted Inn", "east": "Guard Tower"},
        is_locked=True,
        required_item="Scroll"
    ),
    "Guard Tower": Room(
        "Guard Tower",
        "A tall tower. Armoured guards watch your every move.",
        {"west": "Shrine Room", "south": "Castle Bridge"}
    ),
    "Castle Bridge": Room(
        "Castle Bridge",
        "A grand bridge. A huge locked gate blocks the way.",
        {"north": "Guard Tower", "east": "Shadow Throne"},
        is_locked=True,
        required_item="Key"
    ),
    "Shadow Throne": Room(
        "Shadow Throne",
        "The dark throne room. The Shadow Boss awaits!",
        {"west": "Castle Bridge"}
    ),
}

# ─── HELPER FUNCTIONS ────────────────────────────────────────
def draw_text(text, font, colour, x, y):
    # Renders and draws text onto the screen
    surface = font.render(text, True, colour)
    screen.blit(surface, (x, y))

def draw_bag(player, y_start):
    # Draws the bag contents panel on the right side
    draw_text("BAG:", font_small, GOLD, 600, y_start)
    if len(player.bag) == 0:
        draw_text("Empty", font_small, GREY, 600, y_start + 25)
    else:
        for i, item in enumerate(player.bag):
            draw_text(f"{i+1}. {item.name}", font_small, LIGHT_GREY,
                      600, y_start + 25 + (i * 22))
    draw_text(f"({len(player.bag)}/4)", font_small, GREY,
              600, y_start + 120)
    draw_text("D+1-4: drop", font_small, GREY, 600, y_start + 140)

# ─── NAME ENTRY SCREEN ───────────────────────────────────────
player_name   = ""
entering_name = True

while entering_name:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name.strip() != "":
                entering_name = False
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif len(player_name) < 15:
                if event.unicode.isalnum() or event.unicode == " ":
                    player_name += event.unicode

    screen.fill(DARK_BLUE)
    draw_text("Shadow Quest",         font_large,  GOLD,  SCREEN_WIDTH // 2 - 120, 150)
    draw_text("Enter your name:",     font_medium, WHITE, SCREEN_WIDTH // 2 - 120, 250)
    pygame.draw.rect(screen, (30, 30, 70),
                     (SCREEN_WIDTH // 2 - 150, 290, 300, 44), border_radius=8)
    draw_text(player_name + "|",      font_medium, GOLD,  SCREEN_WIDTH // 2 - 140, 300)
    draw_text("Press ENTER to start", font_small,  GREY,  SCREEN_WIDTH // 2 - 110, 360)
    pygame.display.flip()

# ─── CREATE PLAYER ───────────────────────────────────────────
player      = Player(player_name.strip())
message     = "Arrow keys: move | P: pick up | U: use item | D+1-4: drop"
you_win     = False
drop_mode   = False  # FIX 2: drop mode for dropping items

# ─── MAIN GAME LOOP ──────────────────────────────────────────
running = True
while running:
    clock.tick(FPS)
    current = rooms[player.current_room]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not you_win:

            # ── DROP MODE ──────────────────────────────────
            # FIX 2: Press D then a number to drop that item
            if drop_mode:
                if event.key == pygame.K_1 and len(player.bag) >= 1:
                    message = player.drop(0)
                elif event.key == pygame.K_2 and len(player.bag) >= 2:
                    message = player.drop(1)
                elif event.key == pygame.K_3 and len(player.bag) >= 3:
                    message = player.drop(2)
                elif event.key == pygame.K_4 and len(player.bag) >= 4:
                    message = player.drop(3)
                else:
                    message = "Drop cancelled."
                drop_mode = False

            else:
                direction = None

                # Arrow keys for movement
                if event.key == pygame.K_UP:
                    direction = "north"
                elif event.key == pygame.K_DOWN:
                    direction = "south"
                elif event.key == pygame.K_LEFT:
                    direction = "west"
                elif event.key == pygame.K_RIGHT:
                    direction = "east"

                # Move player if direction chosen
                if direction:
                    if direction in current.exits:
                        next_room = rooms[current.exits[direction]]
                        if next_room.is_locked:
                            message = f"Blocked! Need: {next_room.required_item}"
                        else:
                            player.current_room = current.exits[direction]
                            message = f"You moved {direction}!"
                            if player.current_room == "Shadow Throne":
                                you_win = True
                    else:
                        message = "You can't go that way!"

                # P key = pick up item in current room
                elif event.key == pygame.K_p:
                    if current.item is not None:
                        message = player.pick_up(current.item)
                        if "picked up" in message:
                            current.item = None
                    else:
                        message = "Nothing to pick up here."

                # U key = use item to unlock any adjacent locked room
                elif event.key == pygame.K_u:
                    unlocked_something = False
                    for d, room_name in current.exits.items():
                        next_room = rooms[room_name]
                        if next_room.is_locked and next_room.required_item:
                            result = player.use_item(
                                next_room.required_item, next_room.name)
                            if "open" in result:
                                next_room.is_locked = False
                                message = result
                                unlocked_something = True
                                break
                            else:
                                message = result
                    if not unlocked_something:
                        message = "Nothing to unlock here."

                # D key = enter drop mode
                elif event.key == pygame.K_d:
                    if len(player.bag) > 0:
                        drop_mode = True
                        message = "Drop which item? Press 1-4 (or any key to cancel)"
                    else:
                        message = "Your bag is already empty!"

    # ─── DRAW EVERYTHING ─────────────────────────────────────
    screen.fill(DARK_BLUE)

    if you_win:
        draw_text("YOU WIN!", font_large, GOLD,
                  SCREEN_WIDTH // 2 - 100, 180)
        draw_text("You defeated the Shadow Boss!", font_medium,
                  WHITE, SCREEN_WIDTH // 2 - 190, 250)
        draw_text("Press ESC to quit.", font_small, GREY,
                  SCREEN_WIDTH // 2 - 90, 310)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
    else:
        # Title and player info
        draw_text("Shadow Quest", font_large, GOLD, 20, 20)
        draw_text(f"Player: {player.name}  HP: {player.health}",
                  font_small, TEAL, 20, 70)

        # Room info panel
        pygame.draw.rect(screen, (20, 20, 60),
                         (20, 95, 560, 120), border_radius=8)
        draw_text(f">> {current.name}", font_medium, PURPLE, 30, 105)
        draw_text(current.description,  font_small, LIGHT_GREY, 30, 135)

        # Item in room
        if current.item:
            draw_text(f"Item here: {current.item.name}  (P to pick up)",
                      font_small, GREEN, 30, 170)
        else:
            draw_text("No items here.", font_small, GREY, 30, 170)

        # Exits
        draw_text(f"Exits: {current.get_exits_text()}",
                  font_small, WHITE, 30, 230)

        # Message bar
        pygame.draw.rect(screen, (30, 30, 70),
                         (20, 260, 560, 40), border_radius=6)
        draw_text(message, font_small, GOLD, 30, 272)

        # Controls
        draw_text("Arrows: move | P: pick up | U: unlock | D+num: drop",
                  font_small, GREY, 20, 320)

        # Bag panel
        pygame.draw.rect(screen, (20, 20, 60),
                         (580, 95, 200, 220), border_radius=8)
        draw_bag(player, 105)

        # Winning hint
        draw_text("Hint: Torch>Key>Scroll>Coin then enter Dark Forest",
                  font_small, GREY, 20, 560)

    pygame.display.flip()
