extends KinematicBody2D


# Declare member variables here. Examples:
var id = null
var heading = 0
var width = 0
var height = 0
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
var gun_primary = 0
var team_name = ""

var textures = [[preload("res://Assets/BYTEART/PISTOL_LEVEL1.png"),
preload("res://Assets/BYTEART/PISTOL_LEVEL2.png"),
preload("res://Assets/BYTEART/PISTOL_LEVEL3.png"),],
[preload("res://Assets/BYTEART/RIFLE_LEVEL1.png"),
preload("res://Assets/BYTEART/RIFLE_LEVEL2.png"),
preload("res://Assets/BYTEART/RIFLE_LEVEL3.png")],
[preload("res://Assets/BYTEART/SHOTGUN_LEVEL1.png"),
preload("res://Assets/BYTEART/SHOTGUN_LEVEL2.png"),
preload("res://Assets/BYTEART/SHOTGUN_LEVEL3.png")],
[preload("res://Assets/BYTEART/SNIPER_LEVEL1.png"),
preload("res://Assets/BYTEART/SNIPER_LEVEL2.png"),
preload("res://Assets/BYTEART/SNIPER_LEVEL3.png")]]

func set_gun():
	if inventory["guns"][gun_primary] != null:
		var gun = inventory["guns"][gun_primary]["gun_type"]
		var level = inventory["guns"][gun_primary]["level"]
		self.get_node("Sprite/Sprite").texture = textures[gun-1][level-1]
		if gun == 0:
			self.get_node("Sprite/Sprite").offset = 15
		if gun == 1:
			self.get_node("Sprite/Sprite").offset = 20
		if gun == 2:
			self.get_node("Sprite/Sprite").offset = 20
		if gun == 3:
			self.get_node("Sprite/Sprite").offset = 40
	else:
		self.get_node("Sprite/Sprite").texture = null
	
	

# Called when the node enters the scene tree for the first time.
func _ready():
	self.get_node("Sprite").scale.x = .5
	self.get_node("Sprite").scale.y = .5
	pass # Replace with function body.

func update():
	#set_gun()
	self.get_node("Label").text = team_name
	self.get_node("Label").set_as_toplevel(true)
	self.get_node("Label").set_position(self.position)
	self.position = (Vector2(float((2*game_position[0])+(2*width)/2), float((2*game_position[1])+(2*width)/2)))
	self.rotation_degrees = heading
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
