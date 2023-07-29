extends Node2D

func load_map():
	var file = FileAccess.open("res://config/matrix3.txt", FileAccess.READ)
	var line = ""
	var map = []
	
	while (not file.eof_reached()):
		line = file.get_line()
		var tmp_arr = line.split(" ")
		map.append(tmp_arr)
	
	return map

func set_map():
	var obstacle_scene = load("res://scene/Obstacle.tscn")
	#var target_scene = load("res://scene/target.tscn")
	var screen_size = get_viewport().get_visible_rect().size
	print(screen_size)
	
	var m = load_map()
	
	var square_size = Vector2(screen_size[0]/float(len(m[0])), screen_size[1]/float(len(m)))
	
	for i in range(len(m)):
		for j in range(len(m[i])):
			if m[i][j] == "1":
				var obj = obstacle_scene.instantiate()
				obj.position.y = 52 + square_size.y * i
				obj.position.x = 40 + square_size.x * j
				
				add_child(obj)
#			elif m[i][j] == "X":
#				var obj = target_scene.instantiate()
#				obj.position.y = square_size.y * i + 90
#				obj.position.x = square_size.x * j + 55
#
#				add_child(obj)

# Called when the node enters the scene tree for the first time.
func _ready():
	set_map()

