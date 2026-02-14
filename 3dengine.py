try:
	import pygame
except:
	print("Try installing pygame community-edition (pygame-ce)")
import numpy as np
from math import radians,cos,sin,sqrt,ceil
import threading
import time



class Mesh:
	def __init__(self,points,color):
		self.points = points
		self.color = color
	def get_points(self):
		return self.points
	def get_color(self):
		return self.color
	def give_coordinates(self,coords):
		pass

class Rotating_Mesh:
	def __init__(self, points, color, X_rotation=0, Y_rotation=0, Z_rotation=0):
		self.points = points
		self.color = color
		self.X = X_rotation
		self.Y = Y_rotation
		self.Z = Z_rotation
		self.center = self.calculate_center()
		threading.Thread(target=self.apply_rotation, daemon=True).start()

	def calculate_center(self):
		"""Calcule le centre de l'objet"""
		if len(self.points[0]) == 0:
			return [0, 0, 0]
		x_sum = sum(p[0] for p in self.points[0])
		y_sum = sum(p[1] for p in self.points[0])
		z_sum = sum(p[2] for p in self.points[0])
		n = len(self.points[0])
		return [x_sum / n, y_sum / n, z_sum / n]

	def apply_rotation(self):
		while True:
			self.apply_X()
			self.apply_Y()
			self.apply_Z()
			time.sleep(0.02)

	def apply_Z(self):
		if self.Z != 0:
			m1 = np.array([[cos(self.Z), 0, -sin(self.Z)], [0, 1, 0], [sin(self.Z), 0, cos(self.Z)]])
			r = []
			for p in self.points[0]:
				# Translate vers l'origine
				p_translated = [p[0] - self.center[0], p[1] - self.center[1], p[2] - self.center[2]]
				# Applique la rotation
				rot = np.dot(m1, np.array([[p_translated[0]], [p_translated[1]], [p_translated[2]]]))
				# Translate retour au centre
				r.append((rot[0][0] + self.center[0], rot[1][0] + self.center[1], rot[2][0] + self.center[2]))
			self.points[0] = r
			# Recalcule le centre après rotation
			self.center = self.calculate_center()

	def apply_Y(self):
		if self.Y != 0:
			m1 = np.array([[cos(self.Y), -sin(self.Y), 0], [sin(self.Y), cos(self.Y), 0], [0, 0, 1]])
			r = []
			for p in self.points[0]:
				# Translate vers l'origine
				p_translated = [p[0] - self.center[0], p[1] - self.center[1], p[2] - self.center[2]]
				# Applique la rotation
				rot = np.dot(m1, np.array([[p_translated[0]], [p_translated[1]], [p_translated[2]]]))
				# Translate retour au centre
				r.append((rot[0][0] + self.center[0], rot[1][0] + self.center[1], rot[2][0] + self.center[2]))
			self.points[0] = r
			# Recalcule le centre après rotation
			self.center = self.calculate_center()

	def apply_X(self):
		if self.X != 0:
			m1 = np.array([[1, 0, 0], [0, cos(self.X), -sin(self.X)], [0, sin(self.X), cos(self.X)]])
			r = []
			for p in self.points[0]:
				# Translate vers l'origine
				p_translated = [p[0] - self.center[0], p[1] - self.center[1], p[2] - self.center[2]]
				# Applique la rotation
				rot = np.dot(m1, np.array([[p_translated[0]], [p_translated[1]], [p_translated[2]]]))
				# Translate retour au centre
				r.append((rot[0][0] + self.center[0], rot[1][0] + self.center[1], rot[2][0] + self.center[2]))
			self.points[0] = r
			# Recalcule le centre après rotation
			self.center = self.calculate_center()

	def get_points(self):
		return self.points

	def get_color(self):
		return self.color

	def give_coordinates(self, coords):
		pass
	def get_points(self):
		return self.points
	def get_color(self):
		return self.color
	def give_coordinates(self,coords):
		pass











