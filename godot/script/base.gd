extends Node2D


var server = TCPServer.new()
var socket = WebSocketPeer.new()
var stream : StreamPeerTCP
var PORT = 8080

func load_map():
	var file = FileAccess.open("res://config/matrix.txt", FileAccess.READ)
	var line = ""
	var map = []
	
	while (not file.eof_reached()):
		line = file.get_line()
		var tmp_arr = line.split(" ")
		map.append(tmp_arr)
	
	return map

func set_map():
	var obstacle_scene = load("res://scene/Obstacle.tscn")
	var screen_size = get_viewport_rect().size
	print(screen_size)
	
	var m = load_map()
	
	for i in range(len(m)):
		for j in range(len(m[i])):
			if m[i][j] == "1":
				var obj = obstacle_scene.instantiate()
				obj.position.y = screen_size[0]/len(m) * i
				obj.position.x = screen_size[1]/len(m[i]) * j
				add_child(obj)



func info(msg):
	print(msg)

# Called when the node enters the scene tree for the first time.
func _ready():
	set_map()
	server.listen(PORT)

func _process(delta):
	var conn = server.is_connection_available()
	if conn and !stream:
		stream = server.take_connection()
		stream.set_no_delay(true)
		socket.accept_stream(stream)
		
		while socket.get_ready_state() != WebSocketPeer.STATE_OPEN:
			socket.poll()
		
		socket.send_text("Test message from server")
