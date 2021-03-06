import time
import numpy as num
import scipy as sci
import sympy as sym
from sympy import *
from numpy import *
from scipy import *
from scipy.sparse import *

x1 = 0; x2 = 0; x3 = 0; x4 = 0; y1 = 0; y2 = 0; y3 = 0; y4 = 0	# Initializing all variables necessary for the program
range_x = 0; range_y = 0; no_of_elements = 0; range_x_temp = 0; range_y_temp = 0
N1 = 0; N2 = 0; N3 = 0; N4 = 0; dN1s = 0; dN2s = 0; dN3s = 0; dN4s = 0; dN1t = 0; dN2t = 0; dN3t = 0; dN4t = 0
mx = []; my = []; ST = []; k_small = []; row = []; col = []; data = []
element = {}; xst = {}; yst = {}; J = {}; J_inv = {}; J_det = {}; XT = {}; XT_trans = {}; Ke = {}; K = {}; K_temp = {}; row_stiffness = {}; col_stiffness = {}
s = symbols('s'); t = symbols('t'); k = symbols('k')
n = 0

def input_geometry():	# First step of the program where the geopetry is specified
	global x1, x2, x3, x4, y1, y2, y3, y4
	print ("""Please enter the corresponding coordinate values for the geometry under study""")
	ex = [float(input("x1\n> ")), float(input("x2\n> ")), float(input("x3\n> ")), float(input("x4\n> "))]
	wy = [float(input("y1\n> ")), float(input("y2\n> ")), float(input("y3\n> ")), float(input("y4\n> "))]
	ex.sort()
	wy.sort()
	x1 = ex[-1]; x2 = ex[0]; x3 = x2; x4 = x1
	y1 = wy[-1]; y4 = wy[0]; y2 = y1; y3 = y4	# This is the part that sorts out the geometry irrespective of the way the coordinates are entered
	mesh_generation()	# Calls for the next step
	
def mesh_generation():	# Second step of the program where the mesh is generated
	global x1, x2, x3, x4, y1, y2, y3, y4, range_x, range_y, no_of_elements, mx, my, range_x_temp, range_y_temp
	print ("""Please enter what kind of mesh you want.
	1. Enter 'coarse' for a rough mesh.
	2. Enter 'normal' for a normal mesh.
	3. Enter 'fine' for a smooth mesh.""")
	mesh_type = input("> ")
	if mesh_type == 'coarse':	# Coarse mesh splits the geometry into 5 equal horizontal and vertical parts
		x = num.linspace(x2, x1, 5)
		y = num.linspace(y4, y1, 5)
		mx, my = meshgrid(x, y)
		print(mx)
		print(my)
		range_x_temp, range_y_temp = mx.shape
		print(mx.shape)
		print(my.shape)
		range_x = range_x_temp-1
		range_y = range_y_temp-1
		print(range_x, range_y)
		no_of_elements = range_x*range_y
		print(no_of_elements)
	elif mesh_type == 'normal':	# Normal mesh splits the geometry into 10 equal horizontal and vertical parts
		x = num.linspace(x2, x1, 10)
		y = num.linspace(y4, y1, 10)
		mx, my = meshgrid(x, y)
		print(mx)
		print(my)
		range_y_temp, range_x_temp = mx.shape
		range_x = range_x_temp-1
		range_y = range_y_temp-1
		print (range_x, range_y)
		no_of_elements = range_x*range_y
		print(no_of_elements)
	elif mesh_type == 'fine':	# Fine mesh splits the geometry into 20 equal horizontal and vertical parts
		x = num.linspace(x2, x1, 20)
		y = num.linspace(y4, y1, 20)
		mx, my = meshgrid(x, y)
		print(mx)
		print(my)
		range_x_temp, range_y_temp = mx.shape
		print(mx.shape)
		range_x = range_x_temp-1
		range_y = range_y_temp-1
		print (range_x, range_y)
		no_of_elements = range_x*range_y
		print(no_of_elements)
	elif mesh_type == 'sample':	# Sample mesh splits the geometry into any equal horizontal and vertical parts specified by the programmer. Can only be tweaked from inside the code.
		x = num.linspace(x2, x1, 3)
		y = num.linspace(y4, y1, 3)
		mx, my = meshgrid(x, y)
		print(mx)
		print(my)
		range_x_temp, range_y_temp = mx.shape
		print(mx.shape)
		range_x = range_x_temp-1
		range_y = range_y_temp-1
		print (range_x, range_y)
		no_of_elements = range_x*range_y
		print(no_of_elements)
	else:
		mesh_generation()
	input()
	four_node_iso()	# Calls for the next step of the process

