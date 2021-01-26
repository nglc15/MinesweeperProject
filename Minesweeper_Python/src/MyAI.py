# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action
import random
class MyAI( AI ):
	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self._rowDimension = rowDimension
		self._colDimension = colDimension
		self._totalMines = totalMines
		self._startX = startX 
		self._startY = startY 
		self._frontier = []
		self._flagged = []
		self._labels = [] #list keeps track of tiles with effective label > 1.                  //
		self._safe = [(startX, startY)]
		self._uncovered = [(startX, startY)]
		self._minesLeft = totalMines
		self._round = 1
		self._tempTile = ()
		self._unsafe = []
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
	def getAction(self, number: int) -> "Action Object":
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self._round += 1
		# print("LAST SEEN TILE: (", self._startX, ", ", self._startY, ") = ", number)
		# print("UNCOVERED:")
		# print(self._uncovered)
		# print("FLAGGED:")
		# print(self._flagged, len(self._flagged))
		# print("SAFE TILES: ")
		# print(self._safe, len(self._safe))
		# # print("FRONTIER:")
		# print(self._frontier)
		# print("LABELS: ")
		# print(self._labels)
		# print(" ")
		# # print("ROUND: ", self._round)
		#if you've uncovered all the non-mine tiles, end the game
		if len(self._uncovered) == (self._rowDimension*self._colDimension) - self._totalMines:
			#print("gg! YOU'RE A WINNER")
			return Action(AI.Action.LEAVE)
		########################################
		#			RULES OF THUMB			   #
		########################################
		
		if len(self._flagged) == self._totalMines:
			return self.uncoverAll()
		#if the current tile value is 0, append neighboring tiles to safe list
		if number == 0:
			#FIRST RULE OF THUMB
			self.uncoverNeighbors(self._startX, self._startY)
			#uncover and search the last safely viewed tile
			for tile in self._safe:
				if tile not in self._uncovered:
					return self.nextSafeMove(tile)
			#if there are no more uncovered tiles to expand, guess from the frontier
			return self.flagger()
			# return self.guess()
		#if the tile has bombs around it
		elif number > 0:
			#adds label to label list 
			
			# if (self._startX, self._startY) in 
			self._labels.append((self._startX,self._startY, number))
			#add all neighboring uncovered tiles to the frontier list
			self.findFrontier(self._startX, self._startY)
			# #SECOND RULE OF THUMB: if the tile effective label == the number of uncovered neighbors, then add all those tiles to flagged list
			# self.thumbRule(self._startX, self._startY, number)
			#uncover the last safely viewed tile
			for tile in self._safe:
				if tile not in self._uncovered:
					return self.nextSafeMove(tile)
			#if no safe moves left, guess from frontier
			return self.flagger()
		elif number < 0:
			self.safetyCheck()
			for tile in self._safe:
				if tile not in self._uncovered:
					return self.nextSafeMove(tile)
			return self.flagger()
		# return self.guess()
		# elif number < 0:
		# 	return self.guess()
		########################################
		#		END OF RULES OF THUMB		   #
		########################################
		print("FAILED UNCOVER")
		# return Action(AI.Action.LEAVE, self._startX, self._startY)
		#######################################################
	# 					HELPER FUNCTIONS				  #
	#######################################################
	#adds all tiles that are safe to uncover to the safe list
	def uncoverNeighbors(self, x, y):
		for tile in self.getNeighbors(x, y):
			if tile not in self._safe:
				self._safe.append(tile)
		#if any of the safe tiles are in the frontier, remove them from the frontier
		for tile in self._safe:
				if tile in self._frontier:
					self._frontier.remove(tile)
	
	def thumbRule(self, x, y, effectiveValue):
		uncoveredNeighbors = []
		for tile in self.getNeighbors(x, y):
			if tile not in self._safe:
				uncoveredNeighbors.append(tile)
		# print("UN", uncoveredNeighbors)
		if effectiveValue == len(uncoveredNeighbors):
			for tile in uncoveredNeighbors:
				if tile not in self._flagged:
					# print("TILEEEEE: ", tile)
					self._flagged.append(tile)
					# self._uncovered.append(tile)
					self._frontier.remove(tile)
					# print("FLAG", tile[0], tile[1])
					self._startX = tile[0]
					self._startY = tile[1]
					# return Action(AI.Action.FLAG, tile[0], tile[1])
					return True
					# return (tile[0], tile[1])
		# print("flagged list: ", self._flagged) 
		# print("frontier: " , self._frontier)
		return False
	#adds all neighboring covered tiles to frontier
	def findFrontier(self, x, y):
		for tile in self.getNeighbors(x, y):
			if tile not in self._frontier and tile not in self._safe and tile not in self._flagged:
				self._frontier.append(tile)
	#uncover the last safely viewed tile
	def nextSafeMove(self, tile):
		self._startX = tile[0]
		self._startY = tile[1]
		self._uncovered.append(tile)
		# print("NEXTSAFEMOVE UNCOVER:", self._startX, self._startY)
		return Action(AI.Action.UNCOVER, self._startX, self._startY)
	
	def flagger(self):
		# print("label list:", self._labels)
		# print("safe ", self._safe)
		# print("uncovered ", self._uncovered)
		# print("labels:" ,self._labels)
		for tile in self._labels:
			# print("LOOKING AT: ", tile[0], tile[1])
			if self.thumbRule(tile[0],tile[1],tile[2]) == True:
				# print("HELLO")
				return Action(AI.Action.FLAG, self._startX, self._startY)	
		self.safetyCheck()
		for tile in self._safe:
			if tile not in self._uncovered:
				return self.nextSafeMove(tile)
		return self.OneOneRule()
	
	def safetyCheck(self): 
		for tile in self._labels:
			bombCount = 0
			for Tile in self.getNeighbors(tile[0], tile[1]):
				if Tile in self._flagged:
					bombCount += 1
			if tile[2] == bombCount:
				self._labels.remove((tile[0], tile[1], tile[2]))
				self.safeAdd(tile[0], tile[1])
	
	def safeAdd(self, x, y):
		if x > 0:
			if (((x - 1, y)  not in self._safe) and ((x - 1, y) not in self._flagged)):
				self._safe.append((x - 1, y))
			if y > 0 and ((x - 1, y - 1) not in self._safe) and ((x - 1, y - 1) not in self._flagged):
				self._safe.append((x - 1, y - 1))
			if y < self._rowDimension - 1 and ((x - 1, y + 1) not in self._safe) and ((x - 1, y + 1) not in self._flagged):
				self._safe.append((x - 1, y + 1))
		if y > 0 and ((x, y - 1) not in self._safe and ((x, y - 1) not in self._flagged)):
			self._safe.append((x, y - 1))
		if y < self._rowDimension - 1 and ((x, y + 1) not in self._safe) and ((x, y + 1) not in self._flagged):
			self._safe.append((x, y + 1))
		if x < self._colDimension - 1:
			if ((x + 1, y) not in self._safe and ((x + 1,y ) not in self._flagged)):
				self._safe.append((x + 1, y))
			if y > 0 and ((x + 1, y - 1) not in self._safe and ((x + 1, y - 1) not in self._flagged)):
				self._safe.append((x + 1, y - 1))
			if y < self._rowDimension - 1 and ((x + 1, y + 1) not in self._safe and ((x + 1, y + 1) not in self._flagged)):
				self._safe.append((x + 1, y + 1))

	def OneOneRule(self):
		updated = self.updateLabels() 
		# print(self._labels)
		# print(updated)
		for i in updated:
			if i[2] == 1:
				if i[0] == 0:
					if i[1] == self._rowDimension - 1:	#top left corner
						if (i[0]+1, i[1], 1) in updated:
							if (i[0]+2,i[1]) not in self._safe:
								self._safe.append((i[0]+2, i[1]))
							if (i[0]+2,i[1]-1) not in self._safe:
								self._safe.append((i[0]+2,i[1]-1))
						if(i[0], i[1]-1, 1) in updated:
							if(i[0],i[1]-2) not in self._safe:
								self._safe.append((i[0], i[1]-2))	
							if(i[0]+1,i[1]-2) not in self._safe:
								self._safe.append((i[0]+1,i[1]-2))
					elif i[1] == 0:					#bottom left corner
						if(i[0]+1, i[1], 1) in updated:
							if (i[0]+2, i[1]) not in self._safe:
								self._safe.append((i[0]+2,i[1]+1))
							if (i[0]+2,i[1]+1) not in self._safe:
								self._safe.append((i[0]+2,i[1]+1))
						if(i[0], i[1]+1, 1) in updated:
							if(i[0], i[1]+2) not in self._safe:
								self._safe.append((i[0], i[1]+2))
							if(i[0]+1, i[1]+2) not in self._safe:
								self._safe.append((i[0]+1, i[1]+2))
				elif i[0] == self._colDimension - 1:
					if i[1] == self._rowDimension - 1:	#top right corner
						if (i[0]-1, i[1], 1) in updated:
							if (i[0]-2, i[1]) not in self._safe:
								self._safe.append((i[0]-2,i[1]))
							if (i[0]-2,i[1]-1) not in self._safe:
								self._safe.append((i[0]-2, i[1]-1))
						if(i[0], i[1]-1, 1) in updated:
							if(i[0],i[1]-2) not in self._safe:
								self._safe.append((i[0], i[1]-2))	
							if(i[0]-1,i[2]-2) not in self._safe:
								self._safe.append((i[0]-1, i[1]-2))	
					elif i[1] == 0:					#bottom right corner
						if(i[0]-1, i[1], 1) in updated:
							if(i[0]-2,i[1]) not in self._safe:
								self._safe.append((i[0]-2,i[1]))
							if(i[0]-2,i[1]+1) not in self._safe:
								self._safe.append((i[0]-2,i[1]+1))
						if(i[0], i[1]+1, 1) in updated:
							if(i[0], i[1]+2) not in self._safe:
								self._safe.append((i[0],i[1]+2))
							if(i[0]-1,i[1]+2) not in self._safe:
								self._safe.append((i[0]-1, i[1]+2))
				if i[0] == 1 and (i[1] != self._rowDimension - 1 and i[1] != 0): #second column
					if (i[0]-1,i[1],1) in updated:
						if (i[0]+1,i[1]-1) not in self._safe and (i[0]+1,i[1]-1) not in self._flagged:
							self._safe.append((i[0]+1,i[1]-1))
						if (i[0]+1,i[1]) not in self._safe and (i[0]+1,i[1]) not in self._flagged:
							self._safe.append((i[0]+1,i[1]))
						if (i[0]+1,i[1]+1) not in self._safe and (i[0]+1,i[1]+1) not in self._flagged:
							self._safe.append((i[0]+1,i[1]+1))
				if i[0] == self._colDimension - 2 and (i[1] != self._rowDimension - 1 and i[1] != 0): #secondlast column
					if (i[0] + 1, i[1], 1) in updated:
						if (i[0]-1,i[1]-1) not in self._safe and (i[0]-1,i[1]-1) not in self._flagged:
							self._safe.append((i[0]-1,i[1]-1))
						if (i[0]-1,i[1]) not in self._safe and (i[0]-1,i[1]) not in self._flagged:
							self._safe.append((i[0]-1,i[1]))
						if (i[0]-1,i[1]+1) not in self._safe and (i[0]-1,i[1]+1) not in self._flagged:
							self._safe.append((i[0]-1,i[1]+1))
				if i[1] == 1 and (i[0] != 0 and i[0] != self._colDimension - 1): #second row
					if(i[0], i[1]-1, 1) in updated:
						if(i[0]-1,i[1]+1) not in self._safe and (i[0]-1,i[1]+1) not in self._flagged:
							self._safe.append((i[0]-1,i[1]+1))
						if(i[0],i[1]+1) not in self._safe and (i[0],i[1]+1) not in self._flagged:
							self._safe.append((i[0],i[1]+1))
						if(i[0]+1,i[1]+1) not in self._safe and (i[0]+1,i[1]+1) not in self._flagged:
							self._safe.append((i[0]+1,i[1]+1))
				if i[1] == self._rowDimension - 2 and (i[0] != 0 and i[0] != self._colDimension - 1): #secondlast row
					if(i[0], i[1]+1, 1) in updated:
						if (i[0]-1,i[1]-1) not in self._safe and (i[0]-1,i[1]-1) not in self._flagged:
							self._safe.append((i[0]-1,i[1]-1))
						if (i[0],i[1]-1) not in self._safe and  (i[0],i[1]-1) not in self._flagged:
							self._safe.append((i[0],i[1]-1))
						if (i[0]+1,i[1]-1) not in self._safe and (i[0]+1,i[1]-1) not in self._flagged:
							self._safe.append((i[0]+1,i[1]-1))
				if i[0] > 1 and i[0] < self._colDimension - 2 and i[1] > 1 and i[1] < self._rowDimension - 2:
					# print(i[0], i[1])
					if (i[0]+1,i[1],1) in updated:
						# print(1)
						if ((i[0]-1, i[1]) in self._safe or (i[0]-1, i[1]) in self._flagged) and ((i[0]-1, i[1]-1) in self._safe or (i[0]-1, i[1]-1) in self._flagged) and ((i[0]-1, i[1]+1) in self._safe or (i[0]-1, i[1]+1) in self._flagged):
							if(i[0]+2, i[1]) not in self._safe and (i[0]+2, i[1]) not in self._flagged:
								self._safe.append((i[0]+2, i[1]))
							if(i[0]+2, i[1]-1) not in self._safe and (i[0]+2, i[1]-1) not in self._flagged:
								self._safe.append((i[0]+2, i[1]-1))
							if(i[0]+2, i[1]+1) not in self._safe and (i[0]+2, i[1]+1) not in self._flagged:
								self._safe.append((i[0]+2, i[1]+1))
						if ((i[0]+2, i[1]) in self._safe or (i[0]+2, i[1]) in self._flagged) and ((i[0]+2, i[1]-1) in self._safe or (i[0]+2, i[1]-1) in self._flagged) and ((i[0]+2, i[1]+1) in self._safe or (i[0]+2, i[1]+1) in self._flagged):
							if(i[0]-1, i[1]) not in self._safe and (i[0]-1, i[1]) not in self._flagged:
								self._safe.append((i[0]-1, i[1]))
							if(i[0]-1, i[1]-1) not in self._safe and (i[0]-1, i[1]-1) not in self._flagged:
								self._safe.append((i[0]-1, i[1]-1))
							if(i[0]-1, i[1]+1) not in self._safe and (i[0]-1, i[1]+1) not in self._flagged:
								self._safe.append((i[0]-1, i[1]+1))
					if (i[0]-1,i[1],1) in updated:
						# print(2)
						if ((i[0]+1, i[1]) in self._safe or (i[0]+1, i[1]) in self._flagged) and (i[0]+1, i[1]-1) in self._safe or ((i[0]+1, i[1]-1) in self._flagged) and ((i[0]+1, i[1]+1) in self._safe or (i[0]+1, i[1]+1) in self._flagged):
							if(i[0]-2, i[1]) not in self._safe and (i[0]-2, i[1]) not in self._flagged:
								self._safe.append((i[0]-2, i[1]))
							if(i[0]-2, i[1]-1) not in self._safe and (i[0]-2, i[1]-1) not in self._flagged:
								self._safe.append((i[0]-2, i[1]-1))
							if(i[0]-2, i[1]+1) not in self._safe and (i[0]-2, i[1]+1) not in self._flagged:
								self._safe.append((i[0]-2, i[1]+1))
						if ((i[0]-2, i[1]) in self._safe or (i[0]-2, i[1]) in self._flagged) and ((i[0]-2, i[1]-1) in self._safe or (i[0]-2, i[1]-1) in self._flagged) and ((i[0]-2, i[1]+1) in self._safe or (i[0]-2, i[1]+1) in self._flagged):
							if(i[0]+1, i[1]) not in self._safe and (i[0]+1, i[1]) not in self._flagged:
								self._safe.append((i[0]+1, i[1]))
							if(i[0]+1, i[1]-1) not in self._safe and (i[0]+1, i[1]-1) not in self._flagged:
								self._safe.append((i[0]+1, i[1]-1))
							if(i[0]+1, i[1]+1) not in self._safe and (i[0]+1, i[1]+1) not in self._flagged:
								self._safe.append((i[0]+1, i[1]+1))
					if (i[0],i[1]+1,1) in updated:
						# print(3)
						if ((i[0]-1, i[1]-1) in self._safe or (i[0]-1, i[1]-1) in self._flagged) and ((i[0], i[1]-1) in self._safe or (i[0], i[1]-1) in self._flagged) and ((i[0]+1, i[1]-1) in self._safe or (i[0]+1, i[1]-1) in self._flagged):
							if(i[0]-1, i[1]+2) not in self._safe and (i[0]-1, i[1]+2) not in self._flagged:
								self._safe.append((i[0]-1,i[1]+2))
							if(i[0], i[1]+2) not in self._safe and (i[0], i[1]+2) not in self._flagged:
								self._safe.append((i[0],i[1]+2))
							if(i[0]+1, i[1]+2) not in self._safe and (i[0]+1, i[1]+2) not in self._flagged:
								self._safe.append((i[0]+1,i[1]+2))
						if((i[0]-1, i[1]+2) in self._safe or (i[0]-1, i[1]+2) in self._flagged) and ((i[0], i[1]+2) in self._safe or (i[0], i[1]+2) in self._flagged) and ((i[0]+1, i[1]+2) in self._safe or (i[0]+1, i[1]+2) in self._flagged):
							if(i[0]-1, i[1]-1) not in self._safe and (i[0]-1, i[1]-1) not in self._flagged:
								self._safe.append((i[0]-1,i[1]-1))
							if(i[0], i[1]-1) not in self._safe and (i[0], i[1]-1) not in self._flagged:
								self._safe.append((i[0],i[1]-1))
							if(i[0]+1, i[1]-1) not in self._safe and (i[0]+1, i[1]-1) not in self._flagged:
								self._safe.append((i[0]+1,i[1]-1))
					if (i[0],i[1]-1,1) in updated:
						# print(4)
						if((i[0]-1, i[1]+1) in self._safe or (i[0]-1, i[1]+1) in self._flagged) and ((i[0], i[1]+1) in self._safe or (i[0], i[1]+1) in self._flagged) and ((i[0]+1, i[1]+1) in self._safe or (i[0]+1, i[1]+1) in self._flagged):
							if(i[0]-1, i[1]-2) not in self._safe and (i[0]-1, i[1]-2) not in self._flagged:
								self._safe.append((i[0]-1,i[1]-2))
							if(i[0], i[1]-2) not in self._safe and (i[0], i[1]-2) not in self._flagged:
								self._safe.append((i[0],i[1]-2))
							if(i[0]+1, i[1]-2) not in self._safe and (i[0]+1, i[1]-2) not in self._flagged:
								self._safe.append((i[0]+1,i[1]-2))
						if((i[0]-1, i[1]-2) in self._safe or (i[0]-1, i[1]-2) in self._flagged) and ((i[0], i[1]-2) in self._safe or (i[0], i[1]-2) in self._flagged) and ((i[0]+1, i[1]-2) in self._safe or (i[0]+1, i[1]-2) in self._flagged):
							if(i[0]-1, i[1]+1) not in self._safe and (i[0]-1, i[1]+1) not in self._flagged:
								self._safe.append((i[0]-1,i[1]+1))
							if(i[0], i[1]+1) not in self._safe and (i[0], i[1]+1) not in self._flagged:
								self._safe.append((i[0],i[1]+1))
							if(i[0]+1, i[1]+1) not in self._safe and (i[0]+1, i[1]+1) not in self._flagged:
								self._safe.append((i[0]+1,i[1]+1))
		for tile in self._safe:
				if tile not in self._uncovered:
					return self.nextSafeMove(tile)
		return self.OneTwoRule()
	
	def OneTwoRule(self):
		updated = self.updateLabels() 
		for i in updated:
			if i[2] == 1:
					if (i[0]+1,i[1],2) in updated:
						if ((i[0]+2, i[1]) in self._safe or (i[0]+2, i[1]) in self._flagged) and ((i[0]+2, i[1]-1) in self._safe or (i[0]+2, i[1]-1) in self._flagged):
							if((i[0]+2, i[1]+1) not in self._safe and (i[0]+2, i[1]+1) not in self._flagged):
								self._flagged.append((i[0]+2,i[1]+1))
								return Action(AI.Action.FLAG, i[0]+2, i[1]+1)
						if ((i[0]+2, i[1]) in self._safe or (i[0]+2, i[1]) in self._flagged) and ((i[0]+2, i[1]+1) in self._safe or (i[0]+2, i[1]+1) in self._flagged):
							if((i[0]+2, i[1]-1) not in self._safe and (i[0]+2, i[1]-1) not in self._flagged):
								self._flagged.append((i[0]+2,i[1]-1))
								return Action(AI.Action.FLAG, i[0]+2, i[1]-1)
					if (i[0]-1,i[1],2) in updated:
						if ((i[0]-2, i[1]) in self._safe or (i[0]-2, i[1]) in self._flagged) and ((i[0]-2, i[1]-1) in self._safe or (i[0]-2, i[1]-1) in self._flagged):
							if((i[0]-2, i[1]+1) not in self._safe and (i[0]-2, i[1]+1) not in self._flagged):
								self._flagged.append((i[0]-2,i[1]+1))
								return Action(AI.Action.FLAG, i[0]-2, i[1]+1)
						if ((i[0]-2, i[1]) in self._safe or (i[0]-2, i[1]) in self._flagged) and ((i[0]-2, i[1]+1) in self._safe or (i[0]-2, i[1]+1) in self._flagged):
							if((i[0]-2, i[1]-1) not in self._safe and (i[0]-2, i[1]-1) not in self._flagged):
								self._flagged.append((i[0]-2,i[1]-1))
								return Action(AI.Action.FLAG, i[0]-2, i[1]-1)
					if (i[0],i[1]+1,2) in updated:
						if ((i[0], i[1]+2) in self._safe or (i[0], i[1]+2) in self._flagged) and ((i[0]+1, i[1]+2) in self._safe or (i[0]+1, i[1]+2) in self._flagged):
							if((i[0]-1, i[1]+2) not in self._safe and (i[0]-1, i[1]+2) not in self._flagged):
								self._flagged.append((i[0]-1,i[1]+2))
								return Action(AI.Action.FLAG, i[0]-1, i[1]+2)
						if ((i[0], i[1]+2) in self._safe or (i[0], i[1]+2) in self._flagged) and ((i[0]-1, i[1]+2) in self._safe or (i[0]-1, i[1]+2) in self._flagged):
							if((i[0]+1, i[1]+2) not in self._safe and (i[0]+1, i[1]+2) not in self._flagged):
								self._flagged.append((i[0]+1,i[1]+2))
								return Action(AI.Action.FLAG, i[0]+1, i[1]+2)
					if (i[0],i[1]-1,2) in updated:
						if ((i[0], i[1]-2) in self._safe or (i[0], i[1]-2) in self._flagged) and ((i[0]+1, i[1]-2) in self._safe or (i[0]+1, i[1]-2) in self._flagged):
							if((i[0]-1, i[1]-2) not in self._safe and (i[0]-1, i[1]-2) not in self._flagged):
								self._flagged.append((i[0]-1,i[1]-2))
								return Action(AI.Action.FLAG, i[0]-1, i[1]-2)
						if ((i[0], i[1]-2) in self._safe or (i[0], i[1]-2) in self._flagged) and ((i[0]-1, i[1]-2) in self._safe or (i[0]-1, i[1]-2) in self._flagged):
							if((i[0]+1, i[1]-2) not in self._safe and (i[0]+1, i[1]-2) not in self._flagged):
								self._flagged.append((i[0]+1,i[1]-2))
								return Action(AI.Action.FLAG, i[0]+1, i[1]-2)
		for tile in self._safe:
				if tile not in self._uncovered:
					return self.nextSafeMove(tile)
		return self.guess()
	
	# def updateLabels(self):
	# 	updated = []
	# 	for tile in self._labels:
	# 		bombCount = 0
	# 		for Tile in self.getNeighbors(tile[0], tile[1]):
	# 			if Tile in self._flagged:
	# 				bombCount += 1
	# 		if tile[2] != bombCount:
	# 			updated.append((tile[0],tile[1],tile[2]-bombCount))
	# 	return updated
	def updateLabels(self):
		updated = []
		for tile in self._labels:
			bombCount = 0
			if (tile[0] > 0):
				if ((tile[0] - 1, tile[1])  in self._flagged):
					bombCount+=1
				if tile[1] > 0 and ((tile[0] - 1, tile[1] - 1) in self._flagged):
					bombCount+=1
				if tile[1] < self._rowDimension - 1 and ((tile[0] - 1, tile[1] + 1) in self._flagged):
					bombCount+=1
			if tile[1] > 0 and ((tile[0] , tile[1] - 1) in self._flagged):
				bombCount+=1
			if tile[1] < self._rowDimension - 1 and ((tile[0], tile[1] + 1) in self._flagged):
				bombCount+=1
			if tile[0] < self._colDimension - 1:
				if ((tile[0] + 1, tile[1]) in self._flagged):
					bombCount+=1
				if tile[1] > 0 and ((tile[0] + 1, tile[1] - 1) in self._flagged):
					bombCount+=1
				if tile[1] < self._rowDimension - 1 and ((tile[0] + 1, tile[1] + 1) in self._flagged):
					bombCount+=1
			if tile[2] != bombCount:
				updated.append((tile[0],tile[1],tile[2]-bombCount))
		return updated
	#uncover the last tile appended to the frontier
	def guess(self):
		# print("GUESSING: " + str(self._startX) + ", " + str(self._startY))
		
		guess = dict()

		for Tile in self.updateLabels():
			for tile in self.getNeighbors(Tile[0], Tile[1]):
				if tile not in self._uncovered and tile not in self._flagged:
					if tile not in guess.keys():
						guess[tile] = Tile[2]
					else:
						guess[tile] += Tile[2]
		# print(guess)
		minList = []

		for k, v in guess.items():
			if v == min(guess.values()):
				minList.append(k)
		
		if len(minList) != 0:
			tile = random.choice(minList)

			self._startX = tile[0]
			self._startY = tile[1]
			self._safe.append(tile)
		else:
			self._startX = random.randrange(self._colDimension)
			self._startY = random.randrange(self._rowDimension)
			while (self._startX, self._startY) in self._uncovered or (self._startX, self._startY) in self._flagged:
				self._startX = random.randrange(self._colDimension)
				self._startY = random.randrange(self._rowDimension)
		return Action(AI.Action.UNCOVER, self._startX, self._startY)
	
	def uncoverAll(self):
		for x in range(self._colDimension):
			for y in range(self._rowDimension):
				if (x, y) not in self._uncovered and (x, y) not in self._flagged:
					self._uncovered.append((x, y))
					return Action(AI.Action.UNCOVER, x, y)
	
	def getNeighbors(self, x, y):
		neighbors = []
		if x > 0:
			neighbors.append((x - 1, y))
			if y > 0 :
				neighbors.append((x - 1, y - 1))
			if y < self._rowDimension - 1:
				neighbors.append((x - 1, y + 1))
		if y > 0:
			neighbors.append((x, y - 1))
		if y < self._rowDimension - 1:
			neighbors.append((x, y + 1))
		if x < self._colDimension - 1:
			neighbors.append((x + 1, y))
			if y > 0 :
				neighbors.append((x + 1, y - 1))
			if y < self._rowDimension - 1:
				neighbors.append((x + 1, y + 1))
		return neighbors
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################