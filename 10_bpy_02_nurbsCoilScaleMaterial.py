
#
# author: Nadeem Elahi
# nadeem.elahi@gmail.com
# nad@3deem.com
# license: gpl v3
# 

#
# Automated Rotated Geometry Generation
#

import bpy
from math import radians




def fullReset() :
	#https://blenderartists.org/t/deleting-all-from-scene/1296469
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)

	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()


	
def addLamp( name , watts , radius , 
		xloc , yloc , zloc ) :
	#https://docs.blender.org/api/master/bpy.types.Object.html

	lamp_name = name
	light_data = bpy.data.lights.new( 
			name = lamp_name ,
			type = 'POINT'
			)
	light_object = bpy.data.objects.new(
			name = lamp_name ,
			object_data = light_data
			)
	light_object.location = ( xloc , yloc , zloc )

	bpy.context.scene.collection.objects.link ( light_object )
	bpy.data.lights[ lamp_name ].energy = watts # 10 W default
	bpy.data.lights[ lamp_name ].shadow_soft_size = radius 



def addCam( name , 
		xloc , yloc , zloc ,
		xangle , yangle , zangle ) :

	camera_data = bpy.data.cameras.new( name = camera_name )

	camera_object = bpy.data.objects.new( camera_name , camera_data )
	camera_object.rotation_euler = ( xangle , yangle , zangle )
	camera_object.location = ( xloc , yloc , zloc )

	bpy.context.scene.collection.objects.link( camera_object )
		
	bpy.context.view_layer.objects.active = camera_object



def addNurbsPath ( name ,
		radius , depth , resolution ,
		fillCaps ,
		xloc , yloc , zloc ,
		xangle , yangle , zangle ,
		xscale , yscale , zscale ) :

	bpy.ops.curve.primitive_nurbs_path_add(
			radius = radius ,
			location = ( xloc , yloc , zloc ) , 
			rotation = ( xangle , yangle , zangle ) ,
			scale = ( xscale , yscale , zscale )
			)

	bpy.context.object.name = name

	bpy.data.objects[ name ].data.bevel_depth = depth
	bpy.data.objects[ name ].data.bevel_resolution = resolution 
	if ( fillCaps ) :
		bpy.data.objects[ name ].data.use_fill_caps = True

	


def extrudeNurbsPath ( xloc , yloc , zloc ) :
	bpy.ops.curve.extrude_move(
			CURVE_OT_extrude={"mode":'TRANSLATION'}, 
			TRANSFORM_OT_translate={
				"value":(xloc, yloc, zloc) 
				}
			)




def addMaterial ( col_name , obj_name ,
		rcol, gcol , bcol, acol , 
		metallic , roughness ) :

	mat = bpy.data.materials.new( col_name ) 
	bpy.data.materials[ col_name ].diffuse_color = [ rcol , gcol , bcol , acol ]
	bpy.data.materials[ col_name ].metallic = metallic 
	bpy.data.materials[ col_name ].roughness = roughness 
	bpy.ops.object.material_slot_add()
	bpy.data.objects[ obj_name ].active_material = mat


#
# settings
#

# scene reset - delete all objects and data

fullReset()


# add lamp
lamp_name = "lamp1" # front right
addLamp( lamp_name , 100 , 1.0 , # 100 watts , shadow_soft_size / radius 1.0
		1.0 , -1.0 , 1.0 )


lamp_name = "lamp2" # front left up higher 
addLamp( lamp_name , 100 , 5.0 , # 100 watts , shadow_soft_size / radius 1.0
		-2.0 , -2.0 , 2.0 )


lamp_name = "lamp3" # back center
addLamp( lamp_name , 100 , 5.0 , # 100 watts , shadow_soft_size / radius 1.0
		0.0 , 2.0 , 2.0 )



# add camera 
camera_name = "camera1"
addCam( camera_name , 
	0.0 , -5.0 , 2.0 , # xyz loc
	radians( 67 ) , 0 , 0 ) # angles



# wire thinkness/radius
loopCnt = 50

depth = 0.1 
rad = depth / 4 

