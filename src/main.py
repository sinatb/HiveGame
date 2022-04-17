import pygame
import math

from src.board import Board
from src.player import Player
from constants import *
import movement

pygame.init()
pygame.display.set_caption("Hive")
screen = pygame.display.set_mode((1024, 720));

# board and the players
mb = Board(10, 10)

p1 = Player(1)
p2 = Player(2)

# screen assets
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


def main():
    running = True
    turn = 1
    selected_char = NO_PIECE
    moved_piece = NO_PIECE
    debugger_text = "Debugger"
    valid_moves = list()

    def current_player():
        return p1 if turn % 2 == 1 else p2

    draw_field(mb, debugger_text, screen, turn, valid_moves)

    # game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                if (600 < x < 1024) and (0 < y < 360):
                    if turn % 2 == 0:
                        debugger_text = "You cant chose from player 1's pieces"
                    else:
                        i = math.floor((y - 40) / 75)
                        j = math.floor((x - 600) / 80)
                        if i == 0:
                            debugger_text = "Player 1 has chosen " + ALL_PIECES[j]
                            selected_char = ALL_PIECES[j]
                        else:
                            debugger_text = "Chose valid Piece"

                elif (600 < x < 1024) and (360 < y < 720):
                    if turn % 2 == 1:
                        debugger_text = "You cant chose from player 2's pieces"
                    else:
                        i = math.floor((y - 400) / 75)
                        j = math.floor((x - 600) / 80)
                        if i == 0:
                            debugger_text = "Player 2 has chosen " + ALL_PIECES[j]
                            selected_char = ALL_PIECES[j]
                        else:
                            debugger_text = "Chose valid Piece"

                elif (0 < x < 600) and (0 < y < 500):
                    i = math.floor(y / 46)
                    j = math.floor((x - 35 + (0 if (i % 2 == 0) else 25)) / 51)
                    if (0 <= j < 10 and mb.places[i][j].isEmpty() and
                            (selected_char != NO_PIECE or moved_piece != NO_PIECE)):

                        if selected_char == NO_PIECE and moved_piece != NO_PIECE:

                            mb.places[i][j].top_piece = moved_piece
                            debugger_text = "Placed"
                            moved_piece = NO_PIECE
                            valid_moves = list()

                        elif selected_char != NO_PIECE and moved_piece == NO_PIECE:
                            if current_player().has_free_piece(selected_char):
                                mb.places[i][j].top_piece = current_player().get_free_piece(selected_char)
                                debugger_text = 'Placed'
                            else:
                                debugger_text = 'There is no such piece left'

                            selected_char = NO_PIECE

                        turn += 1 if (debugger_text == "Placed") else 0
                    elif mb.places[i][j].isNotEmpty() and selected_char == NO_PIECE and moved_piece == NO_PIECE:
                        if turn % 2 == mb.places[i][j].top_piece.player % 2:
                            moved_piece = mb.places[i][j].pop_top_piece()
                            valid_moves = movement.valid_moves_of(mb, mb.places[i][j], moved_piece.type)
                            debugger_text = "Moving piece"
                        else:
                            debugger_text = "Choose your own piece"
                    else:
                        if mb.places[i][j].isNotEmpty():
                            debugger_text = "The place has already been taken"
                            selected_char = NO_PIECE
                        else:
                            print(i, j)
                            debugger_text = "Please select a piece"

                draw_field(mb, debugger_text, screen, turn, valid_moves)

    pygame.quit()


def draw_deck(player, screen, location):
    ctr = 0
    list_pieces_assets = [queenh, anth, cockroachh, grasshopperh, spiderh]
    for p in list_pieces_assets:
        screen.blit(p, (location[0] + ctr * 80, location[1]))
        under = font.render(ALL_PIECES[ctr] + " = " + str(player.get_free_piece_count(ALL_PIECES[ctr])), True, (0, 0, 0))
        screen.blit(under, (location[0] + ctr * 80 + 15, location[1] + 85))
        ctr += 1


def draw_field(board, debugger_text, screen, turn, valid_moves):
    # clear screen
    screen.fill(WHITE)

    # hex field drawer
    for i in range(0, 10):
        for j in range(0, 10):
            hex_pic = hexagon_valid if board.places[i][j] in valid_moves else hexagon
            screen.blit(hex_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 35, i * 46))
            if board.places[i][j].isEmpty():
                continue

            is_for_p1 = board.places[i][j].top_piece.player == 1

            q_pic, a_pic, c_pic, s_pic, g_pic = (Q_1, A_1, C_1, S_1, G_1) if is_for_p1 else (Q_2, A_2, C_2, S_2, G_2)

            if board.places[i][j].top_piece.type == QUEEN:
                screen.blit(q_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 37, i * 46 + 15))
            elif board.places[i][j].top_piece.type == ANT:
                screen.blit(a_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 44, i * 46 + 10))
            elif board.places[i][j].top_piece.type == COCKROACH:
                screen.blit(c_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 43, i * 46 + 14))
            elif board.places[i][j].top_piece.type == SPIDER:
                screen.blit(s_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 40, i * 46 + 13))
            elif board.places[i][j].top_piece.type == GRASSHOPPER:
                screen.blit(g_pic, (j * 51 + (0 if (i % 2 == 0) else -25) + 38, i * 46 + 12))

    # field lines
    pygame.draw.line(screen, BLACK, (0, 500), (600, 500))
    pygame.draw.line(screen, BLACK, (600, 0), (600, 720))
    pygame.draw.line(screen, BLACK, (600, 360), (1024, 360))

    # texts
    debugger_color = RED if turn % 2 == 0 else BLUE

    debugger = font.render(debugger_text, True, debugger_color)
    screen.blit(debugger, (10, 510))
    player1text = font.render("Player 1", True, BLUE)
    screen.blit(player1text, (782, 10))
    player2text = font.render("Player 2", True, RED)
    screen.blit(player2text, (782, 370))

    # player deck drawer
    draw_deck(p1, screen, (600, 40))
    draw_deck(p2, screen, (600, 400))

    # show
    pygame.display.flip()


if __name__ == "__main__":
    main()
