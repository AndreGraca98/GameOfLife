import os
import cv2
import numpy as np
import tkinter as tk
from numba import jit, njit


    
@njit
def count_neighbors(grid, i, j):
    """
    Params:
    -------
        grid (np.array): old grid
        i (int) : width value for cell 
        j (int) : height value for cell 
    Returns:
        neighbors_state_sum(int) : neighbors sum
    """
    neighbors_state_sum = 0
    for x in range(-1,2):
        for y in range(-1,2):
            if i+x >= 0 and i+x < width and j+y >= 0 and j+y < height:
                neighbors_state_sum += grid[j+y][i+x]
    
    return neighbors_state_sum - grid[j][i]

# @njit
def update_grid(old_grid):
    """
    Params:
        old_grid (np.array): old grid
    Returns:
        next_grid (np.array): new updated grid
    """

    next_grid = np.zeros([height, width])
    for i in range(width):
        for j in range(height):
            
            cell_state = old_grid[j][i]
            
            neighbors_state_sum = count_neighbors(old_grid, i, j)

            if cell_state == 1 and neighbors_state_sum < 2:
                new_cell_state = 0
            elif cell_state == 1 and neighbors_state_sum > 3:
                new_cell_state = 0
            elif cell_state == 0 and neighbors_state_sum == 3:
                new_cell_state = 1
            else:
                new_cell_state = cell_state
            
            next_grid[j][i] = new_cell_state

    return next_grid


def freeze(*args):
    global freeze_flag
    if freeze_flag:
        freeze_flag = False
        print('Not Freezed')
    else:
        freeze_flag = True
        print('Freezed')

def mouse_click(event, x, y, *args):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN and freeze_flag:
        mouseX,mouseY = x,y
        print(mouseX, mouseY)


if __name__ == '__main__':
    global height, width, res
    global freeze_flag
    global mouseX, mouseY
    mouseX = None
    mouseY = None
    freeze_flag = False
    full_screen_flag = False

    res = 10  # resolution

    screen = tk.Tk()
    if full_screen_flag:
        height = screen.winfo_screenheight()//res
        width = screen.winfo_screenwidth()//res
    else:
        height = 480//res
        width = 640//res

    smaller_grid = np.zeros([height, width])
    old_grid = smaller_grid
    

    # smaller_grid[height//2][width//2 + -1] = 1
    # smaller_grid[height//2][width//2 + 0] = 1
    # smaller_grid[height//2][width//2 + 1] = 1

    # smaller_grid[height//2][width//2 + -1] = 1
    # smaller_grid[height//2][width//2 + 0] = 1
    # smaller_grid[height//2][width//2 + 1] = 1
    # smaller_grid[height//2 - 1][width//2 + -1] = 1
    # smaller_grid[height//2 -2 ][width//2 + 0] = 1

    cv2.namedWindow("Game of Life")

    if not full_screen_flag:
        cv2.moveWindow("Game of Life",screen.winfo_screenwidth()//2-width*res//2,screen.winfo_screenheight()//2-height*res//2)

    cv2.createButton("Freeze",freeze,None,cv2.QT_PUSH_BUTTON,1)
    cv2.setMouseCallback('Game of Life',mouse_click)

    while 1:
        show_grid = cv2.resize(smaller_grid, (width*res, height*res), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Game of Life', show_grid)



        if not freeze_flag:
            smaller_grid = update_grid(smaller_grid)
        else:
            if mouseY and mouseX:
                smaller_grid[mouseY//res][mouseX//res] = 1
                mouseX = None
                mouseY = None
                

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        if not np.count_nonzero(smaller_grid):
            print('New grid is empty!')
            # break


