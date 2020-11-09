
import pygame
import math
import random
import time
from itertools import cycle

pygame.init()
# pygame.mixer.init()



screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Planes')


# clock = pygame.time.Clock()


class gameobject():

	def __init__(self, image, sx, sy, x, y, boundary, reverse):

		self.image = pygame.transform.scale(pygame.image.load(image), (sx, sy))
		self.ox = x
		self.oy = y
		self.x = x
		self.y = y
		self.bx1 = boundary[0][0]
		self.bx2 = boundary[0][1]
		self.by1 = boundary[1][0]
		self.by2 = boundary[1][1]	
		self.straight = True
		self.random = False
		self.eavoid = False
		self.oavoid = False
		self.b_avoid = False
		self.b_follow = False
		self.pfollow = False
		self.efollow = False
		self.wallhax = False
		self.yreflect = False
		self.xreflect = False
		self.deflect = False
		self.phase = False
		self.ded = False
		self.orientation = reverse
		self.reverse = reverse

	def rotate180(self):
		self.image = pygame.transform.flip(self.image, False, True)
		if self.reverse:
			self.reverse = False
		else:
			self.reverse = True


	def setpos(self, choose, diff):
		if choose == 0:
			if diff < 0:
				if int(self.x) == self.bx1:
					return
			else:
				if int(self.x) == self.bx2:
					return
			self.x += diff

		else:
			if diff < 0:
				if int(self.y) == self.by1:
					return
			else:
				if int(self.y) == self.by2:
					return
			if int(self.y) == 300:
				self.rotate180()
			self.y += diff

	def updategame(self ):
		if self.ded == False:
			screen.blit(self.image, (self.x, self.y))
		else:
			if self.reverse != self.orientation:
				self.rotate180()
			self.ded = False
			self.x, self.y = self.ox, self.oy

