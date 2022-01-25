extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var id = null
var health = 0
var width = 0
var height = 0
var game_position = [0, 0]
var collidable = false
var destructible = false
var game_rotation = 0
var turn_cooldown = 0
var countdown = null

var texture_off = preload("res://Assets/BYTEART/TELEPORTER_DISABLED.png")
var texture_on = preload("res://Assets/BYTEART/TELEPORTER_ENABLED.png")


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func update():
	self.get_node("Sprite").scale.x = width/16
	self.get_node("Sprite").scale.y = height/16
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))
	if turn_cooldown == countdown:
		self.get_node("Sprite").texture = texture_on
	else: 
		self.get_node("Sprite").texture = texture_off

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
