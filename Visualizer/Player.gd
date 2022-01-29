extends KinematicBody2D


# Declare member variables here. Examples:
var id = null
var heading = 0
var health = 0
var speed = 0
var money = 0
var armor = 0
var sprite_visible = true
var view_radius = 30
var moving = false
var inventory = []
var primary = 0
var game_position = []

var textures = []


# Called when the node enters the scene tree for the first time.
func _ready():
	self.get_node("Sprite").scale.x = .5
	self.get_node("Sprite").scale.y = .5
	pass # Replace with function body.

func update():
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))
	self.rotation_degrees = heading
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