def boundary_conditions():	# Sixth step of the process that gathers temperature boundary conditions from the user. Not yet implemented.
	print ("""Here you will specify the boundary conditions for the problem.
	Temperature will assume the unit of Kelvin, heat flux will assume the unit of W/m2, conveciton coefficient will assume the unit of W/m2K and heat generation will assume the unit of W'm3.
	When specifying boundary conditions, please enter only the numerical values and not the units.
	Enter 'temp' for temperature boundary condition.
	Enter 'conv' for convection boundary condition.
	Enter 'flux' for heat flux boundary condition.
	Enter 'gen' for heat flux generation.
	Enter 'done' once everthing is specified.""")
	type = input("> ")
	if type == 'temp':
		print ("""Please choose the boundary in which you want to apply temperature boundary conditions.""")
		print ("Edge 1 is between the coordinates (%d, %d) and (%d, %d)" % (x1, y1, x2, y2))
		print ("Edge 2 is between the coordinates (%d, %d) and (%d, %d)" % (x2, y2, x3, y3))
		print ("Edge 3 is between the coordinates (%d, %d) and (%d, %d)" % (x3, y3, x4, y4))
		print ("Edge 4 is between the coordinates (%d, %d) and (%d, %d)" % (x4, y4, x1, y1))
		print ("""Please enter the no. of the edge you want to select""")
		edge = input("> ")
		if edge == '1':
			temp_1 = int(input("Please enter the temperature\n> "))
			boundary_conditions()
		elif edge == '2':
			temp_2 = int(input("Please enter the temperature\n> "))
			boundary_conditions()
		elif edge == '3':
			temp_3 = int(input("Please enter the temperature\n> "))
			boundary_conditions()
		elif edge == '4':
			temp_4 = int(input("Please enter the temperature\n> "))
			boundary_conditions()
		else:
			print("Sorry, that is not a valid value")
			boundary_conditions()
	elif type == 'conv':
		print ("""Please choose the boundary in which you want to apply convection boundary conditions.""")
		print ("Edge 1 is between the coordinates (%d, %d) and (%d, %d)" % (x1, y1, x2, y2))
		print ("Edge 2 is between the coordinates (%d, %d) and (%d, %d)" % (x2, y2, x3, y3))
		print ("Edge 3 is between the coordinates (%d, %d) and (%d, %d)" % (x3, y3, x4, y4))
		print ("Edge 4 is between the coordinates (%d, %d) and (%d, %d)" % (x4, y4, x1, y1))
		print ("""Please enter the no. of the edge you want to select""")
		edge = input("> ")
		if edge == '1':
			temp_amb_1 = int(input("Please enter the value of the ambient temperature\n> "))
			conv_coeff_1 = int(input("Please enter the value of the convection coefficient\n> "))
			boundary_conditions()
		elif edge == '2':
			temp_amb_2 = int(input("Please enter the value of the ambient temperature\n> "))
			conv_coeff_2 = int(input("Please enter the value of the convection coefficient\n> "))
			boundary_conditions()
		elif edge == '3':
			temp_amb_3 = int(input("Please enter the value of the ambient temperature\n> "))
			conv_coeff_3 = int(input("Please enter the value of the convection coefficient\n> "))
			boundary_conditions()
		elif edge == '4':
			temp_amb_4 = int(input("Please enter the value of the ambient temperature\n> "))
			conv_coeff_4 = int(input("Please enter the value of the convection coefficient\n> "))
			boundary_conditions()
		else:
			print("Sorry, that is not a valid value")
			boundary_conditions()
	elif type == 'flux':
		print ("""Please choose the boundary in which you want to apply heat flux boundary conditions.""")
		print ("Edge 1 is between the coordinates (%d, %d) and (%d, %d)" % (x1, y1, x2, y2))
		print ("Edge 2 is between the coordinates (%d, %d) and (%d, %d)" % (x2, y2, x3, y3))
		print ("Edge 3 is between the coordinates (%d, %d) and (%d, %d)" % (x3, y3, x4, y4))
		print ("Edge 4 is between the coordinates (%d, %d) and (%d, %d)" % (x4, y4, x1, y1))
		print ("""Please enter the no. of the edge you want to select""")
		edge = input("> ")
		if edge == '1':
			heat_flux_1 = int(input("Please enter the value of the heat flux in this edge\n> "))
			boundary_conditions()
		if edge == '2':
			heat_flux_2 = int(input("Please enter the value of the heat flux in this edge\n> "))
			boundary_conditions()
		if edge == '3':
			heat_flux_3 = int(input("Please enter the value of the heat flux in this edge\n> "))
			boundary_conditions()
		if edge == '4':
			heat_flux_4 = int(input("Please enter the value of the heat flux in this edge\n> "))
			boundary_conditions()
		else:
			print ("Sorry, that is not a valid value")
			boundary_conditions()
	elif type == 'gen':
		heat_gen = int(input("Please enter the value of the heat generation per unit volume within the object\n> "))
		boundary_conditions()
	elif type == 'done':
		stiffness_matrix()
	else:
		print ("Sorry, that is not a valid command")
		boundary_conditions()
	four_node_iso()
	
