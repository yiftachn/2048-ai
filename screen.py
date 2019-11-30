import pygame
import glob
from resizeimage import resizeimage
from PIL import Image
class Screen:

    def __init__(self,height,width,board):
        #tile factor
        self.w_factor = int(width /board.size)
        self.h_factor = int(height/board.size)
        #resize images in dir
        for file in glob.glob("*-orig.png"):
            with open(file, 'r+b') as f:
                with Image.open(f) as image:
                    cover = resizeimage.resize_contain(image, [self.w_factor,self.h_factor])
                    cover.save(str(file)[0:-9] + '.png', image.format)
        #initialize screen
        self.screen = pygame.display.set_mode((height,width))
        #load images onto board
        self.update_screen(board)
        pygame.display.flip()

    #def exit screen
    #def keyboard
    def update_screen(self,board):
        self.screen.fill([255,255,255])
        for row in range(board.size):
            for col in range(board.size):
                tile_image = pygame.image.load(str(board.board[row][col])+'.png')
                rect = tile_image.get_rect()
                self.screen.blit(tile_image,(col*self.h_factor,row*self.w_factor))
                #self.screen.blit(tile_image, rect)
        pygame.display.flip()