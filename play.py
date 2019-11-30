from engine import Board
import pygame
from screen import Screen
import os
def main():
    b = Board(4,debug=False,cubes = 14)
    s = Screen(500,500,b)
    running = True
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYDOWN,pygame.QUIT])
    move = 'stay'
    while(not b.lost and running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    move = 'DOWN'
                elif event.key == pygame.K_UP:
                    move = 'UP'
                elif event.key == pygame.K_LEFT:
                    move = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    move = 'RIGHT'
        #move = input()
        #move = move.upper()
        b.move_board(move)
        move = 'stay'
        s.update_screen(b)
    return 0
if __name__ == '__main__':
    main()
