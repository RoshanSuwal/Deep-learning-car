import pygame
import os
import time
from os import path

from math import sin,cos,radians,degrees,copysign
from pygame.math import Vector2
import numpy as np
pygame.font.init()

dis=pygame.display.set_mode((800,600))
TILE_SIZE=16
BLOCK_IMG=pygame.transform.scale(pygame.image.load(os.path.join("imgs","block.png")).convert_alpha(),(TILE_SIZE,TILE_SIZE))


class Blocks:
	def __init__(self,x,y):
		self.x=x*TILE_SIZE
		self.y=y*TILE_SIZE
		self.img=BLOCK_IMG

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

	def collision(self,px,py,w,h):
		rect=self.img.get_rect()
		tx=False
		ty=False

		if rect.width>=w:
			tx=(self.x>=px and self.x<=px+w) or (self.x+rect.width>=px and self.x+rect.width<=px+w)
		else:
			tx=(px>=self.x and px<=self.x+rect.width) or (px+w>=self.x and px+w<=self.x+rect.width)

		if rect.height>=h:
			ty=(self.y>=py and self.y<=py+h) or (self.y+rect.height>=py and self.y+rect.height<=py+h)
		else:
			ty=(py>=self.y and py<=self.y+rect.height) or (py+h>=self.y and py+h<=self.y+rect.height)

		return (tx and ty)

	def collision_circle(self,cx,cy,raduis):
		dx=cx-self.x-TILE_SIZE/2
		dy=cy-self.y-TILE_SIZE/2

		d=(dx**2+dy**2)**(1/2)
		if d<(raduis+TILE_SIZE/2):
			return True
		return False

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))
		pygame.draw.circle(win,(255,255,255),(self.x,self.y),2)


class Wall:
	def __init__(self):
		game_folder=path.dirname(__file__)
		self.map_data=[]
		self.wall_sprites=[]
		with open(path.join(game_folder,'map.txt'),'rt') as f:
			for line in f:
				self.map_data.append(line)

		for row,tiles in enumerate(self.map_data):
			for col,tile in enumerate(tiles):
				if tile == '1':
					self.wall_sprites.append(Blocks(col,row))

	def collision(self,x,y,car_x,car_y):
		for wall_sprite in self.wall_sprites:
			if wall_sprite.collision(x,y,car_x,car_y):
				return True
		return False

	def collision_circle(self,cx,cy,cr):
		for wall_sprite in self.wall_sprites:
			if wall_sprite.collision_circle(cx,cy,cr):
				return True
		return False

	def distance(self,x,y,w,z):
		return int(((x-w)**2+(y-z)**2)**0.5)

	def draw(self,win):
		for wall_sprite in self.wall_sprites:
			wall_sprite.draw(win)

	def distance_using_circle_collision(self,center_x,center_y,angle):
		STEP=TILE_SIZE/2
		collision_distance=[9 for _ in range(5)]

		sine=[sin(radians(-angle+75)),sin(radians(-angle+30)),sin(radians(-angle)),sin(radians(-angle-30)),sin(radians(-angle-75))]
		cosine=[cos(radians(angle-75)),cos(radians(angle-30)),cos(radians(angle)),cos(radians(angle+30)),cos(radians(angle+75))]

		dx=[i*TILE_SIZE for i in cosine]
		dy=[i*TILE_SIZE for i in sine]

		for i in range(1,8):
			for wall_sprite in self.wall_sprites:
				for j in range(len(dx)):
					if collision_distance[j]==9:
						if wall_sprite.collision_circle(int(center_x+i*dx[j]),int(center_y+i*dy[j]),TILE_SIZE/2):
							dxx=center_x-wall_sprite.x-TILE_SIZE/2
							dyy=center_y-wall_sprite.y-TILE_SIZE/2
							collision_distance[j]=i


		#print(angle,"distance:",collision_distance)
		return collision_distance