# class bulletobject
class bulletobject():
	def __init__(self, image, sx, sy, b_range, enemy, origin, bulletspeed):
		self.image = pygame.transform.scale(pygame.image.load(image), (sx, sy))
		self.xr = b_range[1]
		self.yr = b_range[0]
		self.x = 0
		self.y = 0
		self.enemy = enemy
		self.origin = origin
		self.sbulletspeed = bulletspeed
		self.bulletspeed = bulletspeed
		self.xbulletspeed = -bulletspeed
		self.ready = False


	def collisioncheck(self):
		# distance to self
		odistance = math.sqrt((math.pow(self.x - self.origin.x, 2)) + (math.pow(self.y - self.origin.y, 2)))
		# distance to enemy
		edistance = math.sqrt((math.pow(self.x - self.enemy.x, 2)) + (math.pow(self.y - self.enemy.y, 2)))

		if self.origin.b_avoid or self.origin.b_follow or self.origin.deflect:
			# distance to next bullet
			liveb1 = [(i.x, i.y) for i in ready ]
			liveb2 = [math.sqrt((math.pow(self.x - i[0], 2)) + (math.pow(self.y - i[1], 2))) for i in liveb1]
			for i, j in zip(liveb1, liveb2):
				if j == 0:
					continue
				if self.origin.b_avoid:
				# avoiding other bullets
					if j <= 25:
						if self.x >= i[0]:
							self.x += 1 + round(random.random()*3, 2)
						else:
							self.x -= 1 - round(random.random()*3, 2)
						if self.y >= i[1]:
							self.y += 1 + round(random.random()*3, 2)
						else:
							self.y -= 1 - round(random.random()*3, 2)

				if self.origin.b_follow:
				# bullets follow other bullets
					if j <= 18:
						if self.x >= i[0]:
							self.x -= 1
						else:
							self.x += 1
						if self.y >= i[1]:
							self.y -= 1
						else:
							self.y += 1
				if self.origin.deflect:
					if j <= 25:
						if self.x < i[0]:
							if self.bulletspeed > 0:
								self.xbulletspeed = -self.xbulletspeed
						else:
							if self.xbulletspeed < 0:
								self.xbulletspeed = -self.xbulletspeed
						if self.y < i[1]:
							if self.bulletspeed > 0:
								self.bulletspeed = -self.bulletspeed
						else:
							if self.bulletspeed < 0:
								self.bulletspeed = -self.bulletspeed

		if self.origin.wallhax:
			# wall avoiding behavior
			if (self.x) - 4 <= self.xr[0]:
				self.x += 4
			elif (self.x) + 4 >= self.xr[1]:
				self.x -= 4
			if (self.y) - 4 <= self.yr[0]:
				self.y += 4
			elif (self.y) + 4 >= self.yr[1] :
				self.y -= 4

		if self.origin.yreflect:
			# bullets reflect at y boundary
			if self.y - 5 <= self.yr[0]:
				self.bulletspeed = -self.bulletspeed
			elif self.y + 5 >= self.yr[1] :
				self.bulletspeed = -self.bulletspeed

		if self.origin.xreflect:
			# bullets reflect at x boundary
			if self.x - 5 <= self.xr[0]:
				self.xbulletspeed = -self.xbulletspeed
			elif self.x + 5 >= self.xr[1]:
				self.xbulletspeed = -self.xbulletspeed

		if self.origin.eavoid:
			# enemy avoiding behavior
			if edistance <= 50:
				if self.origin.deflect:
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
					self.x += 1
				else:
					self.x -= 1
				if self.y >= self.enemy.y:
					self.y += 1
				else:
					self.y -= 1

		if self.origin.oavoid:
			# origin avoiding behavior
			if odistance < 50:
				if self.origin.deflect:
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
					self.x += 1
				else:
					self.x -= 1
				if self.y >= self.origin.y:
					self.y += 1
				else:
					self.y -= 1

		if self.origin.efollow:
			# enemy following behavior
			if edistance >= 90:
				if self.origin.deflect:
					# delfects within barrier
					if self.x >= self.enemy.x and self.xbulletspeed < 0:
						self.x += 1
						self.xbulletspeed = -self.xbulletspeed
					elif self.x <= self.enemy.x and self.xbulletspeed > 0:
						self.x -= 1
						self.xbulletspeed = -self.xbulletspeed
					if self.y >= self.enemy.y and self.bulletspeed < 0:
						self.y -= 1
						self.bulletspeed = -self.bulletspeed
					elif self.y <= self.enemy.y and self.bulletspeed > 0:
						self.y += 1	
						self.bulletspeed = -self.bulletspeed
			
				if self.x >= self.enemy.x:
					self.x -= 1
				else:
					self.x += 1
				if self.y >= self.enemy.y:
					self.y -= 1
				else:
					self.y += 1

		if self.origin.pfollow:
			# player following behavior
			if odistance >= 90:
				if self.origin.deflect:
					# deflects within barrier
					if self.x >= self.origin.x and self.xbulletspeed > 0:
						self.x -= 1
						self.xbulletspeed = -self.xbulletspeed
					elif self.x <= self.origin.x and self.xbulletspeed < 0:
						self.x += 1
						self.xbulletspeed = -self.xbulletspeed
					if self.y >= self.origin.y and self.bulletspeed > 0:
						self.y -= 1
						self.bulletspeed = -self.bulletspeed
					elif self.y <= self.origin.y and self.bulletspeed < 0:
						self.y += 1	
						self.bulletspeed = -self.bulletspeed

				if self.x >= self.origin.x:		
					self.x -= 1
				else:
					self.x += 1
				if self.y >= self.origin.y:
					self.y -= 1
				else:
					self.y += 1
		# deletes bullet and ship
		if self.origin.phase == False: 
			if edistance <= 10:
				self.ready = False
				self.enemy.ded = True
				self.bulletspeed = self.sbulletspeed
				score()
				ready.remove(self)

	def setstart(self, x, y):
		self.x = x
		self.y = y
		self.ready = True

	def fire(self):
		if self.y <= self.yr[0] or self.y >= self.yr[1]:
			self.ready = False
			self.bulletspeed = self.sbulletspeed
			ready.remove(self)
		elif self.x <= self.xr[0] or self.x >= self.xr[1]:
			self.ready = False
			self.bulletspeed = self.sbulletspeed
			ready.remove(self)
		screen.blit( self.image, (self.x, self.y))

		if self.origin.straight:
			# staight line
			self.y += self.bulletspeed
			if self.origin.xreflect:
				# just to see how it would move
				# self.x += changesign((self.xbulletspeed + math.sqrt((math.pow(self.bulletspeed, 2)))), checksign(self.xbulletspeed))
				self.x += self.xbulletspeed

		if self.origin.random:
			# random
			self.x = random.randint(- 3, 3) + self.x
			self.y = random.randint(- 3, 3) + self.y

		self.collisioncheck()

