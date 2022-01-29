extends StaticBody2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var id = null
var opening_speed = 0
var open_state = false
var game_position = [0, 0]
var width = 0
var height = 0

var horiz_closed = preload("res://Assets/BYTEART/DOOR_HORIZONTAL_CLOSED.png")
var horiz_open = preload("res://Assets/BYTEART/DOOR_HORIZONTAL_OPEN.png")
var vert_closed = preload("res://Assets/BYTEART/DOOR_VERTICAL_CLOSED.png")
var vert_open = preload("res://Assets/BYTEART/DOOR_VERTICAL_OPEN.png")


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))
	self.get_node("Sprite").scale.x = (width/16)
	self.get_node("Sprite").scale.y = (height/16)
	if open_state == false:
		if width < height: 
			get_node("Sprite").texture = vert_closed
		else:
			get_node("Sprite").texture = horiz_closed
	elif open_state == true:
		if width < height:
			get_node("Sprite").texture = vert_open
		else:
			get_node("Sprite").texture = horiz_open

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
