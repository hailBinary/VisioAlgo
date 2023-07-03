import pygame, sys
from button import Button
from utils import *
import math
from queue import PriorityQueue

pygame.display.set_caption("A* Path Finding Algorithm")

EXPLORED = (0, 180, 216) #explored nodes - light blue
OPEN = (0, 119, 182) #about to explore nodes - dark blue
BACKGROUND_COL = (8, 8, 8) #background color
OBSTACLE_COL = (244, 67, 54) #obstacle color - red
PATH = (255, 200, 87) #path color - yellow
START = (0, 41, 107) #start node - green
LINE_COL = (128, 128, 128) #line color
END = (255, 200, 87) #end node - gold

class Spot:
	def __init__(self, row, col, width, height, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * height
		self.color = BACKGROUND_COL
		self.neighbors = []
		self.width = width
		self.height = height
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == EXPLORED

	def is_open(self):
		return self.color == OPEN

	def is_barrier(self):
		return self.color == OBSTACLE_COL

	def is_start(self):
		return self.color == START

	def is_end(self):
		return self.color == END

	def reset(self):
		self.color = BACKGROUND_COL

	def make_start(self):
		self.color = START

	def make_closed(self):
		self.color = EXPLORED

	def make_open(self):
		self.color = OPEN

	def make_barrier(self):
		self.color = OBSTACLE_COL

	def make_end(self):
		self.color = END

	def make_path(self):
		self.color = PATH

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()



def make_grid(rows, width, height):
	grid = []
	gap1 = width // rows
	gap2 = height // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap1, gap2, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width, height):
	gap1 = width // rows
	gap2 = height // rows
	for i in range(rows + 1):
		pygame.draw.line(win, LINE_COL, (0, i * gap2), (width, i * gap2))
		for j in range(rows + 1):
			pygame.draw.line(win, LINE_COL, (j * gap1, 0), (j * gap1, width))


def draw(win, grid, rows, width, height):
	win.fill(BACKGROUND_COL)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width,height)
	pygame.display.update()


def get_clicked_pos(pos, rows, width, height):
	gap1 = width // rows
	gap2 = height // rows
	y, x = pos

	row = y // gap1
	col = x // gap2

	return row, col
