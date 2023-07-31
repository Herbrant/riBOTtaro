extends CharacterBody2D

const PORT = 8000

var server = TCPServer.new()
var socket: WebSocketPeer = null
var screen_size
var err: Error

func _ready():
	screen_size = get_viewport_rect().size
	server.listen(PORT)

func _process(_delta):	
	if socket == null:
		if server.is_connection_available():
			socket = WebSocketPeer.new()
			socket.accept_stream(server.take_connection())
	else:
		socket.poll()
			
		var state = socket.get_ready_state()
		
		if state == WebSocketPeer.STATE_OPEN:
			while socket.get_available_packet_count():
				var packet = socket.get_packet()
				
				var json = JSON.new()
				err = json.parse(packet.get_string_from_utf8())
				
				if err == OK:
					var data = json.data
					print(data)
					
					var x_pos = 25  + data[0] * screen_size[0]
					var y_pos = 725 - (data[1] * screen_size[1])
					
					
					if rotation_degrees != -rad_to_deg(data[2]):
						rotation_degrees = -(180 - rad_to_deg(data[2]))
					position = position.lerp(Vector2(x_pos, y_pos), _delta)

					#velocity = Vector2.ZERO
					#move_and_slide()
	

