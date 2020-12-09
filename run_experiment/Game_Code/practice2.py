import pygame, math as m
import pandas as pd 
import numpy as np
import random
import sys
import os
import time 
import datetime
pygame.init()


##Color RGB values 
black = [   0,   0,   0]
white = [ 255, 255, 255]
green = [   0, 255,   0]
red   = [ 255,   0,   0]
blue  = [   0,   0, 255]

screen = pygame.display.set_mode((0,0), pygame.RESIZABLE , 0)
pos = pygame.mouse.get_pos()
rand = random.randint(0,250)
myfont = pygame.font.SysFont("Britannic Bold", 25)


order = [1]

for iterator in range(len(order)):
	done = False

	now = datetime.datetime.today().strftime('%m-%d-%y_%H-%M-%S')

	os.chdir('/Users/cogmech/Documents/NRT-Hyperbolic_Search/experiment/experiment')

	pygame.display.set_caption("Network Search Game")
	pygame.mouse.set_visible(1)
	screen.fill(white)
	pygame.display.flip()

	##Loads node location data and scales it to proper screen dimensions
	df = pd.read_excel('/Users/cogmech/Documents/NRT-Hyperbolic_Search/experiment/experiment/practice_maps/practice_maps/practice_eucl_nodes/'+str(order[iterator])+'.xlsx')
	df = df.as_matrix()

	sclr1 = abs(min(df[:,0]))
	sclr2 = abs(min(df[:,1]))
	#scales values into positive
	df[:,0] += sclr1
	df[:,1] += sclr2
	#Adding shifts X to the right
	df[:,0] += 378
	#Subtracting shifts Y up
	df[:,1] += 85


	##Loads distance values 
	df2 = pd.read_excel('/Users/cogmech/Documents/NRT-Hyperbolic_Search/experiment/experiment/practice_maps/practice_maps/practice_eucl_distances/'+str(order[iterator])+'.xlsx')
	df2 = df2.as_matrix()


	##Draws nodes
	for i in range(0,len(df)): #iterates on length number of nodes
	    x2 = df[i][0]
	    y2 = df[i][1]
	    pygame.draw.circle(screen, green, (x2, y2), 7, 0)
	    pygame.display.flip()

	pygame.mouse.set_pos(rand,rand)

	##Parameters
	energy = 5
	player_fuel = energy*2 
	player_fuel_back = energy*2
	ii = 0


	mindx = []
	node = []
	nx = []
	ny = []
	energyhist = []
	timehist = []
	#score is based on number of unique nodes visited
	scorehist = []
	scorehist_str = []


	##Fuelbar starter
	fuelbar = myfont.render('Fuel', False, black)
	screen.blit(fuelbar,(1250,42))

	pygame.draw.rect(screen, green, (1250,65,player_fuel,20),0)
	pygame.display.flip()

	###################################################################
	font_name = pygame.font.match_font('arial')
	def draw_text(surf, text, size, x, y, color):
	    font = pygame.font.Font(font_name,size)
	    text_surface = font.render(text, True, color)
	    text_rect = text_surface.get_rect()
	    text_rect.midtop = (x, y)
	    surf.blit(text_surface, text_rect)
	    pygame.display.flip()

	def fuel_bar(player_fuel):
	    pygame.draw.rect(screen, green, (1250,65,player_fuel,20),0)
	####################################################################

	##Game Loop
	while not done:
	    #Click Event
	    for event in pygame.event.get():
	        mouse = pygame.mouse.get_pos()
	        ##Future cost surveying 
	        if ii >= 1:
	        	for enum, row in enumerate(df):
	        		if df[enum][0]-8 <= mouse[0] <= df[enum][0]+8 and df[enum][1]-8 <= mouse[1] <= df[enum][1]+8:
	        			draw_text(screen, str(df2[mindx[ii-1]][enum]), 18, 1350, 90, black)
	        	pygame.draw.rect(screen, white, (1325, 90, 50, 20), 0)
	        			

	        if event.type == pygame.MOUSEBUTTONDOWN:
	            for j, row in enumerate(df):
	                if df[j][0]-8 <= mouse[0] <= df[j][0]+8 and df[j][1]-8 <= mouse[1] <= df[j][1]+8:
	                    t = time.clock()

	                    timehist.append(t)
	                    node.append(j)
	                    nx.append(df[j][0])
	                    ny.append(df[j][1])
	                    mindx.append(j)
	                    
	                    pygame.draw.circle(screen, red, (df[j][0], df[j][1]), 5, 0)
	                    pygame.display.flip()
	                    pygame.event.clear()

	                    ##Energy Calculation
	                    if ii >= 1:          
	                        energy = energy - df2[mindx[ii-1]][mindx[ii]]
	                        pygame.draw.circle(screen, blue, (df[mindx[ii-1]][0], df[mindx[ii-1]][1]), 5, 0)
	                        pygame.display.flip()

	                        energyhist.append(energy)

	                        ##Fuelbar interaction 
	                        pygame.draw.rect(screen, red, (1250,65,player_fuel_back,20),0)
	                        pygame.display.flip()

	                        player_fuel = player_fuel - df2[mindx[ii-1]][mindx[ii]]*2
	                        fuel_bar(player_fuel)
	                        pygame.display.flip()

	                        ##Score update
	                        unode = np.unique(node)
	                        print(unode)
	                        scorehist.append(len(unode))
	                        scorehist_str.append(str(len(unode)))
	                        print(scorehist)
	                        pygame.draw.rect(screen, white, (100,50,50,20),0)
	                        pygame.display.flip()
	                        draw_text(screen,scorehist_str[ii],18,110,50,black)
	                        ii = ii + 1
	                    else: 
	                        unode = np.unique(node)
	                        scorehist.append(len(unode))
	                        scorehist_str.append(str(len(unode)))
	                        draw_text(screen,scorehist_str[ii],18,110,50,black)
	                        ii = ii + 1
	                        energyhist.append(energy)

	    if event.type == pygame.QUIT or energy <= 0:

	    	done = True