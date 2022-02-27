# Base game functionnality
import numpy as np

class Base2048:

    def __init__(self, r_seed = 1, board_size = 4):
        np.random.seed(seed=r_seed)

        self.board_size = board_size

        self.board = np.full((board_size, board_size), None)
        self._prev_board = None
        
        self.score = 0
        self.game_state = "playing"
        self.insert_random_tile(2)

    def get_board(self):
        return self.board

    def shift(self, direction):
        self._prev_board = self.board.copy()

        self.__getattribute__("shift_"+direction)()
        if not np.array_equiv(self._prev_board, self.board):
            self.insert_random_tile()

        self.game_state = self.get_game_state() 

    def shift_right(self):
        # get non-Null tiles from row
        for row in range(self.board_size):
            tile_list = np.extract(self.board[row,:] != None, self.board[row,:]).tolist()
            new_row = [] 
            # starting at the right-most tile, and moving to the left: Multiply tile with next tile if both tiles are of same value
            while len(tile_list) > 0:
                t = tile_list.pop()
                if len(tile_list) > 0:
                    t_neighbour = tile_list[-1]
                    if t == t_neighbour:
                        t = t + t_neighbour
                        tile_list.pop()
                        self.score += t
                new_row.append(t)
            new_row.extend([None] * (self.board_size - len(new_row)))  
            new_row.reverse()
            self.board[row,:] = new_row
        

    def shift_left(self):
        # get non-Null tiles from row
        for row in range(self.board_size):
            tile_list = np.extract(self.board[row,:] != None, self.board[row,:]).tolist()
            tile_list.reverse()
            new_row = [] 
            # starting at the left-most tile, and moving to the right: Multiply tile with next tile if both tiles are of same value
            while len(tile_list) > 0:
                t = tile_list.pop()
                if len(tile_list) > 0:
                    t_neighbour = tile_list[-1]
                    if t == t_neighbour:
                        t = t + t_neighbour
                        tile_list.pop()
                        self.score += t
                new_row.append(t)
            new_row.extend([None] * (self.board_size - len(new_row)))  
            self.board[row,:] = new_row
    
    def shift_down(self):
        # get non-Null tiles from column
        for col in range(self.board_size):
            tile_list = np.extract(self.board[:,col] != None, self.board[:,col]).tolist()
            new_col = [] 
            # starting at the bottom-most tile, and moving to the up: Multiply tile with next tile if both tiles are of same value
            while len(tile_list) > 0:
                t = tile_list.pop()
                if len(tile_list) > 0:
                    t_neighbour = tile_list[-1]
                    if t == t_neighbour:
                        t = t + t_neighbour
                        tile_list.pop()
                        self.score += t
                new_col.append(t)
            new_col.extend([None] * (self.board_size - len(new_col)))  
            new_col.reverse()
            self.board[:,col] = new_col

    def shift_up(self):
        # get non-Null tiles from column
        for col in range(self.board_size):
            tile_list = np.extract(self.board[:,col] != None, self.board[:,col]).tolist()
            tile_list.reverse()
            new_col = [] 
            # starting at the top-most tile, and moving down: Multiply tile with next tile if both tiles are of same value
            while len(tile_list) > 0:
                t = tile_list.pop()
                if len(tile_list) > 0:
                    t_neighbour = tile_list[-1]
                    if t == t_neighbour:
                        t = t + t_neighbour
                        tile_list.pop()
                        self.score += t
                new_col.append(t)
            new_col.extend([None] * (self.board_size - len(new_col)))  
            self.board[:,col] = new_col


    def insert_random_tile(self, num_tile = 1):
        for i in range(num_tile):
            
            val = 2 if np.random.uniform(low=0.0, high=1.0) < 0.9 else 4  #generate a value (Based on official code of 2048)
            
            pos = np.argwhere(self.board == None)  #Get all available positions
            if len(pos) > 0:
                r = np.random.randint(0, len(pos))
                picked_tile = tuple(pos[r]) #Pick at random an availble tile

                self.board[picked_tile] = val
        
    def get_game_state(self):
        
        #Playing, Won, Lost
        if np.nanmax(self.board.astype('float64')) >= 2048:
            return "won"
        
        if len(np.argwhere(self.board == None)) > 0: #If there are empty cells
            return "playing"

        playable = False
        #Check each tile neighbour to check for pairs
        for i in range(self.board_size):
            for j in range(self.board_size-1):
                tile = self.board[i,j]
                neigh_tile = self.board[i,j+1]
                if tile == neigh_tile:
                    return "playing"

        for i in range(self.board_size-1):
            for j in range(self.board_size):
                tile = self.board[i,j]
                neigh_tile = self.board[i+1,j]
                if tile == neigh_tile:
                    return "playing"            

        print("LOST")
        return "lost"                 




