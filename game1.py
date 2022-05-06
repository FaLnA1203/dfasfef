import pygame
from pygame.locals import *

pygame.init()
win_width = 1000
win_height = 1000

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('game')

tile_size = 50


hornet_image = pygame.image.load('idle_left.png')
bg_image = pygame.image.load('bg.png')


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(win, (255, 255, 255), (0, line * tile_size), (win_width, line * tile_size))
        pygame.draw.line(win, (255, 255, 255), (line * tile_size, 0), (line * tile_size, win_height))

class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_image = pygame.image.load('platform.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    image = pygame.transform.scale(dirt_image, (tile_size, tile_size))
                    image_rect = image.get_rect()
                    image_rect.x = col_count * tile_size
                    image_rect.y = row_count * tile_size
                    tile = (image, image_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            win.blit(tile[0], tile[1])

world_data = [[1, 1, 1, 1, 1], 
             [1, 0, 0, 0, 1], 
             [1, 0, 0, 0, 1], 
             [1, 0, 0, 0, 1], 
             [1, 1, 1, 1, 1],]

world = World(world_data)

run = True
while run:
    win.blit(bg_image, (0, 0))
    win.blit(hornet_image, (100, 100))

    world.draw()
    draw_grid()

    print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()