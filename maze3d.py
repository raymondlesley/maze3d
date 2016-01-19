'''
Created on 28 Feb 2014

Update 25Apr14:
Correct demo cell setup
Implement right_arrow handler
Check for walls on up_arrow

Update 12Jun14:
implement Maze class
add down_arrow handling
introduce Direction class

Update 13Jun14:
implement DFS maze generation algorithm

Update 19Jun14:
add map view

@author: Raymond Lesley
'''

class Rect():
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
    def tl(self):
        return (self._x1, self._y1)
    def tr(self):
        return (self._x2, self._y1)
    def bl(self):
        return (self._x1, self._y2)
    def br(self):
        return (self._x2, self._y2)

    def width(self):
        return self._x2 - self._x1

    def height(self):
        return self._y2 - self._y1

    def shrink(self, x_amount, y_amount):
        self._x1 = self._x1 + x_amount
        self._x2 = self._x2 - x_amount
        self._y1 = self._y1 + y_amount
        self._y2 = self._y2 - y_amount


class Direction():
    '''
    constants
    arranged in a circle
    '''
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    NUM_DIRECTIONS = 4

    def __init__(self, facing):
        self.__facing= facing

    def facing(self, direction):
        return self.__facing == direction

    def left_turn(self):
        return Direction((self.__facing - 1) % self.NUM_DIRECTIONS)
    def right_turn(self):
        return Direction((self.__facing + 1) % self.NUM_DIRECTIONS)
    def about_turn(self):
        return Direction((self.__facing + 2) % self.NUM_DIRECTIONS)


class Colour():
    def __init__(self, r, g, b ):
        self._r = r
        self._g = g
        self._b = b

    def red(self):
        return self._r
    def green(self):
        return self._g
    def blue(self):
        return self._b

    def brighten(self, factor):
        # TODO: what about black?
        self._r = self._r * factor
        if self._r > 255:
            self._r = 255
        
class Cell():
    '''
    constants
    '''
    WALL = None

    '''
    data
    '''
    _x = _y = 0
    n = s = e = w = WALL
    colour = Colour(0, 0, 0)

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.colour = Colour(255, 0, 0) # default = red

    def closed(self):
        return self.n == self.s == self.e == self.w == self.WALL
    
    def draw_cell(self, rect, canvas, direction):
        #edge of screen
        old_tl = rect.tl()
        old_tr = rect.tr()
        old_bl = rect.bl()
        old_br = rect.br()
        
        # wall scale
        x_step = rect.width() / 4 # (rect[2] - rect[0]) / 4 # width/10
        y_step = rect.height() / 4 # (rect[5] - rect[1]) / 4 # height/10
        
        #  edge points: current cell
        rect.shrink(x_step, y_step)
        tl = rect.tl()
        tr = rect.tr()
        bl = rect.bl()
        br = rect.br()
        
        # assume facing North
        if direction.facing(Direction.NORTH):
            left = self.w
            right = self.e
            front = self.n
        elif direction.facing(Direction.WEST):
            left = self.s
            right = self.n
            front = self.w
        elif direction.facing(Direction.EAST):
            left = self.n
            right = self.s
            front = self.e
        else: # direction.facing(Direction.SOUTH):
            left = self.e
            right = self.w
            front = self.s

        # Left wall
        if (left == Cell.WALL):
            # diagonal
            # canvas.create_line(old_tl[0], old_tl[1], tl[0], tl[1], bl[0], bl[1], old_bl[0], old_bl[1])
            canvas.create_polygon(old_tl[0], old_tl[1], tl[0], tl[1], bl[0], bl[1], old_bl[0], old_bl[1], fill="#F00")
        else:
            # horizonal
            # canvas.create_line(old_tl[0], tl[1], tl[0], tl[1], bl[0], bl[1], old_bl[0], bl[1])
            canvas.create_polygon(old_tl[0], tl[1], tl[0], tl[1], bl[0], bl[1], old_bl[0], bl[1], fill="#F77")
        # Right wall
        if (right == Cell.WALL):
            # diagonal
            # canvas.create_line(old_tr[0], old_tr[1], tr[0], tr[1], br[0], br[1], old_br[0], old_br[1])
            canvas.create_polygon(old_tr[0], old_tr[1], tr[0], tr[1], br[0], br[1], old_br[0], old_br[1], fill="#F00")
        else:
            # horizonal
            # canvas.create_line(old_tr[0], tr[1], tr[0], tr[1], br[0], br[1], old_br[0], br[1])
            canvas.create_polygon(old_tr[0], tr[1], tr[0], tr[1], br[0], br[1], old_br[0], br[1], fill="#F77")
        # Front wall
        if (front == Cell.WALL):
            # canvas.create_line(tl[0], tl[1], tr[0], tr[1], br[0], br[1], bl[0], bl[1], tl[0], tl[1])
            # canvas.create_line(tl[0], tl[1], tr[0], tr[1], br[0], br[1], bl[0], bl[1], tl[0], tl[1])
            canvas.create_polygon(tl[0], tl[1], tr[0], tr[1], br[0], br[1], bl[0], bl[1], tl[0], tl[1], fill="#F77")

    def next_cell(self, direction):
        if direction.facing(Direction.NORTH):
            return self.n
        elif direction.facing(Direction.WEST):
            return  self.w
        elif direction.facing(Direction.EAST):
            return  self.e
        else: # direction.facing(Direction.SOUTH):
            return self.s

