import pygame
import os
import time

from pygame.math import Vector2
from math import sin,cos,radians,degrees,copysign

TILE_SIZE=16
dis=pygame.display.set_mode((800,600))
CAR_IMG=pygame.transform.scale(pygame.image.load(os.path.join("imgs","car.png")).convert_alpha(),(32,16))

class Car:
	def __init__(self,x,y,angle=-90):
		self.img=CAR_IMG
		self.lenght=16
		self.position=Vector2(x*TILE_SIZE,y*TILE_SIZE)
		self.width=0
		self.height=0
		self.rad=10
		self.distance=0.0
		self.center_points=self.position
		self.velocity=Vector2(80.0,0.0)## ==(horizental,vertical) velocity
		self.angle=angle
		self.max_acceleration=5.0*TILE_SIZE
		self.max_steering=30 ##maxing angle of turing 30 degree
		self.max_velocity=20*TILE_SIZE
		self.brake_deceleration=10*TILE_SIZE
		self.free_deceleration=2*TILE_SIZE

		self.acceleration=0.0
		self.steering=0.0

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

	def update(self,dt):
		
		self.velocity+=(self.acceleration*dt,0)
		self.velocity.x=max(-self.max_velocity,min(self.velocity.x,self.max_velocity))
		
		if self.steering:
			turing_radius=self.lenght/sin(radians(self.steering))
			angular_velocity=self.velocity.x/turing_radius
		else:
			angular_velocity=0

		self.position+=self.velocity.rotate(-self.angle)*dt
		self.angle+=degrees(angular_velocity)*dt
		self.distance+=self.velocity.x*dt

	def draw(self,win,dis):
		rotate=pygame.transform.rotate(self.img,self.angle)
		rect=rotate.get_rect()
		self.width=rect.width
		self.height=rect.height
		self.rad=int(max(self.width/2,self.height/2))
		self.center_points=self.position+(rect.width/2,rect.height/2)
		
		win.blit(rotate,self.position)
		pygame.draw.circle(win,(255,0,0),(int(self.position.x),int(self.position.y)),2)
		pygame.draw.circle(win,(255,255,255),(int(self.center_points.x),int(self.center_points.y)),int(max(self.width/2,self.height/2)))
		pygame.draw.circle(win,(0,0,255),(int(self.position.x+rect.width),int(self.position.y+rect.height)),2)
		#pygame.draw.rect(win,(255,0,0),((self.position.x-rect.width/2),(self.position.y-rect.height/2),rect.width,rect.height),2)
		pygame.draw.rect(win,(255,0,0),((self.position.x),(self.position.y),rect.width,rect.height),2)

		p=self.center_points.x
		q=self.center_points.y

		pygame.draw.line(win,(255,0,0),(p,q),(p+int(dis[2]*cos(radians(self.angle))),q-int(dis[2]*sin(radians(self.angle)))))

		pygame.draw.line(win,(255,0,0),(p,q),(p+int(dis[0]*cos(radians(self.angle-75))),q-int(dis[0]*sin(radians(self.angle-75)))))
		pygame.draw.line(win,(255,0,0),(p,q),(p+int(dis[1]*cos(radians(self.angle-30))),q-int(dis[1]*sin(radians(self.angle-30)))))
		
		pygame.draw.line(win,(255,0,0),(p,q),(p+int(dis[3]*cos(radians(self.angle+30))),q-int(dis[3]*sin(radians(self.angle+30)))))
		pygame.draw.line(win,(255,0,255),(p,q),(p+int(dis[4]*cos(radians(self.angle+75))),q-int(dis[4]*sin(radians(self.angle+75)))))

	def draws(self,win):
		rotate=pygame.transform.rotate(self.img,self.angle)
		rect=rotate.get_rect()
		self.width=rect.width
		self.height=rect.height
		self.rad=int(max(self.width/2,self.height/2))-2
		self.center_points=self.position+(rect.width/2,rect.height/2)
		#pygame.draw.circle(win,(255,255,255),(int(self.center_points.x),int(self.center_points.y)),int(max(self.width/2,self.height/2)))

		win.blit(rotate,self.position)
		'''angle=self.angle
		sine=[sin(radians(-angle+75)),sin(radians(-angle+30)),sin(radians(-angle)),sin(radians(-angle-30)),sin(radians(-angle-75))]
		cosine=[cos(radians(angle-75)),cos(radians(angle-30)),cos(radians(angle)),cos(radians(angle+30)),cos(radians(angle+75))]

		dx=[i*TILE_SIZE for i in cosine]
		dy=[i*TILE_SIZE for i in sine]

		for i in range(len(dx)):
			for  j in range(dis[i]):
				pygame.draw.circle(win,(255,255,255),(int(self.center_points.x+j*dx[i]),int(self.center_points.y+j*dy[i])),2)'''



	def controls(self,p,dt):
		##for moving forward and backward
		if p=='MOVE_FORWARD':
			if self.velocity.x<0:
				self.acceleration=self.brake_deceleration
			else:
				self.acceleration+=1*TILE_SIZE*dt

		elif p=='MOVE_BACKWARD':
			if self.velocity.x>0:
				self.acceleration=-self.brake_deceleration
			else:
				self.acceleration-=1*TILE_SIZE*dt

		else:
			if abs(self.velocity.x)>dt*self.brake_deceleration:
				self.acceleration=-copysign(self.brake_deceleration,self.velocity.x)
			else:
				if dt!=0:
					self.acceleration=-self.velocity.x/dt
			self.acceleration=0.0


		self.acceleration=max(-self.max_acceleration,min(self.acceleration,self.max_acceleration))
		##turning the car
	def turning(self,p,dt):
		if p=='RIGHT_TURN':
			self.steering-=30*dt
		elif p=='LEFT_TURN':
			self.steering+=30*dt
		else:
			self.steering=0

		self.steering=max(-self.max_steering,min(self.steering,self.max_steering))
		#print(self.steering,self.velocity.x,self.acceleration)
			





