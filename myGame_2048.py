# Base game functionnality
import numpy as np

class Base2048:

    def __init__(self, r_seed = 1, board_size = 4):
        
        self.board_size = board_size

        self.board = np.full((board_size, board_size), None)
        self._prev_board = None
        np.random.seed(seed=r_seed)

        print(self.insert_random_tile(5))

        self.score = 0

    def get_board(self):
        return self.board

    def shift(self, direction):
        self._prev_board = self.board.copy()

        self.__getattribute__("shift_"+direction)()
        if not np.array_equiv(self._prev_board, self.board):
            self.insert_random_tile()

    def shift_right(self):
        # get non-Null tiles from row
        for row in range(4):
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
                new_row.append(t)
                score += t
            new_row.extend([None] * (4 - len(new_row)))  
            new_row.reverse()
            self.board[row,:] = new_row
        

    def shift_left(self):
        # get non-Null tiles from row
        for row in range(4):
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
                new_row.append(t)
                score += t
            new_row.extend([None] * (4 - len(new_row)))  
            self.board[row,:] = new_row
    
    def shift_down(self):
        # get non-Null tiles from column
        for col in range(4):
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
                new_col.append(t)
                score += t
            new_col.extend([None] * (4 - len(new_col)))  
            new_col.reverse()
            self.board[:,col] = new_col

    def shift_up(self):
        # get non-Null tiles from column
        for col in range(4):
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
                new_col.append(t)
                score += t
            new_col.extend([None] * (4 - len(new_col)))  
            self.board[:,col] = new_col


    def insert_random_tile(self, num_tile = 1):
        for i in range(num_tile):
            
            val = 2 if np.random.uniform(low=0.0, high=1.0) < 0.9 else 4  #generate a value (Based on official code of 2048)
            
            pos = np.argwhere(self.board == None)  #Get all available positions
            if len(pos) > 0:
                r = np.random.randint(0, len(pos))
                picked_tile = tuple(pos[r]) #Pick at random an availble tile

                self.board[picked_tile] = val



import os, pygame
from pygame.locals import *
class Demo2048:
    def __init__(self):
        self.actions = {
            "left": K_LEFT, 
            "right": K_RIGHT, 
            "up": K_UP, 
            "down": K_DOWN 
        }

        self.tile_color_scheme = ['#eee4da', '#eee1c9', '#f3b27a', '#f69664', '#f77c5f', '#f75f3b', '#edd073', '#f9f6f2', '#edc950', '#edc53f', '#edc22e']

        self.base = Base2048(board_size = 5) 

        self.inner_margin = 10 #px
        self.tile_spacing = 10
        self.tile_size = 57.5
        
        self.width = (self.base.board.shape[0] * self.tile_size) \
                     + (self.base.board.shape[0] - 1) * self.tile_spacing \
                     + (2 * self.inner_margin)
        self.height = self.width


        self._setup()
        self.draw(None)

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
                    color = self.tile_color_scheme[int(np.log2(tile)) - 1]



                t = pygame.draw.rect(self.screen, color, 
                                 pygame.Rect(x, y, self.tile_size, self.tile_size),
                                 border_top_left_radius=3,
                                 border_top_right_radius=3,
                                 border_bottom_left_radius=3,
                                 border_bottom_right_radius=3)

                font = pygame.freetype.SysFont("comicsansms", 0) 
                if tile != None:

                    text_rect = font.get_rect(str(tile), size = 50)
                    text_rect.center = t.center 
                    font.render_to(self.screen, text_rect, str(tile), "black", size = 50)  




                x += self.tile_size + self.tile_spacing
            y += self.tile_size + self.tile_spacing





        pygame.display.update()
        print(self.base.board)

    def _setup(self):
        """
        Setups up the pygame env, the display and game clock.
        """
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
    game = Demo2048()
    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
                pygame.quit()