class Simulation:
	def __init__(self,dimensions,meshs,Launcher = None):
		if not Launcher:
			pygame.init()
			self.__screen = pygame.display.set_mode(dimensions)
			self.__dimensions = dimensions
			self.__font = pygame.font.SysFont("consolas", 40)
			self.__font_color = (255,255,255)
		else:
			self.__screen = Launcher.screen
			self.__dimensions = Launcher.dimensions
			self.__font = Launcher.font
			self.__font_color = Launcher.font_color
		self.__meshs = meshs
		self.__end = False
		self.__caching = False
		self.__cached_points = {}
				 # z  x  y
		self.__camera = [0,0,5]
		self.__camera_rot = [radians(0), radians(0), radians(90)]
		self.__surface_screen = [self.__dimensions[0]/2, self.__dimensions[1]/2, 1000]
		self.__clock = pygame.time.Clock()
		pygame.event.set_grab(True)
		pygame.mouse.set_visible(False)
		threading.Thread(target=self.__console__,daemon=True).start()


		while not self.__end:
			self.__handle_inputs__()
			self.__render_meshs__(self.__meshs)
			self.__show_fps__()
			self.__give_coords__()
			self.__clock.tick(60)

			pygame.display.flip()
	def __console__(self):
		while not self.__end:
			cmd = input(">>>")
			try:
				if cmd.startswith("tp"):
					cmd = cmd[3:]
					x,y,z = cmd.split(" ")
					self.__camera = [float(x),float(y),float(z)]
			except Exception as e:
				print(e)



	def __give_coords__(self):
		for i in self.__meshs:
			i.give_coordinates([self.__camera,self.__camera_rot[1]])

	def __show_fps__(self):

		text = self.__font.render(str(round(self.__clock.get_fps()))+" FPS", True, self.__font_color)
		self.__screen.blit(text,(10,10))


	def __compute_projected_point__(self,point,camera,camera_rotation,surface):#see more here: https://en.wikipedia.org/wiki/3D_projection
		if (tuple(point),tuple(camera),tuple(camera_rotation)) in self.__cached_points and self.__caching:
			return self.__cached_points[(tuple(point),tuple(camera),tuple(camera_rotation))]
		else:
			projection_m1 = np.array([[1,0,0] ,[0,cos( camera_rotation[0] ),sin( camera_rotation[0] )] ,[0,-sin( camera_rotation[0] ),cos(camera_rotation[0])]])
			projection_m2 = np.array([[cos( camera_rotation[1] ),0, -sin( camera_rotation[1] )] ,[0,1,0] ,[sin( camera_rotation[1] ),0,cos( camera_rotation[1] )] ])
			projection_m3 = np.array([[cos( camera_rotation[2] ),sin( camera_rotation[2] ),0],[-sin( camera_rotation[2] ),cos( camera_rotation[2] ),0],[0,0,1]])
			projection_ma = np.array([[point[0]],[point[1]],[point[2]]])
			projection_mc = np.array([[camera[0]],[camera[1]],[camera[2]]])
			projection_ma_m_c = np.subtract(projection_ma,projection_mc)
			projection_d = np.dot(np.dot(np.dot(projection_m1,projection_m2),projection_m3),projection_ma_m_c)
			b = [0,0]
			b[0] = (surface[2] / projection_d[2]) * projection_d[0] + surface[0]
			b[1] = (surface[2] / projection_d[2]) * projection_d[1] + surface[1]
			self.__cached_points[(tuple(point),tuple(camera),tuple(camera_rotation))] = (b[0][0],b[1][0])
			return (b[0][0],b[1][0])

	def __render_meshs__(self,meshs):
		self.__uncomputed_point = []
		for k in meshs:
			points = []
			for point in k.get_points()[0]:
				points.append(point)
			self.__uncomputed_point.append(points)

		self.__computed_points = []
		for k in meshs:
			points = []
			for point in k.get_points()[0]:
				cp = self.__compute_projected_point__(point,self.__camera,self.__camera_rot,self.__surface_screen)
				points.append(cp)
			self.__computed_points.append(points)

		colored_polygons = []
		for n,mesh in enumerate(meshs):
			mesh_polygons = mesh.get_points()[1]
			color = mesh.get_color()
			for j in mesh_polygons:
				if self.__is_visible__(j,n):
					points = []
					for i in j:
						points.append(self.__computed_points[n][i])
					distance = self.__find_distance_from_cam__(j,n)
					colored_polygons.append((points,color,distance,self.__find_color__(j,n,distance)))
			colored_polygons.sort(key = lambda x:x[2],reverse = True)
		self.__screen.fill((0, 0, 0))

		for n,polygon in enumerate(colored_polygons):
			r,g,b = polygon[1]
			r = ceil(r* abs(polygon[3]))
			g = ceil(g* abs(polygon[3]))
			b = ceil(b* abs(polygon[3]))
			out = True
			for i in polygon[0]:
				if 0<i[0]<self.__dimensions[0] and 0<i[1]<self.__dimensions[1]:
					out = False
			if not out:
				try:
					pygame.draw.polygon(self.__screen, (r,g,b), polygon[0], width=0)
				except Exception as e:
					print(r,g,b)



	def __is_visible__(self, polygon, mesh):
		points = [self.__uncomputed_point[mesh][i] for i in polygon]
		x,y,z = self.__find_medium_coord__(polygon,mesh)
		x-=self.__camera[0]
		y-=self.__camera[1]
		z-=self.__camera[2]
		rotationm=np.array([[1, 0, 0],[0, cos(self.__camera_rot[1]+radians(90)), -sin(self.__camera_rot[1]+radians(90))],[0, sin(self.__camera_rot[1]+radians(90)),  cos(self.__camera_rot[1]+radians(90))]])
		relative_point=np.dot(rotationm,np.array([[x],[y],[z]]))

		return relative_point[1]>0


		return True
	def __find_color__(self,polygon,mesh,distance):
		if len(polygon)>2:
			points = []
			for i in polygon:
				points.append([self.__uncomputed_point[mesh][i][0],self.__uncomputed_point[mesh][i][1],self.__uncomputed_point[mesh][i][2]])

			u = [
			points[0][0]-points[1][0],
			points[0][1]-points[1][1],
			points[0][2]-points[1][2]

			]
			v = [
			points[0][0]-points[2][0],
			points[0][1]-points[2][1],
			points[0][2]-points[2][2]

			]

			normal = [u[1]*v[2]-u[2]*v[1],
				u[2]*v[0]-u[0]*v[2],
				u[0]*v[1]-u[1]*v[0]]


			norme_normal = sqrt(normal[0]**2+normal[1]**2+normal[2]**2)
			if norme_normal == 0:
				norme_normal = 0.1
			middle_point = self.__find_medium_coord__(polygon,mesh)
			normal = [normal[0]/norme_normal,

			normal[1]/norme_normal,
			normal[2]/norme_normal
				]
			cam_to_pol = [middle_point[0]-self.__camera[0],
						middle_point[1]-self.__camera[1],
						middle_point[2]-self.__camera[2]]
			norme_cam_to_pol = sqrt(cam_to_pol[0]**2+cam_to_pol[1]**2+cam_to_pol[2]**2)
			if norme_cam_to_pol==0:
				norme_cam_to_pol = 0.1
			cam_to_pol = [cam_to_pol[0]/norme_cam_to_pol,
			cam_to_pol[1]/norme_cam_to_pol,
			cam_to_pol[2]/norme_cam_to_pol
				]


			scalar = normal[0]*cam_to_pol[0]+normal[1]*cam_to_pol[1]+normal[2]*cam_to_pol[2]

			return scalar

	def __find_medium_coord__(self,polygon,mesh):
		x = 0
		y = 0
		z = 0


		for i in polygon:
			x+=self.__uncomputed_point[mesh][i][0]
			y+=self.__uncomputed_point[mesh][i][1]
			z+=self.__uncomputed_point[mesh][i][2]
		l = len(polygon)
		x = x/l
		y = y/l
		z = z/l
		return x,y,z

	def __find_distance_from_cam__(self,polygon,mesh):
		x,y,z = self.__find_medium_coord__(polygon,mesh)
		return sqrt((x-self.__camera[0])**2+(y-self.__camera[1])**2+(z-self.__camera[2])**2)

	def __handle_inputs__(self):
		dx,dy = 0,0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.__end = True
			elif event.type == pygame.MOUSEMOTION:
				dx, dy = event.rel
				x,y=pygame.mouse.get_pos()
				if not 10<x<self.__dimensions[0]-10 or not 10<y<self.__dimensions[1]-10:
					pygame.mouse.set_pos(self.__dimensions[0]//2, self.__dimensions[1]//2)



		pygame.event.get()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_c]:
			self.__end = True

		if keys[pygame.K_SPACE]:

			self.__camera[0] -= 0.9

		if keys[pygame.K_LSHIFT]:
			self.__camera[0] += 0.9

		if keys[pygame.K_d]:
			self.__camera[1] -= cos(self.__camera_rot[1])*0.9
			self.__camera[2] += sin(self.__camera_rot[1])*0.9
		if keys[pygame.K_q]:
			self.__camera[1] += cos(self.__camera_rot[1])*0.9
			self.__camera[2] -= sin(self.__camera_rot[1])*0.9
		if keys[pygame.K_z]:
			self.__camera[1] -= sin(self.__camera_rot[1])*0.9
			self.__camera[2] -= cos(self.__camera_rot[1])*0.9
		if keys[pygame.K_s]:
			self.__camera[1] += sin(self.__camera_rot[1])*0.9
			self.__camera[2] += cos(self.__camera_rot[1])*0.9

		if dy<0 and self.__camera_rot[0]<1.6:
			self.__camera_rot[0] += 0.04


		if dy>0 and -1.6<self.__camera_rot[0]:
			self.__camera_rot[0] -= 0.04


		if dx<0  :
			self.__camera_rot[1] -= 0.04
		if dx>0:
			self.__camera_rot[1] += 0.04




