

# assumptions:
	# units in are inches and outputted in meters
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pdb

class FarField:

 	def __init__(self, FileLocation):
 		self.loc = FileLocation
 		self.raw = (genfromtxt(self.loc, delimiter=',', skip_header=9, dtype=float))
 		self.degIncrement = 22.5 
 		self.coordinates = self.raw[:, 0:3]


 	def cart2rad(self, coord):
 		# assumes data in the form x, y, z, with y being the axial (azimuthal) direction
  		[m,n] = shape(coord)
 		R = (zeros((m,1)))
 		azimuthal = (zeros((m,1)))
 		polar = (zeros((m,1)))
 		#hackery to get coord[:,2] to an array with some length 
 		XX = zeros((m,1))
 		XX[:,0] = coord[:,2]

 		R[:, 0] = ( coord[:,0] ** 2 + coord[:,1] ** 2 + coord[:,2] ** 2)** .5
 		azimuthal[:, 0] = (arctan(coord[:,1] / coord[:, 0]))

 		polar = (arccos(XX / R))

 		return R, polar, azimuthal


 	def d2r(self, deg):
 		#convert degress to radians
 		rad = deg * (pi/ 180)
 		return rad


 	def expandGrid(self, degIncrement):
 		# assume revolution around the y axis 
 		tol = 1e-8
 		[m, n] = shape(self.coordinates)

 		x = zeros((m, 1))
 		y = zeros((m, 1))
 		z = zeros((m, 1))

 		x[:, 0] = abs( self.coordinates[:, 0] )
 		y[:, 0] = abs( self.coordinates[:, 1] ) 
 		z[:, 0] = abs( self.coordinates[:, 2] ) 

 		# redefine coordinates for convention
 		
 		xd = zeros((m, 1))
 		yd = zeros((m, 1))
 		zd = zeros((m, 1))

 		xd = z
 		yd = x
 		zd = y 

 		# convert inches to meters
 		xd = xd * .0254
 		yd = yd * .0254
 		zd = zd * .0254

 		[m,n] = shape(x)
 		phi = zeros((m,n))
 		th = zeros((m,n))
 		R = zeros((m,n))

 		coordinates = concatenate((xd, yd, zd), axis=1)
 		R, th, phi = self.cart2rad(coordinates)

 		degIncrement = self.d2r(degIncrement)
 		ii = 2


 		# interpolate data locations into a full sphere
 		if abs(th[0] - th[1]) < tol and abs(phi[0] - phi[1]) > tol:
 	 		while abs(th[ii+1, 0] - th[1, 0]) < tol:
 				ii = ii + 1

 			Nphi = ii
 			Nth = len(th) / (Nphi + 1) # python base index is 0

 			# prealloate matrices
 			th_reg = zeros((Nth, Nphi))
 			phi_reg = zeros((Nth, Nphi))

 			# pdb.set_trace()d
 			for i in range(0,Nth):
 				f = i*25
 				th_reg[i, :] = th[f:(f+24), 0, newaxis].T
 				phi_reg[i, :] = phi[f:(f+24), 0, newaxis].T

 		elif abs(th[1] - th[0]) > tol and abs(phi[1] - phi[0]) < tol:
 			while abs(phi[ii+1] - phi[1]) < tol:
 				ii = ii+1

 			Nth = ii
 			Nphi = len(th) / Nth + 1 # python base index is 0

 			# prealloate matrices
 			th_reg = zeros((Nth, Nphi))
 			phi_reg = zeros((Nth, Nphi))

 			for i in range(0, Nphi):
 				f = i*25
 				th_reg[i, :] = th[f, (f+25)]
 				phi_reg[i, :] = phi[f, (f+25)]

 		else:
 			print('A bit of a fuck up here')
 			pass


 		# check if phi is correct
 		if abs( phi_reg[1, 1] - phi_reg[1, 2]) < tol:
 			print('a bit of a fuck up here')


 		nRotations = round(2*pi/degIncrement)
 		# add check on number of rotations here

 		# rotate the section about the axial axis 		
 		th_mapped = zeros((Nth*2, (Nphi+1)*nRotations))
 		th_mapped[0:Nth, 0:2*(Nphi)] = hstack((th_reg, th_reg))

 		ph_mapped = zeros((Nth*2, (Nphi+1)*nRotations))
  		ph_mapped[0:Nth, 0:2*Nphi] = hstack( (phi_reg, (2*degIncrement - phi_reg[::-1]))) 
 		# ^includes the mirror symmetry plane

 		radius = zeros((Nth*2, Nphi*nRotations))
 		radius = R[0,0]


 		# rotate around azimuthal axis
 		for i in range(0, (nRotations/2 -1)):
 			phRot = 2 * degIncrement * i
 			th_mapped[(0:Nth), (Nphi*2*(i+1))] = th_mapped[(0:Nth), 0:2*Nphi]



 		return ph_mapped, th_mapped, radius


# --------------------------------------------BEGIN SCRIPT----------------------------------------------------

LOCATION = r'/Users/Michael/Downloads/far-field_KHIE/data_from_comsol/22.5deg_data_regular.csv'
# LOCATION = r'C:\Users\mikelee\Desktop\FF\data_from_comsol\FF_pressure.csv'
FF = FarField(LOCATION)
phi, th, r = FF.expandGrid(22.5)

# r, w, y, coord = FF.cart2rad(FF.raw)


# fig = plt.figure()
# ax = fig.add_subplot(111, projection = '3d')
# # ax.scatter(abs(coord[:,0]), abs(coord[:,1]), abs(coord[:,2]))
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# # plt.shot()
