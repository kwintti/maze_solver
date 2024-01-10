import unittest
from main import Maze
from unittest.mock import Mock

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Mock()
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
                len(m1._cells),
                num_cols,
                )
        self.assertEqual(
                len(m1._cells[0]),
                num_rows,
                )

    def test_break(self):
        win = Mock()
        m2 = Maze(0, 0, 10, 10, 15, 15, win)
        m2._break_entrance_and_exit()
        self.assertFalse(m2._cells[0][0].has_left_wall)
        self.assertFalse(m2._cells[-1][-1].has_bottom_wall)

    def test_resetting_maze(self):
        win = Mock()
        m3 = Maze(0, 0, 10, 10, 15, 15, win)
        m3._reset_cells_visited()
        for i in range(m3._num_cols):
            for j in range(m3._num_rows):
                self.assertFalse(m3._cells[i][j]._visited)

if __name__ == "__main__":
    unittest.main()
