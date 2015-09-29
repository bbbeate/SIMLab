#====================================#
#         Material test              #
#====================================#

#====================================#
#         Importing modules          #
#====================================#

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import csv


from abaqus import *			#These statements make the basic Abaqus objects accessible to the script... 
from abaqusConstants import *	#... as well as all the Symbolic Constants defined in the Abaqus Scripting Interface.
import odbAccess        		# To make ODB-commands available to the script


#This makes mouse clicks into physical coordinates
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)


#==============================================================================
#	PRELIMINARIES 
#==============================================================================
modelName = 'Linear'

mdb.Model(modelType=STANDARD_EXPLICIT, name=modelName) 	#Create a new model 
if len( mdb.models.keys() ) == 2:			#Delete the default model if present
	del mdb.models['Model-1']								

saveModel = 1			#If 1: save model
runJob = 0		     	#If 1: run job
postProcess = 0			#If 1: post process
Cpus = 2				#Number of CPU's

#====================================#
#          Material                  #
#====================================#

#==== Inputs ====#
materialName = 'Aluminium'
description = 'This is our material'
density = 400
yield_stress = 250
poisson = 0.3
materialData = 'material_data.txt'



mdb.models[modelName].Material(description=description, name=materialName)
mdb.models[modelName].materials[materialName].Density(table=((density, ), ))
mdb.models[modelName].materials[materialName].Elastic(table=((yield_stress, poisson), ))

# Importing material data into plastic table
a = []
with open(materialData, 'r') as f:
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		a.append((float(row[0]), float(row[1])))
	b = tuple(a)
	mdb.models[modelName].materials[materialName].Plastic(table=b)


#====================================#
#          Part                      #
#====================================#

partName = 'Part-1'


###  Geometry  ###
mdb.models[modelName].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[modelName].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(70.0, 12.5))
    
###  Type   ###
mdb.models[modelName].Part(dimensionality=TWO_D_PLANAR, name=partName, type=
    DEFORMABLE_BODY)
mdb.models[modelName].parts[partName].BaseShell(sketch=
    mdb.models[modelName].sketches['__profile__'])
del mdb.models[modelName].sketches['__profile__']