def four_node_iso():	# Third step of the process which implements a four node isoparametric element for the analysis
	global N1, N2, N3, N4, k_small, ST, dN1s, dN2s, dN3s, dN4s, dN1t, dN2t, dN3t, dN4t, s, t, k
	
	N1 = ((1+s)*(1+t)/4)	# Shape functions
	N2 = ((1-s)*(1+t)/4)
	N3 = ((1-s)*(1-t)/4)
	N4 = ((1+s)*(1-t)/4)
	
	dN1s = sym.diff(N1, s); dN1t = sym.diff(N1, t)	# Differentiating the shape functions
	dN2s = sym.diff(N2, s); dN2t = sym.diff(N2, t)
	dN3s = sym.diff(N3, s); dN3t = sym.diff(N3, t)
	dN4s = sym.diff(N4, s); dN4t = sym.diff(N4, t)
	
	ST = sym.Matrix([[dN1s, dN2s, dN3s, dN4s], [dN1t, dN2t, dN3t, dN4t]])	# Assembling the differentiated shape functions
	print(ST)
	
	k = 4	# k value can be tweaked here
	
	k_small = sym.Matrix([[k, 0], [0, k]])	# Calculating the k small matrix which will be the same for all elements since all elements are identical
	print(k_small)
	
	input()
	stiffness_matrix()	# Calls for the next step of the process
	
