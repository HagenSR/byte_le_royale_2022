extends StaticBody2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var id = null
var amount = 0
var game_position = [0, 0]
var heading = 0


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
