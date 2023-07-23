extends CharacterBody2D

const PORT = 8000

var server = TCPServer.new()
var socket = WebSocketPeer.new()
var screen_size

func _ready():
	screen_size = get_viewport_rect().size
	server.listen(PORT)

func _process(delta):
	var err: Error
	socket.accept_stream(server.take_connection())
	socket.poll()
	
	var state = socket.get_ready_state()
	var data
	
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			var packet = socket.get_packet()
			
			var json = JSON.new()
			err = json.parse(packet.get_string_from_utf8())
			
			if err == OK:
				data = json.data
				
				position.x = data[0] * screen_size[0] * delta + 25
				position.y = data[1] * screen_size[1] * delta + 25
				rotation = data[2]
				
				velocity = Vector2.ZERO
				move_and_slide()
	

