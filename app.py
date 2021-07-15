import sys
from heapq import heapify, heappush, heappop
from tkinter import *
import time
import threading
# try removing heapify once done

board_size = 60
block_size = 16
animate = True
background_color = "#fbbb8a"

class Point:
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.visited = 0
        self.prev = None
        self.cost = cost
        self.totalCostFromStart = sys.maxsize
        self.numPointsFromStart = sys.maxsize
        self.available = 1

    def set_prev(self, prev):
        self.prev = prev

    def get_adjacent_points(self):
        adjacent = []
        if(self.row > 0):
            adjacent.append()

    def resetPoint(self):
        self.totalCostFromStart = sys.maxsize
        self.numPointsFromStart = sys.maxsize
        self.prev = None
        self.visited = 0
    


    # sets the distance as the comparing variable
    def __lt__(self, other):
        return self.totalCostFromStart < other.totalCostFromStart


#inplemented using a min heap through heapq
class PriorityQueue:

    def __init__(self):
        self.queue = []
    
    # add a point to the queue
    def enqueue(self, point):
        heappush(self.queue, point)
    
    # remove the point with the smallest distance
    def dequeue(self):
        return heappop(self.queue)

    # check if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # return the point with the smallest distance
    def getMin(self):
        return self.queue[0]



class Grid:

    def __init__(self, window):
        self.startB = None
        self.endB = None
        self.canvas = Canvas(window, highlightbackground="black",highlightthickness=1, height = 960, width = 960)
        self.grid = [[Point(i, j, 1) for j in range(board_size)] for i in range(board_size)]
        self.draw_grid()

        # create a listener to track mouse 1 movement
        self.canvas.bind('<B1-Motion>', self.draw_wall)

    # draw the walls in the grid
    def draw_wall(self, event):
        corner_cords = self.get_block_corner_cord(event.x, event.y)
        block = self.grid[corner_cords[0]][corner_cords[1]]
        if(block == self.startB):
            return
        row = corner_cords[0]
        col = corner_cords[1]
        block.available = 0
        self.canvas.create_rectangle(row * block_size, col * block_size, (row + 1) * block_size, (col + 1) * block_size, fill = "black")

    # get the coordinates of the top left corner of the block (x,y) resides in
    def get_block_corner_cord(self, x, y):
        return (int(x / block_size), int(y / block_size))
        

    # draws all the rectangles and sets them to white
    def draw_grid(self):
        for i in range(board_size):
            for j in range(board_size):
                self.canvas.create_rectangle(i * block_size, j * block_size, (i + 1) * block_size, (j + 1) * block_size, fill = "white")
            

    
    # set the starting point
    def set_start(self, row, col):
        self.startB = self.grid[row][col]
        # color in the start rectangle
        self.canvas.create_rectangle(row * block_size, col * block_size, (row + 1) * block_size, (col + 1) * block_size, fill = "red")

    # set the ending point
    def set_end(self, row, col):
        self.endB = self.grid[row][col]
        # color in the end rectangle
        self.canvas.create_rectangle(row * block_size, col * block_size, (row + 1) * block_size, (col + 1) * block_size, fill = "purple")

    # reset the values of the points and colors of the board
    def reset(self, keep_walls):
        grid = self.grid
        for row in grid:
            for point in row:
                point.resetPoint()
                if((point != self.startB and point != self.endB)):
                    if(not keep_walls or (keep_walls and point.available == 1)):
                        self.canvas.create_rectangle(point.row * block_size, point.col * block_size, (point.row + 1) * block_size, (point.col + 1) * block_size, fill = "white")
                        point.available = 1


    # returns a list of all the points adjacent to the given point
    # only returns the points directly above, right, below, and left in that order 
    def get_adjacent_points(self, point):
        adjacent = []
        # get the above point
        if(point.row > 0):
            adjacent.append(self.grid[point.row - 1][point.col])
        # get the right point
        if(point.col < board_size - 1):
            adjacent.append(self.grid[point.row][point.col + 1])    
        # get the bottom point
        if(point.row < board_size - 1):
            adjacent.append(self.grid[point.row + 1][point.col])
        # get the left point
        if(point.col > 0):
            adjacent.append(self.grid[point.row][point.col - 1])
        return adjacent

    # run dijkstra's algorithm
    def run_dijkstras(self):
        # check if startB and endB are initialized

        if(self.startB == None or self.endB == None):
            return
        
        self.reset(True)
        start = self.startB
        pQueue = PriorityQueue()
        start.totalCostFromStart = 0
        start.numPointsFromStart = 0
        pQueue.enqueue(start)
        
        while(not pQueue.isEmpty()):
            current = pQueue.dequeue()
            row = current.row
            col = current.col
            if(current.visited == 0):
                
                current.visited = 1
                current_cost = current.totalCostFromStart
                adjacent_pts = self.get_adjacent_points(current) 
                for next_point in adjacent_pts:
                    if(current_cost + next_point.cost < next_point.totalCostFromStart and next_point.available == 1):
                        next_point.totalCostFromStart = current_cost + next_point.cost
                        next_point.prev = current
                        next_point.numPointsFromStart = current.numPointsFromStart + 1
                        if(next_point == self.endB):
                            root.after(10, paint_rectangle(row, col, self.canvas, "blue"))
                            root.update()
                            self.draw_shortest_path()
                            root.after(1000, self.show_end_window(True))
                            return
                        pQueue.enqueue(next_point)
                    
                if(animate and current != start):
                    root.after(1, paint_rectangle(row, col, self.canvas, "blue"))
                    root.update()

        root.after(500,self.show_end_window(False))
    
    # opens a new window showing the final result
    def show_end_window(self, success):
        end_window = Toplevel(self.canvas)
        end_window.title("Result")
        end_window.geometry("500x500")
        end_window.config(bg = "green")
        
        result_label = Label(end_window, text = "The shortest path between the two points is " + str(self.endB.numPointsFromStart) + " blocks away")
        result_label.config(bg = "green")
        if(not success):
            result_label.config(text = "No path could be found between the two points")
        
        result_label.pack(pady=100)
        result_label.pack(padx=50)



    # reset the colors but keep the starting and end points the same
    def reset_color(self):
        for row in board_size:
            for col in board_size:
                self.canvas.create_rectangle(row * block_size, col * block_size, (row + 1) * block_size, (col + 1) * block_size, fill = "white")
                self.grid[row][col].visited = 0
    # once the end point is found, draw the path
    def draw_shortest_path(self):
        current = self.endB.prev
        while(current != self.startB):
            root.after(10, paint_rectangle(current.row, current.col, self.canvas, "orange"))
            root.update()
            current = current.prev
                        

    

