import pygame, sys, random
from pygame.locals import *
import time

BOARDWIDTH = 4
BOARDHEIGHT = 4
TILE_SIZE = 80
TILE_SPACE = 2
START_POS = (156, 76)

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)




def get_tile_rects(start_pos):
    tile_rects = []
    empty_tile = (random.randint(0, 3), random.randint(0, 3))
    random_letters = [chr(i) for i in range(65, 65 + 15)]
    random.shuffle(random_letters)
    n = 0
    for i in range(4):
        tile_rects.append([])
        for j in range(4):
            rect = pygame.Rect(
                (start_pos[0] + i * (TILE_SIZE + TILE_SPACE),
                 start_pos[1] + j * (TILE_SIZE + TILE_SPACE),
                 TILE_SIZE, TILE_SIZE))
            if (i, j) == empty_tile:
                tile_rects[i].append([rect, ''])
                continue
            else:
                tile_rects[i].append([rect, random_letters[n]])
            n += 1
    return tile_rects, empty_tile


def draw_tiles(tile_rects, empty_tile):
    global text_font, screen
    for i in range(4):
        for j in range(4):
            if (i, j) == empty_tile:
                pygame.draw.rect(screen, WHITE, tile_rects[i][j][0])
            else:
                pygame.draw.rect(screen, GREEN, tile_rects[i][j][0])
                txt_suf = text_font.render(tile_rects[i][j][1], True, BLACK)
                screen.blit(txt_suf, tile_rects[i][j][0])


def get_clicked_rect(x, y, tile_rects, empty_tile):
    for i in range(4):
        for j in range(4):
            if tile_rects[i][j][0].collidepoint(x, y) and (i, j) != empty_tile:
                return (tile_rects[i][j][0], (i, j))
    return (None, None)


def is_valid_pos(pos):
    return 0 <= pos[0] <= 3 and 0 <= pos[1] <= 3


def check_move(tile_rects, pos):
    return tile_rects[pos[0]][pos[1]][1] == ''


def slide_to_pos(rect, pos, slide_dir, tile_rects):
    global empty_tile
    tile_rects[pos[0]][pos[1]][1], tile_rects[empty_tile[0]][empty_tile[1]][1] = \
        tile_rects[empty_tile[0]][empty_tile[1]][1], tile_rects[pos[0]][pos[1]][1]

    empty_tile = pos


def win_check():
    global win_rects, tile_rects
    for i in range(4):
        for j in range(4):
            if tile_rects[j][i][1] != win_rects[i][j]:
                return False
    return True


pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Slide Puzzle')
screen.fill(WHITE)
game_clock = pygame.time.Clock()
text_font = pygame.font.SysFont('arial', 80)
tile_rects, empty_tile = get_tile_rects(START_POS)
draw_tiles(tile_rects, empty_tile)
slide_dir = ''
win_rects = [[chr(j) for j in range(65 + i * 4, 65 + i * 4 + 4)] for i in range(4)]
win_rects[-1][-1] = ''

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONUP:
            x, y = event.pos[0], event.pos[1]
            (rect, pos) = get_clicked_rect(x, y, tile_rects, empty_tile)
            if pos:
                west_pos = pos[0] - 1, pos[1]
                east_pos = pos[0] + 1, pos[1]
                north_pos = pos[0], pos[1] - 1
                south_pos = pos[0], pos[1] + 1
                if is_valid_pos(west_pos) and check_move(tile_rects, west_pos):
                    slide_dir = 'W'
                elif is_valid_pos(east_pos) and check_move(tile_rects, east_pos):
                    slide_dir = 'E'
                elif is_valid_pos(north_pos) and check_move(tile_rects, north_pos):
                    slide_dir = 'N'
                elif is_valid_pos(south_pos) and check_move(tile_rects, south_pos):
                    slide_dir = 'S'

    if slide_dir:
        slide_to_pos(rect, pos, slide_dir, tile_rects)
        slide_dir = ''

    draw_tiles(tile_rects, empty_tile)

    pygame.display.update()

    if win_check():
        break
    game_clock.tick(FPS)