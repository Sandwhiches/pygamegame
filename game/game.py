
import pygame
import math
import random
import time
from itertools import cycle

pygame.init()
# pygame.mixer.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Planes')

# setting clock
clock = pygame.time.Clock()

# colors:
colors = cycle(((0, 255, 0), (10, 255, 0), (20, 255, 0), (30, 255, 0), (40, 255, 0), (50, 255, 0), (60, 255, 0), (70, 255, 0), (80, 255, 0), (90, 255, 0), (100, 255, 0), (110, 255, 0), (120, 255, 0), (130, 255, 0), (140, 255, 0), (150, 255, 0), (160, 255, 0), (170, 255, 0), (180, 255, 0), (190, 255, 0), (200, 255, 0), (210, 255, 
0), (220, 255, 0), (230, 255, 0), (240, 255, 0), (250, 255, 0), (255, 255, 0), (255, 245, 0), (255, 235, 0), (255, 225, 0), (255, 215, 0), (255, 205, 0), (255, 195, 0), (255, 185, 0), (255, 175, 0), (255, 165, 0), (255, 155, 0), (255, 145, 0), (255, 135, 0), (255, 125, 0), (255, 115, 0), (255, 105, 0), (255, 95, 0), (255, 85, 0), (255, 75, 0), (255, 65, 0), (255, 55, 0), (255, 45, 0), (255, 35, 0), (255, 25, 0), (255, 15, 0), (255, 5, 0), (255, 0, 0), (255, 0, 10), (255, 0, 20), (255, 0, 30), (255, 0, 40), (255, 0, 50), (255, 0, 60), (255, 0, 70), (255, 0, 80), (255, 0, 90), (255, 0, 100), (255, 0, 110), (255, 0, 120), (255, 0, 130), (255, 0, 140), (255, 0, 150), (255, 0, 160), (255, 0, 170), (255, 0, 180), (255, 0, 190), (255, 0, 200), (255, 0, 210), (255, 0, 220), (255, 0, 230), (255, 0, 240), (255, 0, 250), (255, 0, 255), (245, 0, 255), (235, 0, 255), (225, 0, 255), (215, 0, 255), (205, 0, 255), (195, 0, 255), (185, 0, 255), (175, 
0, 255), (165, 0, 255), (155, 0, 255), (145, 0, 255), (135, 0, 255), (125, 0, 255), (115, 0, 255), (105, 0, 255), (95, 0, 255), (85, 0, 255), (75, 0, 255), (65, 0, 255), (55, 0, 255), (45, 0, 255), (35, 0, 255), (25, 0, 255), (15, 0, 255), (5, 0, 255), (0, 0, 255), (0, 10, 255), (0, 20, 255), (0, 30, 255), (0, 40, 
255), (0, 50, 255), (0, 60, 255), (0, 70, 255), (0, 80, 255), (0, 90, 255), (0, 100, 255), (0, 110, 255), (0, 120, 255), (0, 130, 255), (0, 140, 255), (0, 150, 255), (0, 160, 255), (0, 170, 255), (0, 180, 255), (0, 190, 255), (0, 200, 255), (0, 210, 255), (0, 220, 255), (0, 230, 255), (0, 240, 255), (0, 250, 255)))

# game configurations
straight = True
randomy = False
eavoid = False
oavoid = False
b_avoid = False
b_follow = False
pfollow = False
efollow = False
wallhax = False
yreflect = False
xreflect = False
deflect = False
phase = False
lines = True
short = True
drawobj = True
portal = False

class gameobject():
	def __init__(self, image, x, y, angle):
		self.ox = x
		self.oy = y
		self.x = x
		self.y = y
		self.image = image
		self.rotated_image = self.image
		self.ded = False
		self.angle = angle

	def rotateright(self ):
		self.angle -= 2
		self.angle %= 360

	def rotateleft(self ):
		self.angle += 2
		self.angle %= 360

	def setpos(self, diff):
		self.x += diff*(math.cos(math.radians(self.angle)))
		self.y -= diff*(math.sin(math.radians(self.angle)))

	def updategame(self ):
		if self.y <= dy[0] or self.y >= dy[1]:
			if self.y <= dy[0]:
				self.y = dy[1]
			else:
				self.y = dy[0]
		elif self.x <= dx[0] or self.x >= dx[1]:
			if self.x <= dx[0]:
				self.x = dx[1]
			else:
				self.x = dx[0]
		if self.ded == False and drawobj:
			self.rotated_image = pygame.transform.rotate(self.image, self.angle)
			screen.blit(self.rotated_image, (self.x - int(self.rotated_image.get_width()/2), self.y - int(self.rotated_image.get_height()/2)))
		elif drawobj and self.ded:
			self.ded = False
			self.x, self.y = self.ox, self.oy

