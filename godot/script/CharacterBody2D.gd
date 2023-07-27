extends CharacterBody2D

const PORT = 8000

var server = TCPServer.new()
var socket = WebSocketPeer.new()
var screen_size

func _ready():
	screen_size = get_viewport_rect().size
	server.listen(PORT)

func _process(_delta):
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
				print(data)
				
				var x_pos = 25 + data[0] * screen_size[0]
				var y_pos = 725 - (data[1] * screen_size[1])
				
				position = position.lerp(Vector2(x_pos, y_pos), _delta)
				rotation = -data[2]
				
				velocity = Vector2.ZERO
				move_and_slide()
	

