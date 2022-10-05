#!/usr/bin/env python
"""Conways Game of Life - written for pygame"""

import numpy as np
import pygame


# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (175, 175, 175)
GRAY = (100, 100, 100)
RED = (200, 10, 20)

# GAME/UI SETTINGS
HORIZONTAL_CELLS = 30
VERTICAL_CELLS = 20
BORDER = 2
TICK_SPEED = 20

# CUSTOM PYGAME EVENT
TICK = pygame.USEREVENT + 1


def createBoard(width, height):
    """
    Creates a numpy array of zeroes
    :param width: integer
        Width of array
    :param height: integer
        Height of array
    :return:
        Returns empty numpy array
    """
    board = np.zeros((width, height))
    return board


def draw(board, surface, cellsize, border_size):
    """
    Draws black squares on board
    :param board: numpy array
        Contains the data of current board state
    :param surface: pygame surface
        Background surface the squares are drawn on
    :param cellsize: integer
        Size of cells
    :param border_size: integer
        Width of borders
    :return:
        Returns populated numpy array
    """
    for i, x in enumerate(board):
        for j, y in enumerate(x):
            if y == 0:
                col = BLACK
            else:
                col = WHITE
            pygame.draw.rect(surface, col, (border_size + j * (cellsize + border_size),
                                            border_size + (i + 1) * (cellsize + border_size),
                                            cellsize, cellsize))
    return board


def draw_pause(surface, border_size, cellsize):
    """
    Draws pause symbol in top left
    :param surface: pygame surface
        Background surface the pause symbol is drawn on
    :param border_size: integer
        Width of borders
    :param cellsize: integer
        Size of cells
    """
    pygame.draw.rect(surface, LIGHTGRAY,
                     (border_size, border_size, cellsize, cellsize))
    pygame.draw.rect(surface, GRAY,
                     (border_size + 2, border_size + 2, cellsize - 4, cellsize - 4), width=2)
    pygame.draw.rect(surface, BLACK,
                     (border_size + 9, border_size + 7, 4, cellsize - 14))
    pygame.draw.rect(surface, BLACK,
                     (border_size + 17, border_size + 7, 4, cellsize - 14))
    pygame.display.update()


def draw_play(surface, border_size, cellsize):
    """
    Draws play symbol in top left
    :param surface: pygame surface
        Background surface the play symbol is drawn on
    :param border_size: integer
        Width of borders
    :param cellsize: integer
        Size of cells
    """
    pygame.draw.rect(surface, LIGHTGRAY,
                     (border_size, border_size, cellsize, cellsize))
    pygame.draw.rect(surface, GRAY,
                     (border_size + 2, border_size + 2, cellsize - 4, cellsize - 4), width=2)
    pygame.draw.polygon(surface, RED, [(11, 8), (11, 25), (23, 16)])
    pygame.display.update()


def pos_to_square(pos, cellsize, border_size, dim_x, dim_y):
    """
    Converts mouse click position to array index square that was clicked on
    Additionally identifies if the pause button was pressed
    :param pos: tuple
        Mouse position
    :param cellsize: integer
        Size of cells
    :param border_size: integer
        Width of borders
    :param dim_x: integer
        Number of horizontal cells
    :param dim_y: integer
        Number of vertical cells
    :return:
        Returns square index (tuple) and pause state (boolean)
    """
    x, y = (int(pos[0] / (cellsize + border_size)), int(pos[1] / (cellsize + border_size)))

    if x >= dim_y:
        x = dim_y - 1
    if y >= dim_x:
        y = dim_x - 1

    if x == y == 0:
        pause = True
    else:
        pause = False

    square = (x, y - 1)
    return square, pause


def change_square(mainBoard, square):
    """
    Flips a squares state on click
    :param mainBoard: numpy array
        Contains the data of current board state
    :param square: tuple
        Index of square to be changed
    :return:
        Returns numpy array with updated board state
    """
    state = mainBoard[square[1], square[0]]
    if state == 0:
        mainBoard[square[1], square[0]] = 1
    else:
        mainBoard[square[1], square[0]] = 0
    return mainBoard


def rules(alive, count):
    """
    Applies Game of Life rules to determine a squares new state
    :param alive: integer (1 or 0)
        1 = alive, 0 = dead
    :param count: integer
        The number of neighbouring squares that are alive
    :return:
        Returns the new alive state of a square (integer [1 or 0]), as well as its colour (var)
    """
    if (alive == 1) and ((count == 2) or (count == 3)):
        return 1, WHITE
    elif (alive == 0) and (count == 3):
        return 1, WHITE
    else:
        return 0, BLACK


