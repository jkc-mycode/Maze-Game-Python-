import random
import time
import tkinter
from tkinter import *
import os
from collections import deque


window = tkinter.Tk()
window.title("Maze Game")
window.geometry("800x660+50+50")
window.resizable(False, False)


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


def play_computer(player, start, maze_path):
    global is_goal
    current = list(map(int, start))
    for x, y in maze_path:
        if is_goal: return
        current[0] = y - current[0]
        current[1] = x - current[1]
        canvas.move(player, current[0]*wall_size, current[1]*wall_size)
        current[0] = y
        current[1] = x
        time.sleep(0.1)
        canvas.update()

        if current == list(end):
            is_goal = True
            img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\goal_popup.png')
            label = Label(window, image=img)
            label.image = img
            label.place(x=60, y=60)


# 유저 플레이 및 캐릭터 이동 함수
def play_user(event):
    global player
    global start
    global is_goal
    directions = {'Left': (0, -1), 'Right': (0, 1), 'Up': (-1, 0), 'Down': (1, 0)}
    direction = directions.get(event.keysym)
    if direction is None:
        return
    
    start = list(start)
    nx, ny = start[0] + direction[0], start[1] + direction[1]
    print(nx, ny)
    if not (1 <= nx < len(maze_table) and 1 <= ny < len(maze_table[0])) or maze_table[nx][ny] == '1':
        return
    
    canvas.move(player, direction[1]*wall_size, direction[0]*wall_size)
    start[0], start[1] = nx, ny
    start = tuple(start)

    if start == end:
        is_goal = True
        img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\goal_popup.png')
        label = Label(window, image=img)
        label.image = img
        label.place(x=60, y=60)
        
        

def show_countdown():
    return


def select_mode(mode: int):
    if mode == 1:
        play_computer(player, start, maze_path)
    else:
        canvas.bind_all("<KeyPress>", play_user)
    return


def select_stage(size: int):
    canvas.destroy()
    main(size)


def restart():
    window.destroy()
    os.system('python3 Maze_Game_BackTracking\\maze_game.py')


def exit():
    window.quit()


def make_game_menu():
    menubar = tkinter.Menu(window)
    menu_mode = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Mode", menu=menu_mode)
    menu_mode.add_command(label="Auto", command=lambda: select_mode(1))
    menu_mode.add_command(label="User", command=lambda: select_mode(2))

    menu_stage = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Stage", menu=menu_stage)
    menu_stage.add_command(label="5", command=lambda: select_stage(5))
    menu_stage.add_command(label="10", command=lambda: select_stage(10))
    menu_stage.add_command(label="15", command=lambda: select_stage(15))
    menu_stage.add_command(label="20", command=lambda: select_stage(20))
    menu_stage.add_command(label="25", command=lambda: select_stage(25))
    menu_stage.add_command(label="30", command=lambda: select_stage(30))

    menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Menu", menu=menu)
    menu.add_command(label="Restart", command=restart)
    menu.add_separator()
    menu.add_command(label="Exit", command=exit)
    window.config(menu=menubar)



def main(size):
    global maze_size
    global maze_cell_table
    global current_cell
    global stack
    global wall_size
    global maze_path
    global maze_table
    global start
    global end
    global goal
    global player
    global canvas
    global is_goal

    is_goal = False
    maze_size = size
    maze_cell_table = [[Cell(x, y) for x in range(maze_size)] for y in range(maze_size)]
    current_cell = maze_cell_table[0][0]
    stack = []
    wall_size = 300/maze_size

    make_maze_result = True
    while make_maze_result:
        make_maze_result = make_maze()

    maze_table = draw_maze(maze_cell_table)

    maze_table_length = len(maze_table)
    start = (1, 1)
    end = (maze_table_length-2, maze_table_length-2)
    maze_path = search_path(start, end, maze_table)

    for x, y in maze_path:
        maze_table[x][y] = '*'

    canvas = Canvas(window, width=800, height=660, bg="#FFF8E5")
    canvas.pack()
    make_game_menu()
    for y in range(maze_table_length):
        for x in range(maze_table_length):
            if maze_table[y][x] == '1':
                canvas.create_rectangle(x*wall_size, y*wall_size, (x+1)*wall_size, (y+1)*wall_size, fill="#C6D57E", outline="white")
                
    goal_location = wall_size * (maze_size * 2 - 0.5)
    goal_img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\goal.png').subsample(maze_size*2)
    goal = canvas.create_image(goal_location, goal_location, image=goal_img)

    player_location = wall_size * 1.5
    player_img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\character.png').subsample(maze_size*2)
    player = canvas.create_image(player_location, player_location, image=player_img)

    window.mainloop()



maze_size = 5
maze_cell_table = []
current_cell = []
stack = []
wall_size = 0
maze_path = []
maze_table = []
start = ()
end = ()
goal = 0
player = 0
is_goal = False

canvas = tkinter.Canvas(window)

main(maze_size)