# class bulletobject
class bulletobject():
	def __init__(self, image, enemy, origin, bulletspeed):
		self.image = image
		self.x = 0
		self.y = 0
		self.enemy = enemy
		self.origin = origin
		self.bulletspeed = bulletspeed
		self.xbulletspeed = bulletspeed
		self.angle = self.origin.angle
		self.ready = False


	def collisioncheck(self):
		# distance to self
		odistance = math.sqrt((math.pow(self.x - self.origin.x, 2)) + (math.pow(self.y - self.origin.y, 2)))
		# distance to enemy
		edistance = math.sqrt((math.pow(self.x - self.enemy.x, 2)) + (math.pow(self.y - self.enemy.y, 2)))
		# distance travelled by a bullet in one frame plus 40
		dist = abs(self.bulletspeed) + 70)*delta

		if len(ready) > 1 and (b_avoid or b_follow or deflect or lines):
			# distance to next bullet
			liveb1 = [(i.x , i.y) for i in ready if i != self]
			liveb2 = [math.sqrt((math.pow(self.x - i[0], 2)) + (math.pow(self.y - i[1], 2))) for i in liveb1]
			liveb4 = [i for i in ready if i!= self]

			if lines and short:
			# draws line btw closest bullet
				liveb3 = {i:j for i, j in zip(liveb2, liveb1)}
				x, y = liveb3[min(liveb2)]
				pygame.draw.line(screen, color, (self.x + 12.5, self.y + 12.5), (x + 12.5, y + 12.5))


			if b_avoid or b_follow or deflect or (lines and not short):
				for i, j, k in zip(liveb1, liveb2, liveb4):
					if lines and not short:
						pygame.draw.line(screen, color, (self.x + 12.5, self.y + 12.5), (i[0] + 12.5, i[1] + 12.5))
					if b_avoid:
					# avoiding other bullets
						if j <= 25:
							if self.x >= i[0]:
								self.x += dist
							else:
								self.x -= dist
							if self.y >= i[1]:
								self.y += dist
							else:
								self.y -= dist
					if b_follow:
					# bullets follow other bullets
						if j <= 18:
							if self.x >= i[0]:
								self.x -= dist
							else:
								self.x += dist
							if self.y >= i[1]:
								self.y -= dist
							else:
								self.y += dist
					if deflect:
						if j <= 25:
							# if self.x < i[0]:
							# 	if self.bulletspeed > 0:
							# 		self.xbulletspeed = -self.xbulletspeed
							# else:
							# 	if self.xbulletspeed < 0:
							# 		self.xbulletspeed = -self.xbulletspeed
							# if self.y < i[1]:
							# 	if self.bulletspeed > 0:
							# 		self.bulletspeed = -self.bulletspeed
							# else:
							# 	if self.bulletspeed < 0:
							# 		self.bulletspeed = -self.bulletspeed
							self.angle = abs(self.angle - k.angle)

		if yreflect:
			# bullets reflect at y boundary
			if self.y - 5 <= yr[0]:
				self.bulletspeed = -self.bulletspeed
			elif self.y + 5 >= yr[1] :
				self.bulletspeed = -self.bulletspeed

		if xreflect:
			# bullets reflect at x boundary
			if self.x - 5 <= xr[0]:
				self.xbulletspeed = -self.xbulletspeed
			elif self.x + 5 >= xr[1]:
				self.xbulletspeed = -self.xbulletspeed

		if eavoid:
			# enemy avoiding behavior
			if edistance <= 50:
				if deflect:
					# delfects outside enemy barrier
					if self.x < self.enemy.x:
						if self.bulletspeed > 0:
							self.xbulletspeed = -self.xbulletspeed
					else:
						if self.xbulletspeed < 0:
							self.xbulletspeed = -self.xbulletspeed
					if self.y < self.enemy.y:
						if self.bulletspeed > 0:
							self.bulletspeed = -self.bulletspeed
					else:
						if self.bulletspeed < 0:
							self.bulletspeed = -self.bulletspeed

				if self.x >= self.enemy.x:
					self.x += dist
				else:
					self.x -= dist
				if self.y >= self.enemy.y:
					self.y += dist
				else:
					self.y -= dist

		if oavoid:
			# origin avoiding behavior
			if odistance < 50:
				if deflect or xreflect or yreflect:
					# delfects outside barrier
					if self.x < self.origin.x:
						if self.bulletspeed > 0:
							self.xbulletspeed = -self.xbulletspeed
					else:
						if self.xbulletspeed < 0:
							self.xbulletspeed = -self.xbulletspeed
					if self.y < self.origin.y:
						if self.bulletspeed > 0:
							self.bulletspeed = -self.bulletspeed
					else:
						if self.bulletspeed < 0:
							self.bulletspeed = -self.bulletspeed

				if self.x >= self.origin.x:
					self.x += dist
				else:
					self.x -= dist
				if self.y >= self.origin.y:
					self.y += dist
				else:
					self.y -= dist

		if efollow:
			# enemy following behavior
			if edistance >= 90:
				if deflect or xreflect or yreflect:
					# delfects within barrier
					if self.x > self.enemy.x and self.xbulletspeed > 0:
						self.xbulletspeed = -self.xbulletspeed
					elif self.x < self.enemy.x and self.xbulletspeed < 0:
						self.xbulletspeed = -self.xbulletspeed
					if self.y > self.enemy.y and self.bulletspeed > 0:
						self.bulletspeed = -self.bulletspeed
					elif self.y < self.enemy.y and self.bulletspeed < 0:
						self.bulletspeed = -self.bulletspeed
			
				if self.x > self.enemy.x:
					self.x -= dist
				elif self.enemy.x < self.x:
					self.x += dist
				if self.y > self.enemy.y:
					self.y -= dist
				elif self.enemy.y < self.y:
					self.y += dist

		if pfollow:
			# player following behavior
			if odistance >= 90:
				if deflect or xreflect or yreflect:
					# deflects within barrier
					if self.x > self.origin.x and self.xbulletspeed > 0:
						self.xbulletspeed = -self.xbulletspeed
					elif self.x < self.origin.x and self.xbulletspeed < 0:
						self.xbulletspeed = -self.xbulletspeed
					if self.y > self.origin.y and self.bulletspeed > 0:
						self.bulletspeed = -self.bulletspeed
					elif self.y < self.origin.y and self.bulletspeed < 0:
						self.bulletspeed = -self.bulletspeed
				if self.x > self.origin.x:		
					self.x -= dist
				elif self.x < self.origin.x:
					self.x += dist
				if self.y > self.origin.y:
					self.y -= dist
				elif self.y < self.origin.y:
					self.y += dist
		if wallhax:
			# prevents bullets going past edge
			if self.y <= yr[0] - 3 or self.y >= yr[1] + 3:
				if self.y <= yr[0] - 3:
					self.y += dist + 3
				else:
					self.y -= dist + 3
			elif self.x <= xr[0] - 3 or self.x >= xr[1] + 3:
				if self.x <= xr[0] - 3:
					self.x += dist + 3
				else:
					self.x -= dist + 3
		if phase == False: 
			# deletes bullet and ship
			if edistance <= 10:
				self.ready = False
				self.enemy.ded = True
				score()
				ready.remove(self)

	def setstart(self, x, y):
		self.x = x - int(self.origin.rotated_image.get_width()/2)
		self.y = y - int(self.origin.rotated_image.get_height()/2)
		self.ready = True

	def fire(self):
		if portal:
			# moves to opposite edge
			if self.y <= dy[0] or self.y >= dy[1]:
				if self.y <= dy[0]:
					self.y = dy[1]
				else:
					self.y = dy[0]
			elif self.x <= dx[0] or self.x >= dx[1]:
				if self.x <= dx[0]:
					self.x = dx[1]
				else:
					self.x = dx[0]
		else:
			# deletes bullet at edges
			if self.y <= dy[0] or self.y >= dy[1]:
				self.ready = False
				ready.remove(self)
			elif self.x <= dx[0] or self.x >= dx[1]:
				self.ready = False
				ready.remove(self)

		if straight:
			# staight line
			self.y += self.bulletspeed*delta*(math.sin(math.radians(self.angle)))
			self.x -= self.xbulletspeed*delta*(math.cos(math.radians(self.angle)))
		if randomy:
			# random direction
			self.x += random.randint(- 3, 3)
			self.y -= random.randint(- 3, 3)

		self.collisioncheck()

		if drawobj:
			screen.blit( self.image, (self.x, self.y))




