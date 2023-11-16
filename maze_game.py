import random
import time
import tkinter
from tkinter import *
import os
from collections import deque


window = tkinter.Tk()
window.title("Maze Game")
window.geometry("700x500+50+50")
window.resizable(True, True)


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
    global maze_cell_table
    current_cell.visited = True
    children = current_cell.get_children(maze_cell_table)

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
                    temp_table[y_index*2+1][x_index*2] = '1'
                if index == 1 and wall:
                    temp_table[y_index*2+1][x_index*2+2] = '1'
                if index == 2 and wall:
                    temp_table[y_index*2][x_index*2+1] = '1'
                if index == 3 and wall:
                    temp_table[y_index*2+2][x_index*2+1] = '1'
    return temp_table


def draw_table_outline(temp_table: list) -> list:
    length = len(temp_table)
    for row in temp_table:
        row[0] = row[length-1] = '1'

    temp_table[0] = temp_table[length-1] = ['1'] * length
    return temp_table


def draw_maze(maze_cell_table: list) -> list:
    temp_table = []
    table_length = len(maze_cell_table) * 2 + 1

    for x in range(table_length):
        if x % 2 == 0:
            temp_table.append(['0' if x % 2 != 0 else '1' for x in range(table_length)])
        else:
            temp_table.append(['0'] * table_length)
    
    temp_table = draw_walls(maze_cell_table, temp_table)
    temp_table = draw_table_outline(temp_table)

    # print('\n'.join([''.join(x) for x in temp_table]))
    return temp_table

# 미로에서 최단 경로 찾기 (BFS활용)
def search_path(start: tuple, end: tuple, maze: list) -> list:
    location_point = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    prev_location = [[None] * len(maze[0]) for i in range(len(maze))]

    queue = deque([start])

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = prev_location[x][y]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in location_point:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(maze) and 0 <= ny < len(maze[0])) or maze[nx][ny] == '1' or prev_location[nx][ny] is not None:
                continue

            prev_location[nx][ny] = (x, y)
            queue.append((nx, ny))
    
    return []



def play_computer():
    return


def play_user(event):
    global player
    if event.keysym == "Up":
        canvas.move(player, 0, -10)
    elif event.keysym == "Down":
        canvas.move(player, 0, 10)
    elif event.keysym == "Left":
        canvas.move(player, -10, 0)
    elif event.keysym == "Right":
        canvas.move(player, 10, 0)
    return


def select_stage():
    return


def show_countdown():
    return


def set_game_menu():
    return



canvas = Canvas(window, width=700, height=500, bg="#FFF8E5")
canvas.pack()



maze_size = 10  # 나중에 GUI 상에서 입력 받도록 수정
maze_cell_table = [[Cell(x, y) for x in range(maze_size)] for y in range(maze_size)]
current_cell = maze_cell_table[0][0]
stack = []
wall_size = 200/maze_size

make_maze_result = True
while make_maze_result:
    make_maze_result = make_maze()

maze_table = draw_maze(maze_cell_table)

maze_table_length = len(maze_table)
start = (1, 1)
end = (maze_table_length-2, maze_table_length-2)
maze_path = search_path(start, end, maze_table)

print(maze_path)

for x, y in maze_path:
    maze_table[x][y] = '*'

print('\n'.join([''.join(x) for x in maze_table]))

for y in range(maze_table_length):
    for x in range(maze_table_length):
        if maze_table[y][x] == '1':
            canvas.create_rectangle(x*wall_size, y*wall_size, (x+1)*wall_size, (y+1)*wall_size,
                                    fill="#C6D57E", outline="white")
            

img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\character.png').subsample(maze_size*3)
player = canvas.create_image(wall_size*1.5, wall_size*1.5, image=img)

canvas.bind_all("<KeyPress>", play_user)



window.mainloop()