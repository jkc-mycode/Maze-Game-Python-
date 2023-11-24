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



class MazeGame:
    def __init__(self, maze_size=5):
        self.maze_size = maze_size
        self.maze_cell_table = [[Cell(x, y) for x in range(maze_size)] for y in range(maze_size)]
        self.current_cell = self.maze_cell_table[0][0]
        self.stack = []
        self.wall_size = 300/maze_size
        self.maze_path = []
        self.maze_table = []
        self.start = ()
        self.end = ()
        self.goal = 0
        self.player = 0
        self.is_goal = False
        self.canvas = None


    def make_maze(self):
        self.current_cell.visited = True
        children = self.current_cell.get_children(self.maze_cell_table)

        if children:
            choice_cell = random.choice(children)
            choice_cell.visited = True

            self.stack.append(self.current_cell)

            self.remove_walls(self.current_cell, choice_cell)
            self.current_cell = choice_cell
            return True
        elif self.stack:
            self.current_cell = self.stack.pop()
            return True
        else:
            return False


    def remove_walls(self, current_cell: Cell, choice_cell: Cell):
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


    def draw_walls(self, maze_table: list, temp_table: list) -> list:
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


    def draw_table_outline(self, temp_table: list) -> list:
        length = len(temp_table)
        for row in temp_table:
            row[0] = row[length-1] = '1'
        temp_table[0] = temp_table[length-1] = ['1'] * length
        return temp_table


    def draw_maze(self, maze_cell_table: list) -> list:
        temp_table = []
        table_length = len(maze_cell_table) * 2 + 1

        for x in range(table_length):
            if x % 2 == 0:
                temp_table.append(['0' if x % 2 != 0 else '1' for x in range(table_length)])
            else:
                temp_table.append(['0'] * table_length)
        
        temp_table = self.draw_walls(maze_cell_table, temp_table)
        temp_table = self.draw_table_outline(temp_table)
        return temp_table


    def search_path(self, start: tuple, end: tuple, maze: list) -> list:
        location_point = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        prev_location = [[None] * len(maze[0]) for _ in range(len(maze))]
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


    def play_computer(self, player, start, maze_path):
        current = list(map(int, start))
        for x, y in maze_path:
            if self.is_goal: 
                return
            current[0] = y - current[0]
            current[1] = x - current[1]
            self.canvas.move(player, current[0]*self.wall_size, current[1]*self.wall_size)
            current[0] = y
            current[1] = x
            time.sleep(0.1)
            self.canvas.update()

            if current == list(self.end):
                self.is_goal = True
                img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\goal_popup.png')
                label = Label(window, image=img)
                label.image = img
                label.place(x=60, y=60)


    def play_user(self, event):
        directions = {'Left': (0, -1), 'Right': (0, 1), 'Up': (-1, 0), 'Down': (1, 0)}
        direction = directions.get(event.keysym)
        if direction is None:
            return

        self.start = list(self.start)
        nx, ny = self.start[0] + direction[0], self.start[1] + direction[1]
        if not (1 <= nx < len(self.maze_table) and 1 <= ny < len(self.maze_table[0])) or self.maze_table[nx][ny] == '1':
            return

        self.canvas.move(self.player, direction[1]*self.wall_size, direction[0]*self.wall_size)
        self.start[0], self.start[1] = nx, ny
        self.start = tuple(self.start)

        if self.start == self.end:
            self.is_goal = True
            img = tkinter.PhotoImage(file='Maze_Game_BackTracking\img\goal_popup.png')
            label = Label(window, image=img)
            label.image = img
            label.place(x=60, y=60)


    def select_mode(self, mode: int):
        if mode == 1:
            self.play_computer(self.player, self.start, self.maze_path)
        else:
            self.canvas.bind_all("<KeyPress>", self.play_user)


    def select_stage(self, size: int):
        self.canvas.destroy()
        self.__init__(size) # 게임을 초기화하고 선택한 스테이지 사이즈로 게임을 다시 실행합니다.
        self.main()


    def restart(self):
        window.destroy()
        os.system('python3 Maze_Game_BackTracking\\maze_game.py')


    def exit(self):
        window.quit()
       

    def make_game_menu(self):
        menubar = tkinter.Menu(window)
        menu_mode = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mode", menu=menu_mode)
        menu_mode.add_command(label="Auto", command=lambda: self.select_mode(1))
        menu_mode.add_command(label="User", command=lambda: self.select_mode(2))

        menu_stage = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Stage", menu=menu_stage)
        for i in range(5, 31, 5):
            menu_stage.add_command(label=str(i), command=lambda i=i: self.select_stage(i))

        menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=menu)
        menu.add_command(label="Restart", command=self.restart)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.exit)
        window.config(menu=menubar)


    def main(self):
        while self.make_maze():
            continue

        self.maze_table = self.draw_maze(self.maze_cell_table)
        self.start = (1, 1)
        self.end = (len(self.maze_table) - 2, len(self.maze_table) - 2)
        self.maze_path = self.search_path(self.start, self.end, self.maze_table)

        self.canvas = Canvas(window, width=800, height=660, bg="#FFF8E5")
        self.canvas.pack()
        self.make_game_menu()

        for y_index, y_value in enumerate(self.maze_table):
            for x_index, x_value in enumerate(y_value):
                if x_value == '1':
                    self.canvas.create_rectangle(x_index*self.wall_size, y_index*self.wall_size,
                                                 x_index*self.wall_size+self.wall_size, y_index*self.wall_size+self.wall_size, fill='#C6D57E', outline='white')

        self.goal = self.canvas.create_rectangle(self.end[1]*self.wall_size, self.end[0]*self.wall_size,
                                                 self.end[1]*self.wall_size+self.wall_size, self.end[0]*self.wall_size+self.wall_size, fill='#FFAB40', outline='#FFAB40')
        self.player = self.canvas.create_rectangle(self.start[1]*self.wall_size, self.start[0]*self.wall_size,
                                                   self.start[1]*self.wall_size+self.wall_size, self.start[0]*self.wall_size+self.wall_size, fill='#FF4081', outline='#FF4081')
        window.mainloop()


game = MazeGame()
game.main()