yellow = pygame.transform.scale(pygame.image.load('paper-plane.png'), (25, 25))
purple = pygame.transform.scale(pygame.image.load('paper-plane - Copy.png'), (25, 25))

# plane
player = gameobject(yellow, 375, 485, angle = 270)
# enemy plane
enemy = gameobject(purple, 375, 115, angle = 90)



# setting parameters for all bullets going to be created
sx = 25
sy = 25

im2 = pygame.transform.scale(pygame.image.load('rec.png'), (sx, sy))

im1 = pygame.transform.scale(pygame.image.load('rec - Copy.png'), (sx, sy))
xr = (0, 775)
yr = (0, 575)
dx = (-30, 815)
dy = (-30, 615)

bs = 150

# formatting configuration menu
def multlines(text, configs, fontsize):
	text = text.replace('True', 'ON').replace('False', 'OFF').splitlines()
	for i, j in enumerate(text):
		if j[-1] == 'N':
			screen.blit(configs.render(j, True, (128,255,102)), (0, fontsize*i))
		else:
			screen.blit(configs.render(j, True, (255, 255, 120)), (0, fontsize*i))

def update():
	global ppoint, epoint, scoreswitch
	if pyupdate:
		# drawing backround
		screen.fill((30, 20, 30))

	# # draws scoreboard, configs
	if scoreswitch:
		stat = status.render(f'                           YELLOW: {ppoint}   PURPLE: {epoint}', True, (255 , 50, 225))
		screen.blit( stat, (0, 0))
	if configuration:
		multlines(text, configs, 12)
	# bullets getting fired
	for i in ready:
		i.fire()
	# update player,enemy position
	player.updategame()
	enemy.updategame()
	# creates frame in window
	pygame.display.update()