def paint_rectangle(row, col, canvas, color):
    canvas.create_rectangle(row * block_size, col * block_size, (row + 1) * block_size, (col + 1) * block_size, fill = color)
# set start and end points
def set_start_end():
    board.reset(False)
    if(board.startB != None and board.endB != None):
        board.canvas.create_rectangle(board.startB.row * block_size, board.startB.col * block_size, (board.startB.row + 1) * block_size, (board.startB.col + 1) * block_size, fill = "white")
        board.canvas.create_rectangle(board.endB.row * block_size, board.endB.col * block_size, (board.endB.row + 1) * block_size, (board.endB.col + 1) * block_size, fill = "white")
    # parse the entry strings
    start_pt = startPt_entry.get()[1 : -1].split(",")
    end_pt = endPt_entry.get()[1 : -1].split(",")
    try :
        start_x = int(start_pt[0])
        start_y = int(start_pt[1])
        end_x = int(end_pt[0])
        end_y = int(end_pt[1])
    except ValueError:
        # if the entered string is wrong, don't do anything
        return
    # make sure the start and end points are different
    if(start_x == end_x and start_y == end_y):
        return
    board.set_start(start_x, start_y)
    board.set_end(end_x, end_y)



# runs the desired algorithm
def run_algorithm():
    board.run_dijkstras()

# reset the board
def reset_board():
    board.reset(False)

root = Tk()
root.title("Shortest Path Algorithm Animation")
root.geometry("1200x1200")
root.config(background = background_color)

board = Grid(root)

#event = threading.Event()

frame = Frame(root, height = 300, width = 1200) # holds all the widgets above the grid
frame.config(bg = background_color)
frame.pack()

# entry for the starting point
startPt_label = Label(frame, text = "Enter the starting point (x,y)", bg = background_color)
startPt_label.grid(row = 0, column = 0)
startPt_entry = Entry(frame, bd = 0.5)
startPt_entry.grid(row = 0, column = 1)

# entry for the ending point
endPt_label = Label(frame, text = "Enter the ending point (x,y)", bg = background_color)
endPt_label.grid(row = 1, column = 0)
endPt_entry = Entry(frame, bd = 0.5)
endPt_entry.grid(row = 1, column = 1)

# button to apply the start and ending points
set_pts_btn = Button(frame, text = "Set Points", command = set_start_end, highlightthickness=1, pady = 5)
set_pts_btn.grid(row = 2, column = 0, pady= 5)

# button to run disjkstra's
run_btn = Button(frame, text = "Run Dijkstra's", command = run_algorithm, highlightthickness=1, pady = 5)
run_btn.grid(row = 2, column = 1, pady= 5)

# button to reset the board
reset_btn = Button(frame, text = "Reset Board", command = reset_board, highlightthickness = 1, pady = 5)
reset_btn.grid(row = 2, column = 3, pady = 5)



board.canvas.pack()


root.mainloop()


