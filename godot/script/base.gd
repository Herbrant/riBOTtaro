extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	var obstacle_scene = load("res://scene/Obstacle.tscn")
	var screen_size = get_viewport().get_visible_rect().size
	
	var test = obstacle_scene.instantiate()
	test.position.x = 100
	test.position.y = 150
	add_child(test)
	
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
