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

var textures = [
	preload("res://Assets/BYTEART/DOOR_HORIZONTAL_CLOSED.png"),
	preload("res://Assets/BYTEART/DOOR_HORIZONTAL_OPEN.png"),
]


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))
	self.get_node("Sprite").scale.x = (width/16)
	self.get_node("Sprite").scale.y = (height/16)
	if open_state == false:
		get_node("Sprite").texture = textures[0]
	elif open_state == true:
		get_node("Sprite").texture = textures[1]

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
