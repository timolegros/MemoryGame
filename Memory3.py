# TTT Version 1
import pygame, random, time, filecmp


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 415))
    # set the title of the display window
    pygame.display.set_caption('Memory')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.board = []
        self.board_size = 4
        self.load_shuffle()
        self.create_board()
        self.score = 0
        self.counter = 0
        self.safety = 0
        self.image_list = []
        self.turned_cards = []
        self.click_list = []

    def load_shuffle(self):
        self.image_list = []
        for i in range(1, 9):
            image = pygame.image.load('image' + str(i) + '.bmp')
            self.image_list.append(image)
            self.image_list.append(image)
        random.shuffle(self.image_list)

    def create_board(self):
        i = 0
        z = 3
        Tile.set_surface(self.surface)
        image = pygame.image.load('easyname.bmp')
        width = image.get_width() + z
        height = image.get_height() + z
        for row_index in range(0, self.board_size):
            row = []
            for col_index in range(0, self.board_size):
                x = (width * col_index) + z
                y = (height * row_index) + z
                self.tile = Tile(x, y, self.image_list[i])
                row.append(self.tile)
                i = i + 1
            self.board.append(row)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            if self.continue_game:
                self.update()
                self.decide_continue()
                self.draw()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click(event)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.draw_score()
        # Draw the tiles
        for each_row in self.board:
            for each_tile in each_row:
                each_tile.draw_tile()
            pygame.display.update()  # make the updated surface appear on the display

    def click(self, event):
        # decides what to do when an image is clicked
        # event is the mousebuttonup event
        x, y = event.pos
        for i in range(0, 4):
            row = self.board[i]
            for t in range(0, 4):
                image = row[t]
                if image.position(x, y) and len(self.turned_cards) <= 2:
                    image.change_hidden()
                    self.turned_cards.append(image)
                    print(len(self.turned_cards))
                    if self.turned_cards.count(image) == 2:
                        self.turned_cards = []
                        print('if')
                    if len(self.turned_cards) == 2:
                        print('elif')
                        time.sleep(1)
                        image.unchange_hidden()
                        first_image = self.turned_cards[0]
                        first_image.unchange_hidden()
                        self.turned_cards = []

    def draw_score(self):
        self.score = pygame.time.get_ticks() // 1000
        fg_color = pygame.Color('white')
        font = pygame.font.SysFont('', 70)
        text_string = str(self.score)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        if self.score < 10:
            x = 470
        elif 10 <= self.score < 100:
            x = 443
        else:
            x = 420
        location = (x, 0)
        self.surface.blit(text_box, location)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        pass

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        self.counter = 0
        for each_row in self.board:
            for each_tile in each_row:
                if not each_tile.hidden:
                    self.counter = self.counter + 1
        if self.counter >= 16:
            self.continue_game = False


class Tile:
    # An object in this class represents a Dot that moves
    # Shared Attributes or Class Attributes
    surface = None
    border_size = 3
    border_color = pygame.Color('black')
    hidden_tile = pygame.image.load('easyname.bmp')
    hidden = True
    turned_cards = []

    @classmethod
    def set_surface(cls, game_surface):
        cls.surface = game_surface

    # Instance Methods
    def __init__(self, x, y, image):
        self.image = image
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(x, y, width, height)
        self.hidden = True

    def position(self, x, y):
        return self.rect.collidepoint(x, y)

    def draw_tile(self):
        # Draw the dot on the surface
        # - self is the Dot
        counter = []
        if self.hidden == False:
            pygame.draw.rect(Tile.surface, Tile.border_color, self.rect, Tile.border_size)
            Tile.surface.blit(self.image, self.rect)
        else:
            Tile.surface.blit(Tile.hidden_tile, self.rect)

    def change_hidden(self):
        self.hidden = False
        print('its changed')

    def unchange_hidden(self):
        self.hidden = True


main()