import os, pygame
from pygame.locals import *
class Demo2048:
    def __init__(self, n):

        self.inner_margin = 10   #pt
        self.tile_spacing = 10   
        self.tile_size = 58  
        
        self.n = n
        
        self.width = (n * self.tile_size) \
                     + (n - 1) * self.tile_spacing \
                     + (2 * self.inner_margin)
        self.height = self.width


        self._setup()

        self.running = True
        self.start_game()

    def start_game(self):
        #bg colour, font colour, font size
        self.tile_style = [('#eee4da', "#776e65", 41),
                           ('#eee1c9', "#776e65", 41),
                           ('#f3b27a', "#f9f6f2", 41),
                           ('#f69664', "#f9f6f2", 41),
                           ('#f77c5f', "#f9f6f2", 41),
                           ('#f75f3b', "#f9f6f2", 41),
                           ('#edd073', "#f9f6f2", 29),
                           ('#edcc62', "#f9f6f2", 29),
                           ('#edc950', "#f9f6f2", 29),
                           ('#edc53f', "#f9f6f2", 20),
                           ('#edc22e', "#f9f6f2", 20),
                           ('#3c3a33', "#f9f6f2", 20)]

        self.base = Base2048(board_size = self.n) 

        while self.running:

            self.draw(None)
            self.display_score()
            # poll key events
            for event in pygame.event.get():
                # get keys pressed
                key_pressed = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    self.running = False
                if key_pressed[pygame.K_LEFT]:
                    self.base.shift("left")
                if key_pressed[pygame.K_UP]:
                    self.base.shift("up")
                if key_pressed[pygame.K_DOWN]:
                    self.base.shift("down")
                if key_pressed[pygame.K_RIGHT]:
                    self.base.shift("right")
            
        pygame.quit()

    def draw(self, background_color):
        background_color = "#bbada0" 
        self.screen.fill(background_color)

        y = self.inner_margin
        for i in range(self.base.board.shape[0]):
            x = self.inner_margin
            for j in range(self.base.board.shape[1]):
                tile = self.base.board[i,j]
                color = None
                if tile == None:
                    color = "#cdc1b4"
                else:
                    style = self.tile_style[int(np.log2(tile)) - 1]
                    color = style[0]
                    font_color = style[1]
                    font_size = style[2]

                t = pygame.draw.rect(self.screen, color, 
                                 pygame.Rect(x, y, self.tile_size, self.tile_size),
                                 border_top_left_radius=3,
                                 border_top_right_radius=3,
                                 border_bottom_left_radius=3,
                                 border_bottom_right_radius=3)

                if tile != None:
                    font = pygame.font.SysFont("Arial", size = font_size, bold = True) 
                    text = font.render(str(tile), True, font_color)
                    
                    text_rect = text.get_rect()
                    text_rect.center = t.center 

                    self.screen.blit(text, dest=text_rect)

                x += self.tile_size + self.tile_spacing
            y += self.tile_size + self.tile_spacing

        pygame.display.update()

    def display_score(self):
        pygame.display.set_caption('Score - ' + str(self.base.score) + " - " + self.base.game_state)


    def _setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def reset(self):
        self.init()


    def getScreenRGB(self):
        """
        Source : https://github.com/oscastellanos/gym-traffic/blob/master/gym_traffic/envs/traffic_simulator.py
        Returns the current game screen in RGB format.
        Returns
        --------
        numpy uint8 array
            Returns a numpy array with the shape (width, height, 3).
        """
        return pygame.surfarray.array3d(
            pygame.display.get_surface()).astype(np.uint8)


if __name__ == '__main__':
    #pygame.init()
    game = Demo2048(4)
    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()