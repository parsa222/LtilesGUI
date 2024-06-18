import tkinter as tk
from tkinter import messagebox
import random
import time

# TODO: fix line allignments - fix n < 8
# ver2.0:  number the groups in the gui 



#init global vars
size_of_grid = 0 # 2^0 * 2^0 = 1
#b = 0
#a = 0
Lcnt = 0
# 2D array 
arr = []

for j in range(128): # 2^7 (max tiles for now change later)
    row = []
    for i in range(128):
        row.append(0)
    arr.append(row)
        



#for refrences
size = 0
click_enabled = True
start_button = None
canvas = None
cell_size = 0
colors = {}


def main():
    """
    window to take N
    right now the grid is initialized to 128 * 128 (2^8)
    if you want n to be more than 8, change the Arr list size in the top of the code....
    (trust me you dont really need a grid more than 128 * 128)

    """
    global input_window, entry

    input_window = tk.Tk()
    input_window.title("2^n * 2^n")
    input_frame = tk.Frame(input_window)
    input_frame.pack(pady=10)
    label = tk.Label(input_frame, text="Enter N:")
    label.pack(side=tk.LEFT, padx=5)
    entry = tk.Entry(input_frame)
    entry.pack(side=tk.LEFT, padx=5)

    #button
    button = tk.Button(input_frame, text="Make grid", command=button_func)
    button.pack(side=tk.LEFT, padx=5)

    input_window.mainloop()



def button_func():
    """
    checks if values are okay and calls other functions
    """
    try:
        n = int(entry.get())
        if n < 0:
            raise ValueError("REALLY? A NEGATIVE NUMBER?")
        elif n== 0 :
            raise ValueError("0 L tiles")

        
        input_window.destroy() # closing it because there is no need for it to be there anymore
        open_grid_window(n)
    except ValueError as e:
        messagebox.showerror("something is wrong", str(e))


def open_grid_window(n):
    """
    grid window
    calls the grid generator and tiling func
    
    """
    global canvas, start_button , size
    size = 2 ** n
    
    grid_window = tk.Tk()
    grid_window.title(f"Generated {size} by {size} Grid")
    
    canvas = tk.Canvas(grid_window, width=canvas_size, height=canvas_size, bg="white")
    canvas.pack(pady=10)
    
    generate_grid(n, canvas)
    
    messagebox.showinfo("steps", "1- click on a tile to remove \n\n2- then press start")

    button_frame = tk.Frame(grid_window)
    button_frame.pack(pady=10)
    start_button = tk.Button(button_frame, text="start", command=lambda: start_tiling(canvas, start_button))# avoided wrapper functions for better maintainability.

    # hiding the button
    start_button.pack_forget()  

    grid_window.mainloop()



def generate_grid(n, canvas):
    """
    makes the grid using n input and the size that open_grid_window provided
    
    """
    global grid_size, cell_size, click_enabled
    grid_size = 2 ** n
    cell_size = canvas_size // grid_size # the size of each small block
    click_enabled = True 
    

    for row in range(grid_size):
        for col in range(grid_size):
            # cooridates of each block
            x1 = col * cell_size # top-left
            y1 = row * cell_size # top-left
            x2 = x1 + cell_size # bottom-right
            y2 = y1 + cell_size # bottom-right
            rect = canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", tags="rect")

            # making them clickable
            # https://stackoverflow.com/questions/29211794/how-to-bind-a-click-event-to-a-canvas-in-tkinter 
            canvas.tag_bind(rect, "<Button-1>", lambda event, row=row, col=col: remove_tile(event, canvas, row, col)) 
            # the reason i used lambda is because i would be able to pass arguements to remove_tile() func. 



def remove_tile(event, canvas, row, col):
    """
    removing the selected tile and disabling clickability
    fills the selected tile black and sets its value to -1 in the array
    
    """
    global click_enabled, start_button, removed_tile
    if click_enabled:


        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size


        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="removed")
        click_enabled = False  # No more clicks
        removed_tile = (row, col)
        
        arr[row][col] = -1  
        print(f"removed tile ({row},{col})")
        start_button.pack(pady=10)  # +1







def start_tiling(canvas, start_button):
    """
    hides the start button and starts the tiling func
    """
    global size
    global grid_size
    start_button.pack_forget()  
    tile(grid_size, 0, 0)

    global arr

    for i in arr:
        for j in i:
            if j !=0:
                # formatted string to align the numbers
                # https://www.geeksforgeeks.org/string-alignment-in-python-f-string/
                print(f"{j:<3}", end=" ")
        if i[0] != 0:
            print()  


    messagebox.showinfo("complete", f"total L tiles = {int((size *size-1)/3)}")



def mid_line(x, y, size):
    """
    finds the midline of each subgrid to color 
    """
    mid_x = x + size // 2
    mid_y = y + size // 2


    color = "red"

    canvas.create_line(mid_y * cell_size, y * cell_size, mid_y * cell_size, (y + size) * cell_size, fill=color)
    canvas.create_line(x * cell_size, mid_x * cell_size, (x + size) * cell_size, mid_x * cell_size, fill=color)

    canvas.update()


    time.sleep(0.1)


 # main func
