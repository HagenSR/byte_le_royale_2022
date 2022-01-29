extends StaticBody2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var id = null
var gun_type = 0
var level = 0
var pattern = 0
var damage = 0
var fire_rate = 0
var gun_range = 0
var mag_size = 0
var mag_ammo = 0
var width = 0
var height = 0
var game_position = [0,0]

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



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	
func update():
	if level-1 > 0:
		self.get_node("Sprite").texture = textures[gun_type-1][level-1]
	self.get_node("Sprite").scale.x = width/16
	self.get_node("Sprite").scale.y = height/8
	self.position = (Vector2(float(2*game_position[0]), float(2*game_position[1])))


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