def stiffness_matrix():	# Fourth step of the process which calculates the element stiffness matrices for all the elements
	global range_x_temp, range_y_temp, no_of_elements, mx, my, element, xst, yst, J, J_inv, J_det, XT, XT_trans, Ke, K, K_temp, N1, N2, N3, N4, ST, k_small, s, t, k
	j = 0
	i = 0
	for h in range(no_of_elements):
		element[h] = sym.Matrix([[mx[i+1][j+1], my[i+1][j+1]],	# Splitting the individual element coordinate matrices to extract the values
								[mx[i+1][j], my[i+1][j]],
								[mx[i][j], my[i][j]],
								[mx[i][j+1], my[i][j+1]]])
		j += 1
		if j == range_y:
			j = 0
			i += 1
	print(element)
	input()
	
	xst[0] = (element[0][0]*N1)+(element[0][2]*N2)+(element[0][4]*N3)+(element[0][6]*N4); print('x =', xst[0]); input()	# Calculating the coordinate values in the isoparametric coordinates using
	yst[0] = (element[0][1]*N1)+(element[0][3]*N2)+(element[0][5]*N3)+(element[0][7]*N4); print('y =', yst[0]); input()	# the coordinate values from the cartesian coordinates
	J[0] = sym.Matrix([[sym.diff(xst[0], s), sym.diff(yst[0], s)], [sym.diff(xst[0], t), sym.diff(yst[0], t)]]); print('Jacobian =', J[0]); input()	# Jacobian matrix
	J_inv[0] = J[0].inv(); print('Jacobian inverse =', J_inv[0]); input()	# Jacobian inverse
	J_det[0] = J[0].det(); print('Jacibian determinant =', J_det[0]); input()	# Determinant of the Jacobian matrix
	XT[0] = J_inv[0]*ST; print('B =', XT[0]); input()	# B matrix
	XT_trans[0] = XT[0].transpose(); print('B transpose =', XT_trans[0]); input()	# Transpose of B matrix
	Ke[0] = sym.Matrix(4, 4, XT_trans[0]*k_small*XT[0]*J_det[0]).tolist(); print('Ke =', Ke[0]); input()	# Substituting values into the stiffness matrix equation
	K[0] = sym.zeros(4, 4).tolist()
	for m in range(4):	# Calculating stiffness matrices for each element
		for n in range(4):	# Calculating K values for each point in an element stiffness matrix
			K[0][m][n] = (integrate(Ke[0][m][n], (t, -1, 1), (s, -1, 1)))	# Integrating each term of the element stiffness matrix
	print ('Element Stiffness Matrix =', K[0]); input()
	stiffness_assembly()	# Calls for the next step of rhe process
	
def stiffness_assembly():	# Fifth step of the process that assembles all the element stiffness matrices into a single global stiffness matrix
	global n, mapping, K, row, col, data, row_stiffness, col_stiffness
	n = int(math.sqrt(no_of_elements))
	mapping = num.array([2, 3, 1, 0])	# Mapping to help match values from element stiffness matrices to their respective positions in the global stiffness matrix
	element_stiffness = num.matrix([[4,-1,-2,-1], [-1,4,-1,-2], [-2,-1,4,-1], [-1,-2,-1,4]]).tolist()

	a = 0	# Calcualtes the row index values
	for row_index in range ((n**2)+(n-1)):
		if (row_index+1) % (n+1) == 0 and row_index != 0:
			continue
		row_stiffness[a] = num.array([row_index, row_index+1, row_index+n+1, row_index+n+2])
		a += 1
	print(row_stiffness)

	b = 0	# Calculates the column index values
	for column_index in range((n**2)+(n-1)):
		if (column_index+1) % (n+1) == 0 and column_index != 0:
			continue
		col_stiffness[b] = num.array([column_index, column_index+1, column_index+n+1, column_index+n+2])
		b += 1
	print(col_stiffness)

	for i in range(n**2):
		c = 0	
		column_final = col_stiffness[i]
	
		for j in range(4):
			row_final = row_stiffness[i][c]
			c += 1
			row_element = mapping[j]
			col.append(column_final)
		
			for k in range(4):
				row.append(row_final)
				column_element = mapping[k]
				data.append(K[0][row_element][column_element])
	row = ravel(row)
	col = ravel(col)
	data = ravel(data)
	print(row)
	print(shape(row))
	input()
	print(col)
	print(shape(col))
	input()
	print(data)
	print(shape(data))
	input()
	
	stiffness = coo_matrix((data, (row, col)), shape=((n+1)**2,(n+1)**2), dtype = int8).toarray()	# Assembles the global stiffness matrix
	print(stiffness)
	input()	# Should call for the next step in the process which is getting boundary conditions from the user
	
input_geometry()	# Starts the program from input geometry