# plane
player = gameobject('paper-plane.png', 25, 25, 375, 485, ((0, 775), (0, 575)), True)
# enemy plane
enemy = gameobject('paper-plane - Copy.png', 25, 25, 375, 115, ((0, 775), (0, 575)), False)



im2 = 'rec.png'
im1 = 'rec - Copy.png'

sx = 25
sy = 25

xr = (0, 585)
yr = (0, 785)

bs = .5 
# bullet
b1 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b2 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b3 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b4 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b5 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b6 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b7 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b8 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b9 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b10 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b11 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b12 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b10 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b11 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b12 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b13 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b14 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
b15 = bulletobject(im1,sx, sy, b_range = (xr, yr), enemy = enemy, origin = player, bulletspeed = -bs)
mag = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15]
magazine = cycle([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15])

eb1 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb2 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb3 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb4 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb5 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb6 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb7 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb8 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb9 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb10 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb11 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb12 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb10 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb11 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb12 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb13 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb14 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
eb15 = bulletobject(im2,sx, sy, b_range = (xr, yr), enemy = player, origin = enemy, bulletspeed = bs)
emag = [eb1, eb2, eb3, eb4, eb5, eb6, eb7, eb8, eb9, eb10, eb11, eb12, eb13, eb14, eb15]
emagazine = cycle([eb1, eb2, eb3, eb4, eb5, eb6, eb7, eb8, eb9, eb10, eb11, eb12, eb13, eb14, eb15])






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

	# draws scoreboard, configs
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

def score():
	global ppoint, epoint
	if player.ded == True:
		epoint += 1
	else:
		ppoint += 1

def changesign(check, val):
	if check:
		if val < 0:
			pass
		else:
			val = -val
	else:
		if val > 0:
			pass
		else:
			val = -val
	return val

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

# point
ppoint = 0
epoint = 0

