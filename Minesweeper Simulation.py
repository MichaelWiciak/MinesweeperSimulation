import pygame
import random
import math
from timeit import default_timer as timer

try:
	f = open("minesweeperhighscores.txt","r")
	content = f.read()
	f.close()
	topten = content.split("\n")
	for i in range(10):
		topten[i] = topten[i].split("!")
		topten[i][0] = float(topten[i][0])
	topten.pop(10)
except:
	f = open("minesweeperhighscores.txt","w")
	for i in range(10):
		f.write("100000000000000!n/a\n")
	f.close()
	
	f = open("minesweeperhighscores.txt","r")
	content = f.read()
	f.close()
	topten = content.split("\n")
	for i in range(10):
		topten[i] = topten[i].split("!")
		topten[i][0] = float(topten[i][0])
	topten.pop(10)



pygame.init()

width = 400
height  = 500
rows = 20
cols = 20
w = 20
screen = pygame.display.set_mode((width,height))
bombs = 5


def write(x,y,text,size,colour):
	font = pygame.font.Font('freesansbold.ttf',size)
	writings = font.render(str(text),True,colour)
	screen.blit(writings,(x,y))	
	return writings



class Cell(object):
	
	def __init__(self,i,j,w):
		
		self.i = i
		self.j = j
		self.x = self.i * w 
		self.y = self.j * w
		self.w = w
		self.bomb = False
		self.revealed = False
		self.neighbours = None
		self.flag = False
		
	def show(self):
		pygame.draw.rect(screen,(255,255,255),(self.x,self.y,w,w))
		if self.flag:
			pygame.draw.rect(screen,(0,0,0),(self.x+5,self.y+5,10,8))
			pygame.draw.line(screen,(0,0,0),(self.x+5,self.y+5),(self.x+5,self.y+18))
		
		if self.revealed:
			pygame.draw.rect(screen,(200,200,200),(self.x,self.y,w,w))
			if self.bomb:
				pygame.draw.circle(screen,(0,0,0),(self.x+10,self.y+10),7)
			elif self.neighbours > 0:
				write(self.x+5,self.y+5,str(self.neighbours),15,(0,0,0))
				
				
	def reveal(self,mouse,lose):
		if mouse[0] > self.x and mouse[0] < self.x + 20 and mouse[1] > self.y and mouse[1] < self.y + 20 and not(self.flag):
			self.revealed = True
			if self.bomb:
				lose = True
				for i in range(rows):
					for j in range(cols):
						grid[i][j].revealed = True
			if self.neighbours == 0:
				self.fill()
		return lose
	def place_flag(self,total_flags):
		mouse = pygame.mouse.get_pos()
		if mouse[0] > self.x and mouse[0] < self.x + 20 and mouse[1] > self.y and mouse[1] < self.y + 20:
			if self.flag:
				self.flag = False
				total_flags += 1
				return total_flags
			else:
				self.flag = True
				total_flags  -= 1
				return total_flags
		else:
			return total_flags
		
	def revealer(self):
			self.revealed = True
			if self.neighbours == 0:
				self.fill()
	
	def countBombs(self):
		total = 0
		if self.bomb:
			self.neighbours = -1
			return
			
		for xoff in range(-1,2):
			for yoff in range(-1,2):
				i = self.i + xoff
				j = self.j + yoff
				if (i>-1 and i < rows and j > -1 and j < rows):
					neighbour = grid[i][j]
					if neighbour.bomb:
						total += 1
		self.neighbours = total
		
	def fill(self):
		for xoff in range(-1,2):
			for yoff in range(-1,2):
				i = self.i + xoff
				j = self.j + yoff
				if (i>-1 and i < rows and j > -1 and j < rows):	
					neighbour = grid[i][j]
					if not(neighbour.bomb) and not(neighbour.revealed):
						neighbour.revealer()
			
grid = []

for i in range(rows):
	grid.append([])
	for j in range(cols):
		grid[i].append(Cell(i,j,20))
		

allbombs = []		
for bomb in range(bombs):
	bombpos = [random.randint(0,rows-1),random.randint(0,cols-1)]
	while bombpos in allbombs:
		bombpos = [random.randint(0,rows-1),random.randint(0,cols-1)]
	allbombs.append(bombpos)
	grid[bombpos[0]][bombpos[1]].bomb = True
	
for i in range(rows):
	for j in range(cols):
		grid[i][j].countBombs()
	