def tick(board, surface, cellsize, border_size):
    """
    Counts how many neighbouring squares are alive for each square, and calls Rules on each one
    Additionally draws the squares for the next frame
    :param board: numpy array
        Contains the data of current board state
    :param surface: pygame surface
        Surface on which new squares are drawn
    :param cellsize: integer
        Size of Cells
    :param border_size: integer
        Width of borders
    :return:
        Returns updated numpy array with new game state data
    """
    width, height = np.shape(board)
    outputBoard = np.copy(board)
    for i, x in enumerate(board):
        for j, y in enumerate(x):
            count = 0
            nPos = [(i - 1, j), (i - 1, j - 1), (i, j - 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1), (i, j + 1),
                    (i - 1, j + 1)]
            for neighbour in nPos:
                if neighbour[0] == width:
                    neighbour = (0, neighbour[1])
                if neighbour[1] == height:
                    neighbour = (neighbour[0], 0)
                if board[neighbour] == 1:
                    count += 1
            outputBoard[i, j] = rules(y, count)[0]
            outputBoard[i, j], col = rules(y, count)
            pygame.draw.rect(surface, col, (border_size + j * (cellsize + border_size),
                                            border_size + (i + 1) * (cellsize + border_size),
                                            cellsize, cellsize))
    return outputBoard


def paused(mainBoard, surface, cellsize, border_size, dimx, dimy):
    """
    Executes state changes on click, unpauses the game, and sets new events to register the next tick
    :param mainBoard: numpy array
        Contains the data of current board state
    :param surface: pygame surface
        Surface on which new squares are drawn
    :param cellsize: integer
        Size of Cells
    :param border_size: integer
        Width of borders
    :param dimx: integer
        Number of horizontal cells
    :param dimy: integer
        Number of vertical cells
    """
    draw_play(surface, border_size, cellsize)
    p = True
    while p:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=5)[0]:
                    pos = pygame.mouse.get_pos()
                    square, pause = pos_to_square(pos, cellsize, border_size, dimx, dimy)
                    if pause:
                        pygame.time.set_timer(TICK, TICK_SPEED)
                        play(mainBoard, surface, cellsize, border_size, dimx, dimy)
                        p = False
                    elif square[1] == -1:
                        pass
                    else:
                        mainBoard = change_square(mainBoard, square)
                        mainBoard = draw(mainBoard, surface, cellsize, border_size)
                        pygame.display.update()


def play(mainBoard, surface, cellsize, border_size, dimx, dimy):
    """
    Execute ticks every event loop, and identifies if the game needs to be paused
    :param mainBoard: numpy array
        Contains the data of current board state
    :param surface: pygame surface
        Surface on which new squares are drawn
    :param cellsize: integer
        Size of Cells
    :param border_size: integer
        Width of borders
    :param dimx: integer
        Number of horizontal cells
    :param dimy: integer
        Number of vertical cells
    """
    draw_pause(surface, border_size, cellsize)
    t = True
    while t:
        pause, speed = False, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=5)[0]:
                    pos = pygame.mouse.get_pos()
                    square, pause = pos_to_square(pos, cellsize, border_size, dimx, dimy)
            if event.type == TICK:
                mainBoard = tick(np.copy(mainBoard), surface, cellsize, border_size)
                pygame.display.update()
                pygame.time.set_timer(TICK, TICK_SPEED)
        if pause:
            paused(mainBoard, surface, cellsize, border_size, dimx, dimy)
            t = False
        else:
            pass


def init(mainBoard, dim_x, dim_y):
    """
    Initialises the pygame, draws the background and launches the game in a paused state
    :param mainBoard: numpy array
        Contains the data of current board state
    :param dim_x: integer
        Number of horizontal cells
    :param dim_y: integer
        Number of vertical cells
    """
    cellsize = 30
    border_size = BORDER
    window_width = (dim_x + 1) * (cellsize + border_size) + border_size
    window_height = dim_y * (cellsize + border_size) + border_size
    pygame.init()
    surface = pygame.display.set_mode((window_height, window_width))
    pygame.display.set_caption("John Conway's Game of Life - Pause to edit squares")
    surface.fill(GRAY)
    pygame.draw.rect(surface, LIGHTGRAY,
                     (2 * border_size + 1 * cellsize, border_size, (cellsize + border_size) * dim_y - border_size,
                      cellsize))
    mainBoard = draw(mainBoard, surface, cellsize, border_size)
    pygame.display.update()
    paused(mainBoard, surface, cellsize, border_size, dim_x, dim_y)


if __name__ == "__main__":
    """
    Creates a blank board and runs the game on it
    """
    main_Board = createBoard(VERTICAL_CELLS, HORIZONTAL_CELLS)
    init(main_Board, VERTICAL_CELLS, HORIZONTAL_CELLS)

__author__ = "Louis De Neve"
__version__ = "1.0.3"
__status__ = "Development"