width = 15  
height = 10  

xcham = 0.15 # corner chamfer
ycham = 0.10 




# pt 1 - coilPointsDiagram.svg
xloc = xcham
yloc = 0.0
zloc = 0.0

# nurbs path coil
nurbs_path_name = "nurbs1"
addNurbsPath ( nurbs_path_name ,
		1.0 , depth , 4 , # radius , depth , resolution
		1 , # fill caps/end points
		xloc , yloc , zloc ,
		0.0 , 0.0 , 0.0 , 
		1.0 , 1.0 , 1.0 
		)


# 5 verts to start
# remove all but the center vert 
# there are 5 total by default
# delete first two and last two

bpy.ops.object.select_all( action='DESELECT' )
bpy.data.objects[ nurbs_path_name ].select_set( True )

bpy.ops.object.mode_set( mode='EDIT' )
bpy.ops.curve.select_all(action='DESELECT')

bpy.ops.curve.de_select_last()
bpy.ops.curve.dissolve_verts()

#twice
bpy.ops.curve.de_select_last()
bpy.ops.curve.dissolve_verts()

bpy.ops.curve.de_select_first()
bpy.ops.curve.dissolve_verts()

bpy.ops.curve.de_select_first()
bpy.ops.curve.dissolve_verts()

# just center vert remains
bpy.ops.curve.de_select_last()



def eachCoil() :
	# pt 2 - coilPointsDiagram.svg
	xloc = width
	yloc = 0 
	zloc = rad 

	extrudeNurbsPath ( xloc , yloc , zloc )



	# pt 3 - coilPointsDiagram.svg
	xloc = xcham 
	yloc = ycham
	zloc = 0 

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 4 - coilPointsDiagram.svg
	xloc = 0
	yloc = height
	zloc = rad

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 5 - coilPointsDiagram.svg
	xloc = -xcham
	yloc = +ycham 
	zloc = 0

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 6 - coilPointsDiagram.svg
	xloc = -width
	yloc = 0
	zloc = rad

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 7 - coilPointsDiagram.svg
	xloc = -xcham
	yloc = -ycham 
	zloc = 0

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 8 - coilPointsDiagram.svg
	xloc = 0
	yloc = -height
	zloc = rad

	extrudeNurbsPath ( xloc , yloc , zloc )


	# pt 9 - coilPointsDiagram.svg
	xloc = xcham 
	yloc = -ycham
	zloc = 0

	extrudeNurbsPath ( xloc , yloc , zloc )

idx = 0
while idx < loopCnt :
	eachCoil()
	idx += 1



bpy.ops.curve.shade_smooth()


bpy.context.scene.cursor.location = (0.0, 0.0, 0.0) 
bpy.ops.object.mode_set( mode='OBJECT' )

bpy.data.objects[ nurbs_path_name ].scale = ( 0.1 , 0.1 , 0.1 )
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')


addMaterial ( "matCopperCoil" , nurbs_path_name ,
		1.0 , 0.289 , 0.023 , 1.0 ,
		1.0 , 0.1 # metallic , roughness
		)


bpy.data.scenes["Scene"].render.film_transparent = True

bpy.context.scene.render.image_settings.color_mode = 'RGBA'

last_frame = 36
bpy.data.scenes["Scene"].frame_start = 1
bpy.data.scenes["Scene"].frame_end = last_frame

# frame 1:0deg -> 360:359deg
#https://docs.blender.org/api/current/info_quickstart.html

nurbs_coil = bpy.data.objects[ nurbs_path_name ]
nurbs_coil.animation_data_create()
nurbs_coil.animation_data.action = bpy.data.actions.new( name = "zRotate360" )

fcurve = nurbs_coil.animation_data.action.fcurves.new ( data_path = "rotation_euler" , index = 2 )


last_deg = radians ( 359 )

keyframe_one = fcurve.keyframe_points.insert ( frame = 1 , value = 0 )
keyframe_one.interpolation = "LINEAR"

keyframe_two = fcurve.keyframe_points.insert ( frame = last_frame , value = last_deg )
keyframe_two.interpolation = "LINEAR"
