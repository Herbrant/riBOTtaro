extends CharacterBody2D

@export var speed = 400
@export var rotation_speed = 1.5

const PORT = 8000

var server = TCPServer.new()
var socket = WebSocketPeer.new()

var rotation_direction = 0

func get_input():
	rotation_direction = Input.get_axis("left", "right")
	velocity = transform.x * Input.get_axis("down", "up") * speed

func _physics_process(delta):
	get_input()
	rotation += rotation_direction * rotation_speed * delta
	move_and_slide()

func _ready():
	server.listen(PORT)
	

func _process(delta):
	var err: Error
	socket.accept_stream(server.take_connection())
	socket.poll()
	
	var state = socket.get_ready_state()
	
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			
			print("Packet: ",packet.get_string_from_utf8())
	
	
	# Position updates
	var v: Vector2
	v.x = 1
	v.y = 1
	global_translate(v)
	move_and_slide()
	rotate(10)
