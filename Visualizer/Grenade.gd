extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var fuse_time = 1000
var game_position = [0,0]

var explosion = preload("res://Assets/explosion.jpeg")

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func update():
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))
	if fuse_time <= 0:
		if fuse_time <= -1:
			self.remove_and_skip()
		self.get_node("Sprite").texture = explosion
		self.get_node("Sprite").scale.x = 75*(1/820)
		self.get_node("Sprite").scale.y = 75*(1/500)
		
	fuse_time -= 1
	
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