total_flags = bombs
loop = True
time = 0 
win = False
lose = False
startscreen = True
highscorescreen = False
rulescreen = False
game = False
done = True
while loop:
	
	while startscreen:
		screen.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = False
				start = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					startscreen = False
					game = True
					text_loop = True
					base_font = pygame.font.Font(None,32)
					user_text = ""

					input_rect = pygame.Rect(50,200,140,32)
					colour_active = pygame.Color("lightskyblue3")
					colour_passive = pygame.Color(0,0,0)
					colour = colour_passive

					active = False
					box_input = "What's your name?"

					
					
					while text_loop:
						
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								pygame.quit()
								loop = False
							if event.type == pygame.MOUSEBUTTONDOWN:
								if input_rect.collidepoint(event.pos):
									active = True
									colour = colour_active
								else:
									active = False
									colour = colour_passive
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_RETURN:
									name = user_text
									box_input = "Hello "+name
									user_text = ""
									active = False
									colour = colour_passive
									text_loop = False
								elif active:
									if event.key == pygame.K_BACKSPACE:
										user_text = user_text[:-1]
									else:
										user_text += event.unicode
						
						screen.fill((255,255,255))
						
						pygame.draw.rect(screen,colour,input_rect,3)
						
						text_surface = base_font.render(user_text,True,(0,0,0))
						screen.blit(text_surface,(input_rect.x+5,input_rect.y+5))
						
						if not(active) and user_text == "":
							writings = write(input_rect.x+5,input_rect.y+5,box_input,32,(100,100,100))
							input_rect.w = max(text_surface.get_width()+10,writings.get_width()+10)
						else:
							input_rect.w = max(text_surface.get_width()+10,100)
						
						
						pygame.display.update()
					
					break
				elif event.key == pygame.K_h:
					startscreen = False
					highscorescreen = True
					break
				elif event.key == pygame.K_r:
					startscreen = False
					rulescreen = True
					break
		write(45,100,"Mine-Sweeper",45,(0,0,0))
		write(98,250,"Press Space to Start",20,(0,0,0))
		write(87,300,"Press H for highscores",20,(0,0,0))
		write(115,350,"Press R for Rules",20,(0,0,0))
		pygame.display.update()
		
	while rulescreen:
		screen.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = False
				screen = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					startscreen = True
					rulescreen = False
		write(30,50,"Mine-Sweeper Rules",35,(0,0,0))
		write(80,100,"Press Space to go home",20,(0,0,0))
		write(10,200,"Left-Click to dig up a square",15,(255,0,0))
		write(10,250,"Right-Click to place a flag",15,(255,0,0))
		write(10,300,"Click the scroller to remove a flag",15,(255,0,0))
		
				
		pygame.display.update()
	
	while highscorescreen:
		screen.fill((255,255,255))
		
		write(80,475,"Press Space to go home",20,(255,0,0))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				loop = False
				highscorescreen = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					startscreen = True
					highscorescreen = False
				
		write(10,10,"Position",15,(0,0,0))
		write(100,10,"Time",15,(0,0,0))
		write(200,10,"Name",15,(0,0,0))
		
		for i in range(10):
			write(30,i*45+40,str(i+1),15,(0,0,0))
			if topten[i][1] != "n/a":
				write(100,i*45+40,str(topten[i][0]),15,(0,0,0))
				write(200,i*45+40,str(topten[i][1]),15,(0,0,0))
			else:
				write(100,i*45+40,"not set",15,(0,0,0))
				write(200,i*45+40,"not set",15,(0,0,0))
		
		
		pygame.display.update()

	while game:
		if not(win) and not(lose):
			start = timer()
			
		
		screen.fill((255,255,255))
		
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop = False
					game = False
					
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		write(10,410,"Flags: "+str(total_flags),20,(0,0,0))
		write(10,450,"Time: "+str(round(time,2)),20,(0,0,0))
		
		not_revealed = 0
		for i in range(rows):
			for j in range(cols):
				grid[i][j].show()
				if not(grid[i][j].revealed):
					not_revealed += 1
		if not_revealed == bombs and total_flags == 0:
			win = True	
			write(150,420,"You Win",32,(255,0,0))
			
		if lose:
			for i in range(rows+1):
				pygame.draw.line(screen,(0,0,0),(i*w,0),(i*w,400),2)
			for j in range(cols+1):
				pygame.draw.line(screen,(0,0,0),(0,j*w),(400,j*w),2)
			write(150,420,"You Lose",32,(255,0,0))
			pygame.display.update()
			pygame.time.delay(5000)
			game = False
			startscreen = True
		
		if not(win):
			for i in range(rows):
				for j in range(cols):
					
					if click[0] == 1:
						lose = grid[i][j].reveal(mouse,lose)
					if click[2] == 1 and not(grid[i][j].flag):
						total_flags = grid[i][j].place_flag(total_flags)
					if click[1] == 1 and grid[i][j].flag:
						total_flags = grid[i][j].place_flag(total_flags)
		for i in range(rows+1):
			pygame.draw.line(screen,(0,0,0),(i*w,0),(i*w,400),2)
		for j in range(cols+1):
			pygame.draw.line(screen,(0,0,0),(0,j*w),(400,j*w),2)
		
		
			
			
		
		pygame.display.update()
		if not(win) and not(lose):
			end = timer()
			time += (end-start)
		
		if win and done:
			listy = [round(time,2),name]
			topten.append(listy)
			for i in range(10):
				for j in range(10):
					if topten[j][0] > topten[j+1][0]:
						switch = topten[j]
						topten[j] = topten[j+1]
						topten[j+1] = switch
			topten.pop(10)
			done = False
			
			f = open("minesweeperhighscores.txt","w")
			for i in range(10):
				f.write(str(topten[i][0])+"!"+str(topten[i][1])+"\n")
			f.close()
			
			pygame.display.update()
			pygame.time.delay(5000)
			game = False
			startscreen = True
			