# updates scoreboard
def score():
	global ppoint, epoint
	if player.ded == True:
		epoint += 1
	else:
		ppoint += 1


def checksign(check):
	if check > 0:
		return 1
	else:
		return -1

status = pygame.font.Font('freesansbold.ttf',32)
configs = pygame.font.Font('freesansbold.ttf',12)

pyupdate = True
scoreswitch = True
configuration = True
sound = False
ready = []

# points
ppoint = 0
epoint = 0

run = True
epress = True
ppress = True
configcheck = True
count = 1
while run:
	# returns each event in keyboard
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			continue
		
	# updating delta value and setting frame rate
	delta = clock.tick(60)/1000
	# updating game configs 
	text = f'[1]straight: {straight}\n[2]random: {randomy}\n[3]enemyavoid: {eavoid}\n[4]playersavoid: {oavoid}\n[5]bulletavoid: {b_avoid}\n[6]bulletfollow: {b_follow}\n[7]enemyfollow: {efollow}\n[8]playerfollow: {pfollow}\n[9]wallborder {wallhax}\n[0]yreflect: {yreflect}\n[F1]xreflect: {xreflect}\n[F2]deflectbullets: {deflect}\n[F3]phasebullets: {phase}\n[F4]/[i]short, lines: {short} {lines}\n[F5]drawobjs: {drawobj}\n[F6]portal: {portal}\n[F7]updatesc: {pyupdate}\n[F8]scoreboard: {scoreswitch}\n[F9]configs: {configuration}\n[F10]soundeffect: {sound}\n[\]exit\n[-]/[+]bulletspd: {round(bs, 1)}\nfps: {round(clock.get_fps(), 2)}, delta: {delta}\nx, y : {int(player.x)}, {int(player.y)}\nlivebullets: {len(ready)}\nangle: {player.angle}'
	# updating color
	if count % 2 == 0:
		color = next(colors)
	count += 1
	# controlling ships
	keys = pygame.key.get_pressed()

	# allows keypresses 1 - K12 to change game settings
	if configcheck:
		if keys[pygame.K_i]:
			short = not short
			configcheck = False

		elif keys[pygame.K_1]:
			straight = not straight
			configcheck = False

		elif keys[pygame.K_2]:
			randomy = not randomy
			configcheck = False

		elif keys[pygame.K_3]:
			eavoid = not eavoid
			configcheck = False

		elif keys[pygame.K_4]:
			oavoid = not oavoid
			configcheck = False

		elif  keys[pygame.K_5]:
			b_avoid = not b_avoid
			configcheck = False

		elif  keys[pygame.K_6]:
			b_follow = not b_follow
			configcheck = False

		elif keys[pygame.K_7]:
			efollow = not efollow
			configcheck = False

		elif keys[pygame.K_8]:
			pfollow = not pfollow
			configcheck = False

		elif keys[pygame.K_9]:
			wallhax = not wallhax
			configcheck = False

		elif keys[pygame.K_0]:
			yreflect = not yreflect
			configcheck = False	

		elif keys[pygame.K_F1]:
			xreflect = not xreflect
			configcheck = False	
		
		elif keys[pygame.K_F2]:
			deflect = not deflect
			configcheck = False

		elif keys[pygame.K_F3]:
			phase = not phase
			configcheck = False	

		elif keys[pygame.K_F4]:
			lines = not lines
			configcheck = False

		elif keys[pygame.K_F5]:
			drawobj = not drawobj
			configcheck = False
	
		elif keys[pygame.K_F6]:
			portal = not portal
			configcheck = False
		
		elif keys[pygame.K_F7]:
			pyupdate = not pyupdate
			configcheck = False
		
		elif keys[pygame.K_F8]:
			scoreswitch = not scoreswitch
			configcheck = False

		elif keys[pygame.K_F9]:
			configuration =  not configuration
			configcheck = False

		elif keys[pygame.K_F10]:
			sound = not sound
			configcheck = False
		
		elif keys[pygame.K_MINUS]:
			bs -= 1
			configcheck = False

		elif keys[pygame.K_EQUALS]:
			bs += 1
			configcheck = False

		elif keys[pygame.K_BACKSLASH]:
			run = False
			continue


	# enemy ship - WASD, player ship - arrow keys
	if  keys[pygame.K_w]:
		enemy.setpos(-150*delta)

	if keys[pygame.K_a]:
		enemy.rotateleft()
	
	if keys[pygame.K_s]:
		enemy.setpos(150*delta)

	if keys[pygame.K_d]:
		enemy.rotateright()

	if  keys[pygame.K_UP]:
		player.setpos(-150*delta)

	if keys[pygame.K_LEFT]:
		player.rotateleft()

	if keys[pygame.K_DOWN]:
		player.setpos(150*delta)

	if keys[pygame.K_RIGHT]:
		player.rotateright()

	# controlling bullets: enemy ship - LEFT SHIFT, player ship - RIGHT SHIFT
	if keys[pygame.K_RSHIFT] and ppress == True:
		if sound:
			pygame.mixer.music.load('muda.mp3')
			pygame.mixer.music.play()
		bulletp = bulletobject(im1,enemy = enemy, origin = player, bulletspeed = bs)
		bulletp.setstart(player.x, player.y)
		ready.append(bulletp)
		ppress = False
	if keys[pygame.K_LSHIFT] and epress == True:
		if sound:
			pygame.mixer.music.load('ora.mp3')
			pygame.mixer.music.play()		
		bullete = bulletobject(im2,enemy = player, origin = enemy, bulletspeed = bs)
		bullete.setstart(enemy.x, enemy.y)
		ready.append(bullete)
		epress = False

	# activate on release
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RSHIFT:
			ppress = True
			configcheck = True
		elif event.key == pygame.K_LSHIFT:
			epress = True
		elif configcheck == False and event.key in [pygame.K_x, pygame.K_i, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_MINUS, pygame.K_EQUALS, pygame.K_BACKSLASH]:
			configcheck = True

	update()






