import pygame
import math

from src.board import Board
from src.player import Player

pygame.init()
pygame.display.set_caption("Hive")
screen = pygame.display.set_mode((1024, 720));

# board and the players
mb = Board(10, 10)
mb.draw()

p1 = Player(1)
p2 = Player(2)

# screen assets
spiderh = pygame.image.load("../assets/spider.JPG")
anth = pygame.image.load("../assets/ant.JPG")
cockroachh = pygame.image.load("../assets/cockroach.JPG")
queenh = pygame.image.load("../assets/queen.JPG")
grasshopperh = pygame.image.load("../assets/grasshopper.JPG")

hexagon = pygame.image.load("../assets/hexagon.png")
hexagon_used = pygame.image.load("../assets/hexagon_valid.png")

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
hexagon.set_colorkey((255, 255, 255))
hexagon_used.set_colorkey((255, 255, 255))

queenh.set_colorkey((255, 255, 255))
spiderh.set_colorkey((255, 255, 255))
cockroachh.set_colorkey((255, 255, 255))
anth.set_colorkey((255, 255, 255))
grasshopperh.set_colorkey((255, 255, 255))

A_1.set_colorkey((255, 255, 255))
A_2.set_colorkey((255, 255, 255))

Q_1.set_colorkey((255, 255, 255))
Q_2.set_colorkey((255, 255, 255))

C_1.set_colorkey((255, 255, 255))
C_2.set_colorkey((255, 255, 255))

S_1.set_colorkey((255, 255, 255))
S_2.set_colorkey((255, 255, 255))

G_1.set_colorkey((255, 255, 255))
G_2.set_colorkey((255, 255, 255))

# loading the font
font = pygame.font.Font('../assets/8514fix.fon', 12)


# In[44]:


def main():
    running = True
    turn = 1
    selected_char = "X"
    moved_piece = "N"
    debuger_text = "Debuger"

    draw_field(mb, debuger_text, screen)

    # game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                (x, y) = pygame.mouse.get_pos()
                if ((x > 600 and x < 1024) and (y > 0 and y < 360)):
                    if (turn % 2 == 0):
                        debuger_text = "You cant chose from player 1's pieces"
                    else:
                        list_pieces = ["Q", "A", "C", "G", "S", "S"]
                        i = math.floor((y - 40) / 75)
                        j = math.floor((x - 600) / 80)
                        if (i == 0):
                            debuger_text = "Player 1 has chosen " + list_pieces[j]
                            selected_char = list_pieces[j]
                        else:
                            debuger_text = "Chose valid Piece"

                elif ((x > 600 and x < 1024) and (y > 360 and y < 720)):
                    if (turn % 2 == 1):
                        debuger_text = "You cant chose from player 2's pieces"
                    else:
                        list_pieces = ["Q", "A", "C", "G", "S", "S"]
                        i = math.floor((y - 400) / 75)
                        j = math.floor((x - 600) / 80)
                        if (i == 0):
                            debuger_text = "Player 2 has chosen " + list_pieces[j]
                            selected_char = list_pieces[j]
                        else:
                            debuger_text = "Chose valid Piece"

                elif ((x > 0 and x < 600) and (y > 0 and y < 500)):
                    i = math.floor(y / 46)
                    j = math.floor((x - 35 + (0 if (i % 2 == 0) else 25)) / 51)
                    if (j >= 0 and j < 10 and mb.places[i][j].piece == "N" and (
                            selected_char != "X" or moved_piece != "N")):
                        if (selected_char == "X" and moved_piece != "N"):
                            if (turn % 2 == 1):
                                p1.add_piece(moved_piece)
                                p1.place_piece(moved_piece, mb, i, j)
                            else:
                                p2.add_piece(moved_piece)
                                p2.place_piece(moved_piece, mb, i, j)
                            debuger_text = "Placed"
                            moved_piece = "N"
                        elif (selected_char != "X" and moved_piece == "N"):
                            if (turn % 2 == 1):
                                debuger_text = "Placed" if p1.place_piece(selected_char, mb, i,
                                                                          j) else "There is no such piece left"
                            else:
                                debuger_text = "Placed" if p2.place_piece(selected_char, mb, i,
                                                                          j) else "There is no such piece left"
                            selected_char = "X"
                        turn += 1 if (debuger_text == "Placed") else 0
                    elif (mb.places[i][j].piece != "N" and selected_char == "X" and moved_piece == "N"):
                        if (turn % 2 == mb.places[i][j].player_num % 2):
                            moved_piece = mb.places[i][j].piece
                            mb.places[i][j].piece = "N"
                            mb.places[i][j].player_num = -1
                            debuger_text = "Moving piece"
                        else:
                            debuger_text = "Chose your own piece"
                    else:
                        if (mb.places[i][j].piece != "N"):
                            debuger_text = "The place has already been taken"
                            selected_char = "X"
                        else:
                            debuger_text = "Please select a piece"

                draw_field(mb, debuger_text, screen)

    pygame.quit()


