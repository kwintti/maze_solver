from tkinter import Tk, BOTH, Canvas
from time import sleep
import random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze solver")

        self.__canvas = Canvas(self.__root, bg="white",
                               height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def close(self):
        self.__window_running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x


class Line:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_color="red"):
        canvas.create_line(
                self.point_a.x, self.point_a.y, self.point_b.x,
                self.point_b.y, fill=fill_color, width=2
                )
        canvas.pack(fill=BOTH, expand=1)


class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win
        self._visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y2 = y2
        self._x2 = x2
        self._y1 = y1
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        if self.has_left_wall is False:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        if self.has_right_wall is False:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        if self.has_top_wall is False:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        if self.has_bottom_wall is False:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        midx = (self._x1 + self._x2)/2
        midy = (self._y1 + self._y2)/2

        to_midx = (to_cell._x1 + to_cell._x2)/2
        to_midy = (to_cell._y1 + to_cell._y2)/2
        color = "gray"
        if undo is False:
            color = "red"
        line = Line(Point(midx, midy), Point(to_midx, to_midy))
        self._win.draw_line(line, color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        if seed is not None:
            random.seed(seed)

    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                column.append(cell)
                self._draw_cell(cell, i, j)
            self._cells.append(column)
        self._break_entrance_and_exit()

    def _draw_cell(self, cell, i, j):
        x1 = (self._cell_size_x * i) + self._x1
        y1 = (self._cell_size_y * j) + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(self._cells[0][0], 0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._cells[-1][-1], len(self._cells)-1, len(self._cells[0])-1)

    def print_maze(self):
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if self._cells[i][j]._visited:
                    print('.', end='') # Visited cell
                elif (self._cells[i][j].has_top_wall and
                      self._cells[i][j].has_bottom_wall and
                      self._cells[i][j].has_left_wall and
                      self._cells[i][j].has_right_wall):
                    print('#', end='') # Wall
                else:
                    print(' ', end='') # Empty space
            print('\n')  # Newline at the end of each row

    def _break_walls_r(self, i, j):
        print("hello", i, j)
        self._cells[i][j]._visited = True
        while True:
            cells_to_visit = []
            if i == 0 and j == 0:
                if self._cells[i+1][j]._visited is True and self._cells[i][j+1]._visited is True:
                    self._draw_cell(self._cells[i][j], i, j)
                    return
                # check right cell
                if self._cells[i+1][j]._visited is False:
                    cells_to_visit.append((i+1, j))
                # check down cell
                if self._cells[i][j+1]._visited is False:
                    cells_to_visit.append((i, j+1))
            elif i == 0 and j == self._num_rows-1:
                if self._cells[i+1][j]._visited is True and self._cells[i][j-1]._visited is True:
                    self._draw_cell(self._cells[i][j], i, j)
                    return
                # check right cell
                if self._cells[i+1][j]._visited is False:
                    cells_to_visit.append((i+1, j))
                # check up cell
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            elif i == self._num_cols-1 and j == self._num_rows-1:
                if self._cells[i-1][j]._visited is True and self._cells[i][j-1]._visited is True:
                    self._draw_cell(self._cells[i][j], i, j)
                    return
                # check left cell
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check up cell
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            elif i == self._num_cols-1 and j == 0:
                if self._cells[i-1][j]._visited is True and self._cells[i][j+1]._visited is True:
                    self._draw_cell(self._cells[i][j], i, j)
                    return
                # check left cell
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check up cell
                if self._cells[i][j+1]._visited is False:
                    cells_to_visit.append((i, j+1))
            elif i == self._num_cols-1 and j == self._num_rows-1:
                if self._cells[i-1][j]._visited is True and self._cells[i][j-1]._visited is True:
                    self._draw_cell(self._cells[i][j], i, j)
                    return
                # check left cell
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check up cell
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            elif i == 0 and j < self._num_rows-1 and j > 0:
                print("jei", i, j, self._num_rows)
                # check right cell
                if self._cells[i+1][j]._visited is False:
                    print("you")
                    cells_to_visit.append((i+1, j))
                # check bottom cell
                if self._cells[i][j+1]._visited is False:
                    cells_to_visit.append((i, j+1))
                # check up cell
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            elif j == 0 and i < self._num_cols and i > 0:
                # check left cell
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check right cell
                if self._cells[i+1][j]._visited is False:
                    cells_to_visit.append((i+1, j))
                # check bottom cell
                if self._cells[i][j+1]._visited is False:
                    cells_to_visit.append((i, j+1))
            elif i < self._num_cols-1 and j == self._num_rows-1:
                # check left
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check right
                if self._cells[i+1][j]._visited is False:
                    cells_to_visit.append((i+1, j))
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            elif i == self._num_cols-1 and j < self._num_rows-1:
                # check left
                if self._cells[i-1][j]._visited is False:
                    cells_to_visit.append((i-1, j))
                # check bottom
                if self._cells[i][j+1]._visited is False:
                    cells_to_visit.append((i, j+1))
                if self._cells[i][j-1]._visited is False:
                    cells_to_visit.append((i, j-1))
            else:
                if i < self._num_cols-1 and j < self._num_rows-1 and i > 0 and j > 0:
                    print("heip")
                    if self._cells[i+1][j]._visited is True and self._cells[i][j+1]._visited is True and self._cells[i-1][j]._visited is True and self._cells[i][j-1]._visited is True:
                        self._draw_cell(self._cells[i][j], i, j)
                        return
                    else:
                        # check right cell
                        if self._cells[i+1][j]._visited is False:
                            cells_to_visit.append((i+1, j))
                        # check down cell
                        if self._cells[i][j+1]._visited is False:
                            cells_to_visit.append((i, j+1))
                        # check left cell
                        if self._cells[i-1][j]._visited is False:
                            cells_to_visit.append((i-1, j))
                        # check up cell
                        if self._cells[i][j-1]._visited is False:
                            cells_to_visit.append((i, j-1))

            print(cells_to_visit)
            if len(cells_to_visit) > 0:
                new_i, new_j = cells_to_visit[random.randrange(0, len(cells_to_visit))]
                if i == new_i and j+1 == new_j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[new_i][new_j].has_top_wall = False
                    self._break_walls_r(new_i, new_j)
                    self._draw_cell(self._cells[i][j], i, j)
                if i+1 == new_i and j == new_j:
                    self._cells[i][j].has_right_wall = False
                    self._cells[new_i][new_j].has_left_wall = False
                    self._break_walls_r(new_i, new_j)
                    self._draw_cell(self._cells[i][j], i, j)
                if i-1 == new_i and j == new_j:
                    self._cells[i][j].has_left_wall = False
                    self._cells[new_i][new_j].has_right_wall = False
                    self._break_walls_r(new_i, new_j)
                    self._draw_cell(self._cells[i][j], i, j)
                if i == new_i and j-1 == new_j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[new_i][new_j].has_bottom_wall = False
                    self._break_walls_r(new_i, new_j)
                    self._draw_cell(self._cells[i][j], i, j)

            return
       #self.print_maze()

    def _reset_cells_visited(self):

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j]._visited = False
                print("resetting", self._cells[i][j]._visited)




def main():
    win = Window(1200, 600)
    # win.draw_line(Line(Point(10,10), Point(400, 450)), "red")
   # cell = Cell(win)
   # cell.has_left_wall = False
   # cell.draw(10,10,100,150)
   # cell2 = Cell(win)
   # cell2.draw(200,250, 600, 550)
   # cell.draw_move(cell2)
    maze = Maze(100, 100, 5, 5, 150, 50, win, seed=0) 
    maze._break_walls_r(0,0)
    maze._reset_cells_visited()

    win.wait_for_close()

main()
