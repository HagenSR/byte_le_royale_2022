extends StaticBody2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var consumable_type = 0
var width = 0
var height = 0
var game_position = [0, 0]

var textures = [
	preload("res://Assets/BYTEART/HEALTH_PACK.png"),
	preload("res://Assets/BYTEART/SHIELD.png"),
	preload("res://Assets/BYTEART/SPEED.png"),
	preload("res://Assets/BYTEART/RADAR.png"),
	preload("res://Assets/BYTEART/GERNADE.png"),
]


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():
	get_node("Sprite").texture = textures[consumable_type-1]
	self.get_node("Sprite").scale.x = width/16
	self.get_node("Sprite").scale.y = height/16
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