def tile(n, x, y):
    """
    the core logic 
    https://www.geeksforgeeks.org/tiling-problem-using-divide-and-conquer-algorithm/


    n is size of given square, p is location of missing cell
Tile(int n, Point p)

1) Base case: n = 2, A 2 x 2 square with one cell missing is nothing 
   but a tile and can be filled with a single tile.

2) Place a L shaped tile at the center such that it does not cover
   the n/2 * n/2 subsquare that has a missing square. Now all four 
   subsquares of size n/2 x n/2 have a missing cell (a cell that doesn't
   need to be filled).  See figure 2 below.

3) Solve the problem recursively for following four. Let p1, p2, p3 and
   p4 be positions of the 4 missing cells in 4 squares.
   a) Tile(n/2, p1)
   b) Tile(n/2, p2)
   c) Tile(n/2, p3)
   d) Tile(n/2, p3)
    """
    global Lcnt
    if n == 2:
        Lcnt += 1
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        while color == "#000000" or color == "#FFFFFF":
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        colors[Lcnt] = color
        for i in range(n):
            for j in range(n):
                if arr[x + i][y + j] == 0:
                    arr[x + i][y + j] = Lcnt
                    canvas_x1 = (y + j) * cell_size
                    canvas_y1 = (x + i) * cell_size
                    canvas_x2 = canvas_x1 + cell_size
                    canvas_y2 = canvas_y1 + cell_size
                    canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="black", fill=color)
                    print(f"tile at ({x + i}, {y + j}) added to group {Lcnt}")
        canvas.update()
        time.sleep(0.1)
        return
    mid_line(x, y, n)
    r, c = 0, 0
    for i in range(x, x + n):
        for j in range(y, y + n):
            if arr[i][j] != 0:
                r, c = i, j
                break

        # recursively breaks it into sub grids
    if r < x + n // 2 and c < y + n // 2: # top-Left sub grid
        place_and_color(x + n // 2, y + n // 2 - 1, x + n // 2, y + n // 2, x + n // 2 - 1, y + n // 2)
    elif r >= x + n // 2 and c < y + n // 2: # bottom-Left
        place_and_color(x + n // 2 - 1, y + n // 2, x + n // 2, y + n // 2, x + n // 2 - 1, y + n // 2 - 1)
    elif r < x + n // 2 and c >= y + n // 2: #top-Right
        place_and_color(x + n // 2, y + n // 2 - 1, x + n // 2, y + n // 2, x + n // 2 - 1, y + n // 2 - 1)
    else:  # bottom-Right
        place_and_color(x + n // 2 - 1, y + n // 2, x + n // 2, y + n // 2 - 1, x + n // 2 - 1, y + n // 2 - 1)
    tile(n // 2, x, y + n // 2)
    tile(n // 2, x, y)
    tile(n // 2, x + n // 2, y)
    tile(n // 2, x + n // 2, y + n // 2)
    #print(arr)




def place_and_color(x1, y1, x2, y2, x3, y3):
    """
    colors the tiles by their groups
    """
    global Lcnt
    Lcnt += 1
    tile_num = Lcnt
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    # all colors but white and black
    while color == "#000000" or color == "#FFFFFF":
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    colors[tile_num] = color
    arr[x1][y1] = tile_num
    arr[x2][y2] = tile_num
    arr[x3][y3] = tile_num
    for (x, y) in [(x1, y1), (x2, y2), (x3, y3)]:
        canvas_x1 = y * cell_size
        canvas_y1 = x * cell_size
        canvas_x2 = canvas_x1 + cell_size
        canvas_y2 = canvas_y1 + cell_size
        canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="black", fill=color)
    canvas.update()
    time.sleep(0.1)

# starts everything
canvas_size = 500
grid_size = 0
cell_size = 0
#c = 0 
removed_tile = None # initialzied

main()





#  https://www.geeksforgeeks.org/tiling-problem-using-divide-and-conquer-algorithm/
# size_of_grid = 0
# b = 0
# a = 0
# cnt = 0
# arr = [[0 for i in range(128)] for j in range(128)]

# def place(x1, y1, x2, y2, x3, y3):
# 	global cnt
# 	cnt += 1
# 	arr[x1][y1] = cnt;
# 	arr[x2][y2] = cnt;
# 	arr[x3][y3] = cnt;
	
# def tile(n, x, y):
# 	global cnt
# 	r = 0
# 	c = 0
# 	if (n == 2):
# 		cnt += 1
# 		for i in range(n):
# 			for j in range(n):
# 				if(arr[x + i][y + j] == 0):
# 					arr[x + i][y + j] = cnt
# 		return 0; 
# 	for i in range(x, x + n):
# 		for j in range(y, y + n):
# 			if (arr[i][j] != 0):
# 				r = i
# 				c = j 
# 	if (r < x + n / 2 and c < y + n / 2):
# 		place(x + int(n / 2), y + int(n / 2) - 1, x + int(n / 2), y + int(n / 2), x + int(n / 2) - 1, y + int(n / 2))
	
# 	elif(r >= x + int(n / 2) and c < y + int(n / 2)):
# 		place(x + int(n / 2) - 1, y + int(n / 2), x + int(n / 2), y + int(n / 2), x + int(n / 2) - 1, y + int(n / 2) - 1)
	
# 	elif(r < x + int(n / 2) and c >= y + int(n / 2)):
# 		place(x + int(n / 2), y + int(n / 2) - 1, x + int(n / 2), y + int(n / 2), x + int(n / 2) - 1, y + int(n / 2) - 1)
	
# 	elif(r >= x + int(n / 2) and c >= y + int(n / 2)):
# 		place(x + int(n / 2) - 1, y + int(n / 2), x + int(n / 2), y + int(n / 2) - 1, x + int(n / 2) - 1, y + int(n / 2) - 1)
	
# 	tile(int(n / 2), x, y + int(n / 2));
# 	tile(int(n / 2), x, y);
# 	tile(int(n / 2), x + int(n / 2), y);
# 	tile(int(n / 2), x + int(n / 2), y + int(n / 2)); 
	
# 	return 0

# size_of_grid = 8
# a = 0
# b = 0
# arr[a][b] = -1
# tile(size_of_grid, 0, 0)

# for i in range(size_of_grid):
# 	for j in range(size_of_grid):
# 		print(arr[i][j], end=" ")
# 	print()