def draw_deck(player, screen, location):
    ctr = 0
    list_pieces = ["Q", "A", "C", "G", "S"]
    list_pieces_assets = [queenh, anth, cockroachh, grasshopperh, spiderh]
    for p in list_pieces_assets:
        screen.blit(p, (location[0] + ctr * 80, location[1]))
        under = font.render(list_pieces[ctr] + " = " + str(player.pieces[list_pieces[ctr]]), True, (0, 0, 0))
        screen.blit(under, (location[0] + ctr * 80 + 15, location[1] + 85))
        ctr += 1


def draw_field(board, debuger_text, screen):
    # clear screen
    screen.fill((255, 255, 255))

    # hex field drawer
    for i in range(0, 10):
        for j in range(0, 10):
            screen.blit(hexagon, (j * 51 + (0 if (i % 2 == 0) else -25) + 35, i * 46))
            if (board.places[i][j].player_num == 1):
                if (board.places[i][j].piece == "Q"):
                    screen.blit(Q_1, (j * 51 + (0 if (i % 2 == 0) else -25) + 37, i * 46 + 15))
                elif (board.places[i][j].piece == "A"):
                    screen.blit(A_1, (j * 51 + (0 if (i % 2 == 0) else -25) + 44, i * 46 + 10))
                elif (board.places[i][j].piece == "C"):
                    screen.blit(C_1, (j * 51 + (0 if (i % 2 == 0) else -25) + 43, i * 46 + 14))
                elif (board.places[i][j].piece == "S"):
                    screen.blit(S_1, (j * 51 + (0 if (i % 2 == 0) else -25) + 40, i * 46 + 13))
                elif (board.places[i][j].piece == "G"):
                    screen.blit(G_1, (j * 51 + (0 if (i % 2 == 0) else -25) + 38, i * 46 + 12))
            else:
                if (board.places[i][j].piece == "Q"):
                    screen.blit(Q_2, (j * 51 + (0 if (i % 2 == 0) else -25) + 37, i * 46 + 15))
                elif (board.places[i][j].piece == "A"):
                    screen.blit(A_2, (j * 51 + (0 if (i % 2 == 0) else -25) + 44, i * 46 + 10))
                elif (board.places[i][j].piece == "C"):
                    screen.blit(C_2, (j * 51 + (0 if (i % 2 == 0) else -25) + 43, i * 46 + 14))
                elif (board.places[i][j].piece == "S"):
                    screen.blit(S_2, (j * 51 + (0 if (i % 2 == 0) else -25) + 40, i * 46 + 13))
                elif (board.places[i][j].piece == "G"):
                    screen.blit(G_2, (j * 51 + (0 if (i % 2 == 0) else -25) + 38, i * 46 + 12))

    # field lines
    pygame.draw.line(screen, (255, 0, 255), (0, 500), (600, 500))
    pygame.draw.line(screen, (255, 0, 255), (600, 0), (600, 720))
    pygame.draw.line(screen, (255, 0, 255), (600, 360), (1024, 360))

    # texts
    debuger = font.render(debuger_text, True, (0, 0, 255))
    screen.blit(debuger, (10, 510))
    player1text = font.render("Player 1", True, (0, 0, 255))
    screen.blit(player1text, (782, 10))
    player2text = font.render("Player 2", True, (255, 0, 0))
    screen.blit(player2text, (782, 370))

    # player deck drawer
    draw_deck(p1, screen, (600, 40))
    draw_deck(p2, screen, (600, 400))

    # show
    pygame.display.flip()


if __name__ == "__main__":
    main()
