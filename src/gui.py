import pygame
import game_controller
import math
from constants import *


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Hive")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RED = (219, 12, 17)
BLUE = (7, 90, 138)
WHITE = (245, 245, 245)
BLACK = (43, 43, 43)
FULL_WHITE = (255, 255, 255)


class Rectangle:
    def __init__(self, x_top_left, x_bottom_right, y_top_left, y_bottom_right):
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.x_bottom_right = x_bottom_right
        self.y_bottom_right = y_bottom_right

    def __contains__(self, item):
        return self.x_top_left <= item[0] <= self.x_bottom_right and self.y_top_left <= item[1] <= self.y_bottom_right


# hit boxes
INSPECTOR_MODE_BUTTON = Rectangle(SCREEN_WIDTH - 100, SCREEN_WIDTH, SCREEN_HEIGHT - 100, SCREEN_HEIGHT)
PLAYER1_DECK = Rectangle(950, SCREEN_WIDTH, 0, SCREEN_HEIGHT / 2)
PLAYER2_DECK = Rectangle(950, SCREEN_WIDTH, SCREEN_HEIGHT / 2, SCREEN_HEIGHT)
BOARD_HITBOX = Rectangle(0, 950, 0, 750)
PASS_TURN = Rectangle(810, 940, 760, 785)


# screen assets
eye_active = pygame.image.load("../assets/eye_active.png")
eye_notactive = pygame.image.load("../assets/eye_n.png")

pass_turn = pygame.image.load("../assets/pass_turn_small.jpg")

spiderh = pygame.image.load("../assets/spider.JPG")
anth = pygame.image.load("../assets/ant.JPG")
cockroachh = pygame.image.load("../assets/cockroach.JPG")
queenh = pygame.image.load("../assets/queen.JPG")
grasshopperh = pygame.image.load("../assets/grasshopper.JPG")

hexagon = pygame.image.load("../assets/hexagon.png")
hexagon_valid = pygame.image.load("../assets/hexagon_valid.png")

A_1 = pygame.image.load("../assets/A_1.JPG")
A_2 = pygame.image.load("../assets/A_2.JPG")

C_1 = pygame.image.load("../assets/C_1.JPG")
C_2 = pygame.image.load("../assets/C_2.JPG")

S_1 = pygame.image.load("../assets/S_1.JPG")
S_2 = pygame.image.load("../assets/S_2.JPG")

G_1 = pygame.image.load("../assets/G_1.JPG")
G_2 = pygame.image.load("../assets/G_2.JPG")

Q_1 = pygame.image.load("../assets/Q_1.JPG")
Q_2 = pygame.image.load("../assets/Q_2.JPG")

# removing the white background from assets
hexagon.set_colorkey(FULL_WHITE)
hexagon_valid.set_colorkey(FULL_WHITE)

eye_active.set_colorkey(FULL_WHITE)
eye_notactive.set_colorkey(FULL_WHITE)

queenh.set_colorkey(FULL_WHITE)
spiderh.set_colorkey(FULL_WHITE)
cockroachh.set_colorkey(FULL_WHITE)
anth.set_colorkey(FULL_WHITE)
grasshopperh.set_colorkey(FULL_WHITE)

A_1.set_colorkey(FULL_WHITE)
A_2.set_colorkey(FULL_WHITE)

Q_1.set_colorkey(FULL_WHITE)
Q_2.set_colorkey(FULL_WHITE)

C_1.set_colorkey(FULL_WHITE)
C_2.set_colorkey(FULL_WHITE)

S_1.set_colorkey(FULL_WHITE)
S_2.set_colorkey(FULL_WHITE)

G_1.set_colorkey(FULL_WHITE)
G_2.set_colorkey(FULL_WHITE)

# loading the font
font = pygame.font.Font('../assets/8514fix.fon', 12)
font1 = pygame.font.Font('../assets/8514fix.fon', 8)


def draw_deck(player, screen, location):
    ctr = 0
    list_pieces_assets = [queenh, anth, cockroachh, grasshopperh, spiderh]
    for p in list_pieces_assets:
        screen.blit(p, (location[0] + ctr * 50, location[1]))
        under = font1.render(ALL_PIECES[ctr] + " =" + str(player.get_free_piece_count(ALL_PIECES[ctr])), True, (0, 0, 0))
        screen.blit(under, (location[0] + ctr * 50 + 10, location[1] + 57))
        ctr += 1


def draw_field(gs):
    # clear screen
    screen.fill(WHITE)

    # hex field drawer
    for i in range(gs.board.m):
        for j in range(gs.board.n):
            hexplace = gs.board(i, j)
            hex_pic = hexagon_valid if hexplace in gs.valid_moves else hexagon

            screen.blit(hex_pic, (j * 40 + (0 if (i % 2 == 0) else -20) + 35, i * 32))
            if hexplace.isEmpty():
                continue

            is_for_p1 = hexplace.top_piece.player == 1

            q_pic, a_pic, c_pic, s_pic, g_pic = (Q_1, A_1, C_1, S_1, G_1) if is_for_p1 else (Q_2, A_2, C_2, S_2, G_2)

            top_piece_type = hexplace.top_piece.type
            if top_piece_type == QUEEN:
                screen.blit(q_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 36, i * 32 + 10))
            elif top_piece_type == ANT:
                screen.blit(a_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 46, i * 32 + 8))
            elif top_piece_type == COCKROACH:
                screen.blit(c_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 43, i * 32 + 14))
            elif top_piece_type == SPIDER:
                screen.blit(s_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 40, i * 32 + 13))
            elif top_piece_type == GRASSHOPPER:
                screen.blit(g_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 38, i * 32 + 12))

    # field lines
    pygame.draw.line(screen, BLACK, (0, 750), (950, 750))
    pygame.draw.line(screen, BLACK, (950, 0), (950, SCREEN_HEIGHT))
    pygame.draw.line(screen, BLACK, (950, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
    #
    # # texts
    debugger_color = RED if gs.turn % 2 == 0 else BLUE
    #
    debugger = font.render(gs.debugger_text, True, debugger_color)
    screen.blit(debugger, (10, 760))
    player1text = font.render("Player 1", True, BLUE)
    screen.blit(player1text, (1082, 10))
    player2text = font.render("Player 2", True, RED)
    screen.blit(player2text, (1082, SCREEN_HEIGHT/2 + 10))
    #
    # # player deck drawer
    draw_deck(gs.p1, screen, (950, 40))
    draw_deck(gs.p2, screen, (950, SCREEN_HEIGHT/2 + 40))

    # eye
    eye = eye_notactive if not gs.inspector_mode else eye_active
    screen.blit(eye, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

    # pass turn
    screen.blit(pass_turn, (810, 760))

    # show
    pygame.display.flip()


def extract_board_i_j(x, y):
    i = math.floor(y / 32)
    j = math.floor((x - 35 + (0 if (i % 2 == 0) else 20)) / 40)
    return i, j


def extract_p1_deck_i_j(x, y):
    i = math.floor((y - 40) / 47)
    j = math.floor((x - 950) / 50)
    return i, j


def extract_p2_deck_i_j(x, y):
    i = math.floor((y - 440) / 47)
    j = math.floor((x - 950) / 50)
    return i, j


def tick(gs):
    # setting frame rate
    clock.tick(60)

    game_status = game_controller.game_status(gs)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        if game_status != ONGOING:
            gs.debugger_text = 'Game is a draw.' if game_status == DRAW else f'Player {game_status} won!'
            continue

        game_controller.handle_event(gs, event)

    draw_field(gs)

    return True