'''
Maze - grid of Cells
'''
import random
class Maze():

    def __init__(self, width, height):
        self._width = width
        self._height = height
        # TODO: generate the maze!
        self._cells = [[Cell(x, y) for y in range(self._height)] for x in range(self._width)]
        print("Maze is", len(self._cells), "wide x", len(self._cells[0]))

    def generate_dummy_maze(self):
        '''
        dummy setup - for testing
        '''
        cell1 = Cell(1, 0)
        cell1.n = Cell(1, 1)
        cell1.w = Cell(0, 0)
        cell1.e = Cell.WALL
        cell1.s = Cell.WALL
        self._cells[1][0] = cell1
        
        cell2 = cell1.n
        cell2.n = Cell(1, 2)
        cell2.w = Cell.WALL
        cell2.e = Cell(2, 2)
        cell2.s = cell1
        self._cells[1][1] = cell2
        
        cell3 = cell2.n
        cell3.n = Cell(1, 3)
        cell3.w = Cell(0, 2)
        cell3.e = Cell.WALL
        cell3.s = cell2
        self._cells[1][2] = cell3
        
        cell4 = cell3.n
        cell4.n = Cell.WALL
        cell4.w = Cell.WALL
        cell4.s = cell3
        cell4.e = Cell.WALL
        self._cells[1][3] = cell4

        cell5 = cell1.w
        cell5.n = Cell.WALL
        cell5.w = Cell.WALL
        cell5.s = Cell.WALL
        cell5.e = cell1
        self._cells[0][0] = cell5

        cell6 = cell2.e
        cell6.n = Cell.WALL
        cell6.w = cell2
        cell6.s = Cell.WALL
        cell6.e = Cell.WALL
        self._cells[2][1] = cell6

        cell7 = cell3.w
        cell7.n = Cell.WALL
        cell7.w = Cell.WALL
        cell7.s = Cell.WALL
        cell7.e = cell3
        self._cells[0][2] = cell7
        
        self._starting_cell = cell1

    def generate_DFS(self):
        '''
        Depth-first algorithm from: http://mazeworks.com/mazegen/mazetut/index.htm
        create a CellStack (LIFO) to hold a list of cell locations 
        set TotalCells = number of cells in grid 
        choose a cell at random and call it CurrentCell 
        set VisitedCells = 1 
          
        while VisitedCells < TotalCells 
            find all neighbors of CurrentCell with all walls intact  
            if one or more found 
                choose one at random 
                knock down the wall between it and CurrentCell 
                push CurrentCell location on the CellStack 
                make the new cell CurrentCell 
                add 1 to VisitedCells
            else 
                pop the most recent cell entry off the CellStack 
                make it CurrentCell
            endIf 
        
        endWhile
        '''
        cell_stack = []
        total_cells = self._width * self._height
        x = 0
        y = 0
        visited_cells = 1
        
        while visited_cells < total_cells:
            print("exploring cell(", x, ",", y, ")")
            # find unvisited cells
            unvisited = []
            # left?
            north = self.north_cell(x, y)
            if (north != None) and (north.closed()):
                print("... found cell(", north._x, ",", north._y, ")")
                unvisited.append(north)
            east = self.east_cell(x, y)
            if (east != None) and (east.closed()):
                print("... found cell(", east._x, ",", east._y, ")")
                unvisited.append(east)
            south = self.south_cell(x, y)
            if (south != None) and (south.closed()):
                print("... found cell(", south._x, ",", south._y, ")")
                unvisited.append(south)
            west = self.west_cell(x, y)
            if (west != None) and (west.closed()):
                print("... found cell(", west._x, ",", west._y, ")")
                unvisited.append(west)
            
            num_unvisited = len(unvisited)
            if num_unvisited > 0:
                # more unvisited cells - choose one
                chosen = random.randint(0, num_unvisited-1)
                # join cells
                current_cell = self._cells[x][y]
                next_cell = unvisited[chosen]
                nx = next_cell._x
                ny = next_cell._y
                if (nx == x):
                    # n or s
                    if (ny > y):
                        #n
                        current_cell.n = next_cell
                        next_cell.s = current_cell
                    else: # (ny < y)
                        #s
                        current_cell.s = next_cell
                        next_cell.n = current_cell
                else: # (ny == y)
                    # w or e
                    if (nx > x):
                        # e
                        current_cell.e = next_cell
                        next_cell.w = current_cell
                    else: # (nx < x)
                        # w
                        current_cell.w = next_cell
                        next_cell.e = current_cell
                # push new cell onto stack
                cell_stack.append((nx, ny))
                # move to new cell
                x = nx
                y = ny
                # increase num visited cells
                visited_cells = visited_cells + 1
            else:
                (x, y) = cell_stack.pop()
        self._starting_cell = self._cells[0][0]

        
    def starting_cell(self):
        return self._starting_cell

    def north_cell(self, x, y):
        ny = y + 1
        if (ny >= self._height):
            return None
        else:
            return self._cells[x][ny]
    def east_cell(self, x, y):
        nx = x + 1
        if (nx >= self._width):
            return None
        else:
            return self._cells[nx][y]
    def south_cell(self, x, y):
        if (y > 0):
            return self._cells[x][y-1]
        else:
            return None
    def west_cell(self, x, y):
        if (x > 0):
            return self._cells[x-1][y]
        else:
            return None


