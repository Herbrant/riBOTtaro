extends CharacterBody2D

@export var speed = 400
@export var rotation_speed = 1.5

var server = TCPServer.new()
var socket = WebSocketPeer.new()
var peer: StreamPeerTCP
var rotation_direction = 0

func get_input():
	rotation_direction = Input.get_axis("left", "right")
	velocity = transform.x * Input.get_axis("down", "up") * speed

func _physics_process(delta):
	get_input()
	rotation += rotation_direction * rotation_speed * delta
	move_and_slide()

func _ready():
	server.listen(8000)
	

func _process(delta):
	socket.poll()
	peer = server.take_connection()
	socket.accept_stream(peer)
	
	var state = socket.get_ready_state()
	if state == socket.STATE_OPEN:
		print("OPEN")
	elif state == socket.STATE_CLOSING:
		print("CLOSING")
	elif state == socket.STATE_CLOSED:
		print("CLOSED")
	
	
	
