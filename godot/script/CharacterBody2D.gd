extends CharacterBody2D

const PORT = 8000

var server = TCPServer.new()
var socket = WebSocketPeer.new()
var screen_size

func _ready():
	screen_size = get_viewport_rect().size
	server.listen(PORT)

func _physics_process(delta):
	var err: Error
	socket.accept_stream(server.take_connection())
	socket.poll()
	
	var state = socket.get_ready_state()
	
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			var pos = packet.to_float32_array()
			print("Packet received: ", pos)
			
			position.x = pos[0] * screen_size[0] * delta
			position.y = pos[1] * screen_size[1] * delta
			rotation = pos[2]
			
			velocity = Vector2.ZERO
			move_and_slide()
			
	

func _process(delta):
	pass