'''
experimental
draw maze from current cell
'''
        
from tkinter import Tk, Canvas
# from time import sleep


class Maze3DGame():

    def __init__(self): 
        self.width = 400
        self.height = 300
        
        self.root = Tk()
        self.w = Canvas(self.root, width=self.width, height=self.height)
        self.w.pack()

        self.rows = 10
        self.columns = 10
        self._maze = Maze(self.columns, self.rows)
        # self._maze.generate_dummy_maze()
        self._maze.generate_DFS()

        self.current_cell = self._maze.starting_cell()
        self.current_direction = Direction(Direction.NORTH)
        self.showing_map = False
    
    def spin(self, event):
        print("key pressed:", event)
        self.draw_maze(self.current_cell, self.current_direction)
    
    def up_arrow(self, event):
        next_cell = self.current_cell.next_cell(self.current_direction)
        if next_cell == Cell.WALL:
            # can't walk through walls!
            self.root.bell()
        else:
            self.current_cell = next_cell
        self.draw()

    def down_arrow(self, event):
        backwards = self.current_direction.about_turn()
        next_cell = self.current_cell.next_cell(backwards)
        if next_cell == Cell.WALL:
            # can't walk through walls!
            self.root.bell()
        else:
            self.current_cell = next_cell
        self.draw()
        
    def left_arrow(self, event):
        self.current_direction = self.current_direction.left_turn()
        self.draw()

    def right_arrow(self, event):
        self.current_direction = self.current_direction.right_turn()
        self.draw()

    def m_key(self, event):
        if (self.showing_map):
            self.showing_map = False
        else:
            self.showing_map = True
        self.draw()

    def draw(self):
        if (self.showing_map):
            self.draw_map()
        else:
            self.draw_maze()
            

    def draw_maze(self):
        cell = self.current_cell
        direction = self.current_direction

        # "perspective" from corners to centre
        centre_x = self.width/2
        centre_y = self.height/2
        
        # wall scale
        x_step = self.width/2.5
        y_step = self.height/2.5
        
        # (beyond) edge of screen
        old_tl = (-x_step, -y_step)
        old_tr = (self.width+x_step, -y_step)
        old_bl = (-x_step, self.height+y_step)
        old_br = (self.width+x_step, self.height+y_step)
        rect = Rect(-x_step, -y_step, self.width+x_step, self.height+y_step)        
        
        sky = self.w.create_polygon(old_tl[0], old_tl[1], old_tr[0], old_tr[1], old_br[0], centre_y, old_bl[0], centre_y, fill="#ACF")
        grass = self.w.create_polygon(old_tl[0], centre_y, old_tr[0], centre_y, old_br[0], old_br[1], old_bl[0], old_bl[1], fill="#7F7")
        
        while cell != Cell.WALL:
            cell.draw_cell(rect, self.w, direction)
            cell = cell.next_cell(direction)

    def draw_map(self):
        cell_width = self.width / self.columns
        cell_height = self.height / self.rows

        # clear
        background = self.w.create_polygon(0, 0, 0, self.height, self.width, self.height, self.width, 0, fill="#FFF")
        
        # draw walls
        for row in range(self.rows):
            for col in range(self.columns):
                bl_x = col * cell_width + 1
                bl_y = self.height - row * cell_height + 1
                
                br_x = bl_x + cell_width
                br_y = bl_y
                tl_x = bl_x
                tl_y = bl_y - cell_height
                tr_x = bl_x + cell_width
                tr_y = bl_y - cell_height
                cell = self._maze._cells[col][row]

                if (cell.n == Cell.WALL):
                    # draw North wall
                    line = self.w.create_line(tl_x, tl_y, tr_x, tr_y)
                if (cell.e == Cell.WALL):
                    # draw East wall
                    line = self.w.create_line(tr_x, tr_y, br_x, br_y)
                if (cell.s == Cell.WALL):
                    # draw South wall
                    line = self.w.create_line(bl_x, bl_y, br_x, br_y)
                if (cell.w == Cell.WALL):
                    # draw West wall
                    line = self.w.create_line(tl_x, tl_y, bl_x, bl_y)

                if (cell == self.current_cell):
                    # draw us
                    if (self.current_direction.facing(Direction.NORTH)):
                        tc_x = (tr_x + tl_x) / 2
                        tc_y = tl_y
                        cursor = self.w.create_line(bl_x, bl_y, tc_x, tc_y, br_x, br_y)
                    if (self.current_direction.facing(Direction.EAST)):
                        rc_x = tr_x
                        rc_y = (tr_y + br_y) / 2
                        cursor = self.w.create_line(tl_x, tl_y, rc_x, rc_y, bl_x, bl_y)
                    if (self.current_direction.facing(Direction.SOUTH)):
                        bc_x = (tr_x + tl_x) / 2
                        bc_y = bl_y
                        cursor = self.w.create_line(tl_x, tl_y, bc_x, bc_y, tr_x, tr_y)
                    if (self.current_direction.facing(Direction.WEST)):
                        lc_x = tl_x
                        lc_y = (tr_y + br_y) / 2
                        cursor = self.w.create_line(tr_x, tr_y, lc_x, lc_y, br_x, br_y)

        self.showing_map = True

    def start(self):
        self.root.bind("<Up>", self.up_arrow)
        self.root.bind("<Left>", self.left_arrow)
        self.root.bind("<Right>", self.right_arrow)
        self.root.bind("<Down>", self.down_arrow)
        self.root.bind("m", self.m_key)

        self.draw()

        self.root.mainloop()

game = Maze3DGame()
game.start()
