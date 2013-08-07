# convert cartiesian to radial 

# assumptions:
	# units in are inches and outputted in meters
from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class FarField:

 	def __init__(self, FileLocation):
 		self.loc = FileLocation
 		self.raw = (genfromtxt(self.loc, delimiter=',', skip_header=10, dtype=float))


 	def cart2rad(self, coord):
 		# assumes data in the form x, y, z, with y being the axial (azimuthal) direction
  		[m,n] = shape(coord)
 		r = (zeros((m,1)))
 		w = (zeros((m,1)))
 		y = (zeros((m,1)))

 		#convert into meters from inches
 		coord = coord * .0254

 		r = ( coord[:,0] ** 2 + coord[:,2] ** 2)** .5
 		w = (arctan(coord[:,2] / coord[:,0]))
 		y = (coord[:, 1])

 		return r, w, y, coord


 	def d2r(self, deg):
 		#convert degress to radians
 		rad = deg * (pi/ 180)
 		return rad

 	def expandGrid(self, Data, degIncrement):
 		# assume revolution around the y axis 
 		x = abs( Data[:, 0] )
 		y = abs( Data[:, 1] ) 
 		z = abs( Data[:, 2] ) 

 		# redefine coordinates for convention
 		xd = z
 		yd = x
 		zd = y 

 		phi0, th0, r0 = self.cart2rad(Data)
 		degIncrement = self.d2r(degIncrement)












LOCATION = r'/Users/Michael/Downloads/far-field_KHIE/data_from_comsol/22.5deg_data_regular.csv'
# LOCATION = r'Y:\12in, 33mode\No Urethane\data_from_comsol\12D_224E_Al2O3_Full_Stiff_Assembly_Steel_NoUrethane_22.5_pressure.csv'
FF = FarField(LOCATION)

r, w, y, coord = FF.cart2rad(FF.raw)


fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(abs(coord[:,0]), abs(coord[:,1]), abs(coord[:,2]))
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
