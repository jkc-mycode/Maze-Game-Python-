import tkinter

# 키 이름을 입력할 변수 선언
key = 0
# 키를 눌렀을 때 실행할 함수 정의
def key_down(e):
    global key # key을 전역 변수로 취급
    key = e.keysym # 눌려진 키 이름을 key에 대입

# 키를 눌렀다 뗐을 때 실행할 함수 정의
def key_up(e):
    global key # key을 전역 변수로 취급
    key = "" # key에 빈 문자열 대입

mx = 1 # 캐릭터의 가로 뱡향 위치를 관리하는 변수
my = 1 # 캐릭터의 세로 뱡향 위치를 관리하는 변수

# 실시간 처리를 수행할 함수 정의
def main_proc():
    global mx, my # mx, my를 전역 변수로 선언
    # key 방향이 통로라면 그 방향에 맞게 mx, my값을 변경
    if key == "Up" and maze[my-1][mx] == 0: 
        my -= 1
    if key == "Down" and maze[my+1][mx] == 0:
        my += 1
    if key == "Left" and maze[my][mx-1] == 0:
        mx -= 1
    if key == "Right" and maze[my][mx+1] == 0:
        mx += 1
    canvas.coords("MYCHR", mx*80 + 40, my*80 + 40) # 캐릭터 이미지 이동
    root.after(200, main_proc) # 0.2초 후 main_proc 함수 지정


root = tkinter.Tk()
root.title("미로 안 이동하기")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x * 80, y * 80, x * 80 + 79, y * 80 + 79, fill="skyblue", width=0)

img = tkinter.PhotoImage(file="Maze_Game_BackTracking\img\character.png")
canvas.create_image(mx * 80 + 40, my * 80 + 40, image=img, tag="MYCHR")
main_proc()
root.mainloop()

