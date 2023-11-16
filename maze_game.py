import random
import time
import tkinter
from tkinter import *
import os




class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = [True, True, True, True]  # Left, Right, Up, Down
    
    # maze_table에는 Cell 객체가 들어감 (2차원 리스트)
    def get_children(self, maze_table: list) -> list:
        location_point = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        children = []
        for x, y in location_point:
            if self.x+x in [len(maze_table), -1] or self.y+y in [-1, len(maze_table)]:
                continue

            child = maze_table[self.y+y][self.x+x]
            if child.visited:
                continue

            children.append(child)
        return children


def make_maze():
    global current_cell
    global maze_table
    current_cell.visited = True
    children = current_cell.get_children(maze_table)

    if children:
        choice_cell = random.choice(children)
        choice_cell.visited = True

        stack.append(current_cell)

        remove_walls(current_cell, choice_cell)
        current_cell = choice_cell
        return True
    elif stack:
        current_cell = stack.pop()
        return True
    else:
        return False


def remove_walls(current_cell: Cell, choice_cell: Cell):
    if choice_cell.x > current_cell.x:
        choice_cell.walls[0] = False
        current_cell.walls[1] = False
    elif choice_cell.x < current_cell.x:
        choice_cell.walls[1] = False
        current_cell.walls[0] = False
    elif choice_cell.y > current_cell.y:
        choice_cell.walls[2] = False
        current_cell.walls[3] = False
    elif choice_cell.y < current_cell.y:
        choice_cell.walls[3] = False
        current_cell.walls[2] = False


def draw_walls(maze_table: list, temp_table: list) -> list:
    for y_index, y_value in enumerate(maze_table):
        for x_index, x_value in enumerate(y_value):
            for index, wall in enumerate(x_value.walls):
                if index == 0 and wall:
                    temp_table[y_index*2+1][x_index*2] = '⬛'
                if index == 1 and wall:
                    temp_table[y_index*2+1][x_index*2+2] = '⬛'
                if index == 2 and wall:
                    temp_table[y_index*2][x_index*2+1] = '⬛'
                if index == 3 and wall:
                    temp_table[y_index*2+2][x_index*2+1] = '⬛'
    return temp_table


def draw_table_outline(temp_table: list) -> list:
    length = len(temp_table)
    for row in temp_table:
        row[0] = row[length-1] = '⬛'

    temp_table[0] = temp_table[length-1] = ['⬛'] * length
    return temp_table


def draw_maze(maze_table: list):
    temp_table = []
    table_length = len(maze_table) * 2 + 1

    for x in range(table_length):
        if x % 2 == 0:
            temp_table.append(['⬜' if x % 2 != 0 else '⬛' for x in range(table_length)])
        else:
            temp_table.append(['⬜'] * table_length)
    
    temp_table = draw_walls(maze_table, temp_table)
    temp_table = draw_table_outline(temp_table)

    print('\n'.join([''.join(x) for x in temp_table]))


def search_path():
    return


def play_computer():
    return


def play_user():
    return


def select_stage():
    return


def show_countdown():
    return


def set_game_menu():
    return



maze_size = 10  # 나중에 GUI 상에서 입력 받도록 수정
maze_table = [[Cell(x, y) for x in range(maze_size)] for y in range(maze_size)]
current_cell = maze_table[0][0]
stack = []

make_maze_result = True
while make_maze_result:
    make_maze_result = make_maze()

draw_maze(maze_table)