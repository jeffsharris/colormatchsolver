#!/usr/bin/env python
# -*- coding: utf-8 -*-
positions = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]
maxPosition = 0

class Tile:
	def __init__(self, color1, color2, color3, color4):
		self.colors = []
		self.colors.append(color1)
		self.colors.append(color2)
		self.colors.append(color3)
		self.colors.append(color4)
		
	def getEdge(self, edge): # 0 = top, 1 = right, 2 = bottom, 3 = left
		if edge == 0:
			return Edge(self.colors[0], self.colors[1])
		elif edge == 1:
			return Edge(self.colors[1], self.colors[2])
		elif edge == 2:
			return Edge(self.colors[3], self.colors[2])
		elif edge == 3:
			return Edge (self.colors[0], self.colors[3])
		else:
			return null
			
	def __str__(self):
		colorString = ""
		for x in self.colors:
			colorString += x + " "
		return colorString
			
class Edge:
	def __init__(self, color1, color2):
		self.color1 = color1
		self.color2 = color2
	def __eq__(self, other):
		return (self.color1 == other.color1) & (self.color2 == other.color2)
	def __ne__(self, other):
		return (self.color1 != other.color1) | (self.color2 != other.color2)
	def __str__(self):
		return (self.color1 + " " + self.color2)

class Placement: # rotation: 0 = not rotated, 1 = rotated 90° clockwise, 2 = 180°, 3 = 270°

	def __init__(self, baseTile, rotation):
		if rotation == 0:
			self.virtualTile = Tile(baseTile.colors[0], baseTile.colors[1], baseTile.colors[2], baseTile.colors[3])
		elif rotation == 1:
			self.virtualTile = Tile(baseTile.colors[3], baseTile.colors[0], baseTile.colors[1], baseTile.colors[2])
		elif rotation == 2:
			self.virtualTile = Tile(baseTile.colors[2], baseTile.colors[3], baseTile.colors[0], baseTile.colors[1])
		elif rotation == 3:
			self.virtualTile = Tile(baseTile.colors[1], baseTile.colors[2], baseTile.colors[3], baseTile.colors[0])
	def getEdge(self, edge):
		return self.virtualTile.getEdge(edge)
	def __str__(self):
		return str(self.virtualTile)

class Grid:
	def __init__(self):
		self.positionArray = [None] * 16

	def place(self, placement, location):
		if (location > 4) & (location != 7):
			if placement.getEdge(0) != self.positionArray[location - 4].getEdge(2):
				return False

		if (location % 4 > 0) & (location != 1) & (location != 13):
			if placement.getEdge(3) != self.positionArray[location - 1].getEdge(1):
				return False

		if (location <= 0 | location == 3 | location == 12 | location >= 15):
			raise Exception("Invalid location: " + location)
			
		self.positionArray[location] = placement
		return True

	def remove(self, location):
		self.positionArray[location] = None

	def __str__(self):
		s = ""
		for i in positions:
			s += "Tile " + str(i) + ":" + str(self.positionArray[i]) + "\n"
		return s
			
def addToGrid(grid, positionIndex, remainingTiles):
	global maxPosition
	if positionIndex > maxPosition:
		
		print "Found grid of " + str(positionIndex) + " tiles:\n"
		print str(grid) + "---"
		maxPosition = positionIndex
	for i in remainingTiles:
		for j in range(4):
			if grid.place(Placement(i, j), positions[positionIndex]):			
				if (positionIndex == 11):
					print grid
					return True
				newTiles = []
				for k in remainingTiles:
					if k != i:
						newTiles.append(k)
				validPosition = addToGrid(grid, positionIndex+1, newTiles)
				if validPosition: 
					return True
	return False # we were not able to add the tile


tiles = [None] * 12
tiles[0] = Tile("blue", "red", "white", "green")
tiles[1] = Tile("blue", "red", "white", "green")
tiles[2] = Tile("blue", "red", "green", "white")
tiles[3] = Tile("blue", "red", "green", "white")
tiles[4] = Tile("blue", "green", "yellow", "red")
tiles[5] = Tile("blue", "green", "yellow", "red")
tiles[6] = Tile("blue", "yellow", "green", "red")
tiles[7] = Tile("blue", "white", "red", "yellow")
tiles[8] = Tile("blue", "white", "red", "yellow")
tiles[9] = Tile("blue", "yellow", "red", "green")
tiles[10] = Tile("blue", "yellow", "red", "green")
tiles[11] = Tile("blue", "yellow", "green", "red")

grid = Grid()
foundSolution = addToGrid(grid, 0, tiles)
print "Was a solution found? " + str(foundSolution)