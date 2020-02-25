import pygame
import arena
import car as CAR
import sys
import os
from os import path
import time
import math
import pygame.math

import neat 
import visualize
import pickle
import numpy as np

WIDTH=800
HEIGHT=600
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
BLOCK_IMG=pygame.transform.scale(pygame.image.load(os.path.join("imgs","block.png")).convert_alpha(),(16,16))
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Game:
	def __init__(self):
		self.screen=WIN
		pygame.display.set_caption("2DCAR")
		self.clock=pygame.time.Clock()
		self.ticks=60
		self.wall=arena.Wall()
		self.car=CAR.Car(3,3)
		self.nets=[]
		self.cars=[]
		self.ge=[]

	def draw(self):
		self.wall.draw(self.screen)
		#self.car.draw(self.screen,dis)
		self.car.draws(self.screen)
		pygame.display.update()

	def draw_nets(self,score,velocity):
		score_label=STAT_FONT.render("Score:"+str(score),1,(255,255,255))
		self.screen.blit(score_label,(WIDTH-score_label.get_width()-15,10))
		velocity_label=STAT_FONT.render("velocity:"+str(velocity),1,(255,255,255))
		self.screen.blit(velocity_label,(WIDTH-velocity_label.get_width()-15,10+velocity_label.get_height()))
		population_label=STAT_FONT.render("population:"+str(len(self.cars)),1,(255,255,255))
		self.screen.blit(population_label,(WIDTH-population_label.get_width()-15,10+velocity_label.get_height()+population_label.get_height()))
		self.wall.draw(self.screen)
		for car in self.cars:
			car.draws(self.screen)
		pygame.display.update()


	def run(self):
		dt=self.clock.get_time()/1000
		pressed=pygame.key.get_pressed()
		#print("RUn")
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()

		'''if pressed[pygame.K_UP]:
			#print("Pressed up")
			p="MOVE_FORWARD"
			self.car.controls(1,dt)
		elif pressed[pygame.K_DOWN]:
			self.car.controls('MOVE_BACKWARD',dt)
		elif pressed[pygame.K_RIGHT]:
			self.car.controls('RIGHT_TURN',dt)
		elif pressed[pygame.K_LEFT]:
			self.car.controls('LEFT_TURN',dt)
		else:
			self.car.controls('update',dt)

		
		#self.car.update(dt)'''
		self.screen.fill((0,0,0))
		if self.wall.collision(self.car.position.x,self.car.position.y,self.car.width,self.car.height):
			pass
			#print("collision has occured")
		if self.wall.collision_circle(self.car.center_points.x,self.car.center_points.y,self.car.rad):
			print("collisionn")
		else:
			print("no collision")


		dis=self.wall.distance_using_circle_collision(self.car.center_points.x,self.car.center_points.y,self.car.angle)
		
		print("dis",dis,self.car.distance)
		right= dis[0] if dis[0]>dis[1] else dis[1]
		left=dis[3] if dis[3]>dis[4] else dis[4]

		if left>right:
			self.car.controls('LEFT_TURN',1)
		elif right>left:
			self.car.controls('RIGHT_TURN',1)
		else:
			self.car.controls('update',dt)
		self.car.update(dt)

		self.draw()
		
		self.clock.tick(self.ticks)

	def eval_genomes(self,genomes,config):
		
		self.cars=[]
		self.nets=[]
		self.ge=[]

		for genome_id,genome in genomes:
			genome.fittness=0
			net=neat.nn.FeedForwardNetwork.create(genome,config)
			self.nets.append(net)
			self.cars.append(CAR.Car(3,3))
			self.ge.append(genome)

		run=True
		while run and len(self.cars)>0:
			max_fittness=0
			max_velocity=0
			dt=self.clock.get_time()/1000
			pressed=pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()

				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_UP:
						run=False


			for x,car in enumerate(self.cars):

				dis=self.wall.distance_using_circle_collision(car.center_points.x,car.center_points.y,car.angle)
				#dis.append(car.velocity.x)

				print(dis)
				output=self.nets[self.cars.index(car)].activate(dis)
				#print(x,output)
				if output[0]>0:
					self.cars[self.cars.index(car)].controls('MOVE_FORWARD',output[0])
				elif output[0]<0:
					self.cars[self.cars.index(car)].controls('MOVE_BACKWARD',-output[0])
				else:
					self.cars[self.cars.index(car)].controls('update',dt)

				if output[1]>0:
					self.cars[self.cars.index(car)].turning('RIGHT_TURN',1)
				elif output[1]<0:
					self.cars[self.cars.index(car)].turning('LEFT_TURN',1)
				
				
				#print(x,self.cars[self.cars.index(car)].position,dt)
				
				self.cars[self.cars.index(car)].update(dt)

				self.ge[x].fitness=self.cars[self.cars.index(car)].distance
				if self.ge[x].fitness>max_fittness:
					max_fittness=self.ge[x].fitness
				if self.cars[self.cars.index(car)].velocity.x>max_velocity:
					max_velocity=car.velocity.x
			##collision code
			for car in self.cars:
				if self.wall.collision_circle(car.center_points.x,car.center_points.y,car.rad):
					self.ge[self.cars.index(car)].fittness-=10
					self.nets.pop(self.cars.index(car))
					self.ge.pop(self.cars.index(car))
					self.cars.pop(self.cars.index(car))

			self.screen.fill((0,0,0))
			self.draw_nets(int(max_fittness),int(max_velocity))
			self.clock.tick(60)



	def config(self,config_file):
		config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
			neat.DefaultSpeciesSet,neat.DefaultStagnation,
			config_file)
		p=neat.Population(config)
		p.add_reporter(neat.StdOutReporter(True))
		stats=neat.StatisticsReporter()
		p.add_reporter(stats)
		winner=p.run(self.eval_genomes,50)
		print('\nBest genomes:\n{!s}'.format(winner))



g=Game()
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
g.config(config_path)