run = True
epress = True
ppress = True
configcheck = True
while run:
	# returns each event in keyboard
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			continue

	# updating game configs 
	text = f'[1]straight: {player.straight}\n[2]random: {player.random}\n[3]enemyavoid: {player.eavoid}\n[4]playeravoid: {player.oavoid}\n[5]bulletavoid: {player.b_avoid}\n[6]bulletfollow: {player.b_follow}\n[7]enemyfollow: {player.efollow}\n[8]playerfollow: {player.pfollow}\n[9]wallborder {player.wallhax}\n[0]yreflect: {player.yreflect}\n[F1]xreflect: {player.xreflect}\n[F2]deflectbullets: {player.deflect}\n[F3]phasebullets: {player.phase}\n[F4]updatesc: {pyupdate}\n[F5]scoreboard: {scoreswitch}\n[F6]configs: {configuration}\n[F7]soundeffect: {sound}\n[F8]exit game\n[F9/F10]bulletspd: {round(b1.sbulletspeed, 1)}pix/frm'
	
	# controlling ships
	keys = pygame.key.get_pressed()

	if configcheck:
		if keys[pygame.K_1]:
			if player.straight:
				player.straight = False
				enemy.straight = False
			else:
				player.straight = True
				enemy.straight = True
			configcheck = False

		elif keys[pygame.K_2]:
			if player.random:
				player.random = False
				enemy.random = False
			else:
				player.random = True
				enemy.random = True
			configcheck = False

		elif keys[pygame.K_3]:
			if player.eavoid:
				player.eavoid = False
				enemy.eavoid = False
			else:
				player.eavoid = True
				enemy.eavoid = True
			configcheck = False

		elif keys[pygame.K_4]:
			if player.oavoid:
				player.oavoid = False
				enemy.oavoid = False
			else:
				player.oavoid = True
				enemy.oavoid = True
			configcheck = False

		elif  keys[pygame.K_5]:
			if player.b_avoid:
				player.b_avoid = False
				enemy.b_avoid = False
			else:
				player.b_avoid = True
				enemy.b_avoid = True
			configcheck = False

		elif  keys[pygame.K_6]:
			if player.b_follow:
				player.b_follow = False
				enemy.b_follow = False
			else:
				player.b_follow = True
				enemy.b_follow = True
			configcheck = False

		elif keys[pygame.K_7]:
			if player.efollow:
				player.efollow = False
				enemy.efollow = False
			else:
				player.efollow = True
				enemy.efollow = True
			configcheck = False

		elif keys[pygame.K_8]:
			if player.pfollow:
				player.pfollow = False
				enemy.pfollow = False
			else:
				player.pfollow = True
				enemy.pfollow = True
			configcheck = False

		elif keys[pygame.K_9]:
			if player.wallhax:
				player.wallhax = False
				enemy.wallhax = False
			else:
				player.wallhax = True
				enemy.wallhax = True
			configcheck = False

		elif keys[pygame.K_0]:
			if player.yreflect:
				player.yreflect = False
				enemy.yreflect = False
			else:
				player.yreflect = True
				enemy.yreflect = True
			configcheck = False	

		elif keys[pygame.K_F1]:
			if player.xreflect:
				player.xreflect = False
				enemy.xreflect = False
			else:
				player.xreflect = True
				enemy.xreflect = True
			configcheck = False	
		
		elif keys[pygame.K_F2]:
			if player.deflect:
				player.deflect = False
				enemy.deflect = False
			else:
				player.deflect = True
				enemy.deflect = True
			configcheck = False

		elif keys[pygame.K_F3]:
			if player.phase:
				player.phase = False
				enemy.phase = False
			else:
				player.phase = True
				enemy.phase = True
			configcheck = False	

		elif keys[pygame.K_F4]:
			if pyupdate:
				pyupdate = False
			else:
				pyupdate = True
			configcheck = False

		elif keys[pygame.K_F5]:
			if scoreswitch:
				scoreswitch = False
			else:
				scoreswitch = True	
			configcheck = False
	
		elif keys[pygame.K_F6]:
			if configuration:
				configuration = False
			else:
				configuration = True	
			configcheck = False
		
		elif keys[pygame.K_F7]:
			if sound == False:
				sound = True
			else:
				sound = False

			configcheck = False
		
		elif keys[pygame.K_F8]:
			run = False
			continue

		elif keys[pygame.K_F9]:
			for i, j in zip(mag, emag):
				i.bulletspeed -= .1
				j.bulletspeed += .1
				i.sbulletspeed -= .1
				j.sbulletspeed += .1
			configcheck = False
		elif keys[pygame.K_F10]:
			for i, j in zip(mag, emag):
				i.bulletspeed += .1
				j.bulletspeed -= .1
				i.sbulletspeed += .1
				j.sbulletspeed -= .1
			configcheck = False

	
	if  keys[pygame.K_w]:
		enemy.setpos(1, -.3)

	if keys[pygame.K_a]:
		enemy.setpos(0, -.3)

	if keys[pygame.K_s]:
		enemy.setpos(1, .3)

	if keys[pygame.K_d]:
		enemy.setpos(0, .3)

	if  keys[pygame.K_UP]:
		player.setpos(1, -.3)

	if keys[pygame.K_LEFT]:
		player.setpos(0, -.3)

	if keys[pygame.K_DOWN]:
		player.setpos(1, .3)

	if keys[pygame.K_RIGHT]:
		player.setpos(0, .3)

	# controlling bullets
	if keys[pygame.K_RSHIFT] and ppress == True:
		if sound:
			pygame.mixer.music.load('muda.mp3')
			pygame.mixer.music.play()
		bulletp = next(magazine)
		if bulletp.ready == False:
			bulletp.bulletspeed = changesign(player.reverse, bulletp.bulletspeed)
			bulletp.setstart(player.x, player.y)
			ready.append(bulletp)
			ppress = False
	if keys[pygame.K_LSHIFT] and epress == True:
		if sound:
			pygame.mixer.music.load('ora.mp3')
			pygame.mixer.music.play()		
		bullete = next(emagazine)
		if bullete.ready == False:
			bullete.bulletspeed = changesign(enemy.reverse, bullete.bulletspeed)
			bullete.setstart(enemy.x, enemy.y)
			ready.append(bullete)
			epress = False

	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RSHIFT:
			ppress = True
			configcheck = True
		elif event.key == pygame.K_LSHIFT:
			epress = True
		elif configcheck == False and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10]:
			configcheck = True

	update()






