import pygame
import math

from src.board import Board
from src.player import Player
from constants import *
import movement

pygame.init()
pygame.display.set_caption("Hive")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

# board and the players
mb = Board(22, 22)

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
font1 = pygame.font.Font('../assets/8514fix.fon', 8)


def main():
    running = True
    turn = 1
    selected_char = NO_PIECE
    moved_piece = NO_PIECE
    debugger_text = "Debugger"
    valid_moves = list()

    def player1_turn():
        return turn % 2 == 1

    def current_player():
        return p1 if player1_turn() else p2

    draw_field(mb, debugger_text, screen, turn, valid_moves)

    # game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = event.pos
                if (950 < x < SCREEN_WIDTH) and (0 < y < SCREEN_HEIGHT/2):
                    if not player1_turn():
                        debugger_text = "You can't chose from player 1's pieces"
                    else:
                        i = math.floor((y - 40) / 47)
                        j = math.floor((x - 950) / 50)
                        if i == 0:
                            debugger_text = "Player 1 has chosen " + ALL_PIECES[j]
                            selected_char = ALL_PIECES[j]
                        else:
                            debugger_text = "Chose valid Piece"

                elif (950 < x < SCREEN_WIDTH) and (SCREEN_HEIGHT/2 < y < SCREEN_HEIGHT):
                    if player1_turn():
                        debugger_text = "You can't chose from player 2's pieces"
                    else:
                        i = math.floor((y - 440) / 47)
                        j = math.floor((x - 950) / 50)
                        if i == 0:
                            debugger_text = "Player 2 has chosen " + ALL_PIECES[j]
                            selected_char = ALL_PIECES[j]
                        else:
                            debugger_text = "Choose valid Piece"

                elif (0 < x < 950) and (0 < y < 750):
                    i = math.floor(y / 32)
                    j = math.floor((x - 35 + (0 if (i % 2 == 0) else 20)) / 40)
                    if (0 <= j < 22 and mb.places[i][j].isEmpty() and
                            (selected_char != NO_PIECE or moved_piece != NO_PIECE)):

                        if selected_char == NO_PIECE and moved_piece != NO_PIECE:
                            if mb.places[i][j] in valid_moves:
                                mb.places[i][j].top_piece = moved_piece
                                debugger_text = PLACED
                                moved_piece = NO_PIECE
                                valid_moves = list()
                            else:
                                debugger_text = 'This move is illegal'
                        elif selected_char != NO_PIECE and moved_piece == NO_PIECE:
                            if not current_player().has_free_piece(selected_char):
                                debugger_text = 'There is no such piece left'
                                selected_char = NO_PIECE
                            elif turn > 2 and not movement.can_accept_new_piece(mb, mb.places[i][j], current_player().num):
                                debugger_text = 'A new piece cannot be placed here'
                            else:
                                mb.places[i][j].top_piece = current_player().get_free_piece(selected_char)
                                debugger_text = PLACED
                                selected_char = NO_PIECE

                        turn += 1 if (debugger_text == PLACED) else 0
                    elif mb.places[i][j].isNotEmpty() and selected_char == NO_PIECE and moved_piece == NO_PIECE:
                        if turn % 2 == mb.places[i][j].top_piece.player % 2:
                            place = mb.places[i][j]
                            valid_moves = movement.valid_moves_of(mb, place, place.top_piece.type, should_pop=True)
                            if len(valid_moves) <= 0:
                                debugger_text = 'This piece has no legal moves'
                            else:
                                moved_piece = place.pop_top_piece()
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
        screen.blit(p, (location[0] + ctr * 50, location[1]))
        under = font1.render(ALL_PIECES[ctr] + " =" + str(player.get_free_piece_count(ALL_PIECES[ctr])), True, (0, 0, 0))
        screen.blit(under, (location[0] + ctr * 50 + 10, location[1] + 57))
        ctr += 1


def draw_field(board, debugger_text, screen, turn, valid_moves):
    # clear screen
    screen.fill(WHITE)

    # hex field drawer
    for i in range(board.m):
        for j in range(board.n):
            hex_pic = hexagon_valid if board.places[i][j] in valid_moves else hexagon

            screen.blit(hex_pic, (j * 40 + (0 if (i % 2 == 0) else -20) + 35, i * 32))
            if board.places[i][j].isEmpty():
                continue

            is_for_p1 = board.places[i][j].top_piece.player == 1

            q_pic, a_pic, c_pic, s_pic, g_pic = (Q_1, A_1, C_1, S_1, G_1) if is_for_p1 else (Q_2, A_2, C_2, S_2, G_2)

            if board.places[i][j].top_piece.type == QUEEN:
                screen.blit(q_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 36, i * 32 + 10))
            elif board.places[i][j].top_piece.type == ANT:
                screen.blit(a_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 46, i * 32 + 8))
            elif board.places[i][j].top_piece.type == COCKROACH:
                screen.blit(c_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 43, i * 32 + 14))
            elif board.places[i][j].top_piece.type == SPIDER:
                screen.blit(s_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 40, i * 32 + 13))
            elif board.places[i][j].top_piece.type == GRASSHOPPER:
                screen.blit(g_pic, (j * 40 + (0 if (i % 2 == 0) else -25) + 38, i * 32 + 12))

    # field lines
    pygame.draw.line(screen, BLACK, (0, 750), (950, 750))
    pygame.draw.line(screen, BLACK, (950, 0), (950, SCREEN_HEIGHT))
    pygame.draw.line(screen, BLACK, (950, SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT/2))
    #
    # # texts
    debugger_color = RED if turn % 2 == 0 else BLUE
    #
    debugger = font.render(debugger_text, True, debugger_color)
    screen.blit(debugger, (10, 760))
    player1text = font.render("Player 1", True, BLUE)
    screen.blit(player1text, (1082, 10))
    player2text = font.render("Player 2", True, RED)
    screen.blit(player2text, (1082, SCREEN_HEIGHT/2 + 10))
    #
    # # player deck drawer
    draw_deck(p1, screen, (950, 40))
    draw_deck(p2, screen, (950, SCREEN_HEIGHT/2 + 40))

    # show
    pygame.display.flip()


if __name__ == "__main__":
    main()
