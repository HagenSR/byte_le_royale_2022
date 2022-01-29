extends StaticBody2D


var id = null
var health = 0
var width = 0
var height = 0
var game_position = [0, 0]
var collidable = false
var destructible = true
var game_rotation = 0

var textures = []


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():

	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))

	self.get_node("Sprite").scale.x = width/16
	self.get_node("Sprite").scale.y = height/16
#	if health > 12:
#		get_node("Sprite").texture = textures[0]
#	elif health > 6:
#		get_node("Sprite").texture = textures[1]
#	elif health > 0:
#		get_node("Sprite").texture = textures[2]


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
