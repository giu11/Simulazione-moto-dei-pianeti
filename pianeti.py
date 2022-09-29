import pygame
import math
pygame.init()

WIDTH, HEIGHT =  800, 800 #Costanti per grandezza schermo
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Mostra a schermo io gioco della larghezza desiderata 
pygame.display.set_caption("Simulazione pianeti")#Titolo

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
	AU = 149.6e6 * 1000 #Unità astronomiche sono la distanza tra la Terra e il sole in metri 
	G = 6.67428e-11
	SCALE = 250 / AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 giorno

	def __init__(self, x, y, radius, color, mass): #Parametri per ogni pianeta 
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = [] #Punti dell'orbita per disegnarla
		self.sun = False #if pianeta is sun
		self.distance_to_sun = 0

		self.x_vel = 0 #Per muovere nel cerchio abbiamo vel x e vely
		self.y_vel = 0

	def draw(self, win): #Disegna i pianeti
		x = self.x * self.SCALE + WIDTH / 2 # Per rcentrali perchè in basso a sinistra(800,800)
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit: #per disegnare orbita 
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2) #comando per disegnare linee

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		if not self.sun: #Far edere la distanza dal sole 
			distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2)) #Per posizionare il testo

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2 #Forza di attrazione gravitazionalke
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force #Forza x
		force_y = math.sin(theta) * force #Forza y
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0 
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP # F = ma a = F/M v/t = F/M v = F/m+t-> day 
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP 
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y)) # Punti per diesganre l'orbita che vanno nell'init 


def main():
	run = True
	clock = pygame.time.Clock()#Stesa vel su tutti i pc 

	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) #Creiamo tutti i pianeti
	sun.sun = True

	earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
	earth.y_vel = 29.783 * 1000 # Velocità y per farli muovere in traiettoria circolare

	mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000 #km/s -> m/s

	mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000 #Negativi per direzione

	venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000

	planets = [sun, earth, mars, mercury, venus] #lista con i pianeti

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0)) #Schermo nero in RGB

		for event in pygame.event.get(): #Itera nella lista degli eventi
			if event.type == pygame.QUIT: # Se chiude allora stop
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()
