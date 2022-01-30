extends MarginContainer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"\
var health = 0
var armor = 0
var shield = false
var money = 0
var inventory = []

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

var c_textures = [preload("res://Assets/BYTEART/HEALTH_PACK.png"),
preload("res://Assets/BYTEART/SHIELD.png"),
preload("res://Assets/BYTEART/SPEED.png"),
preload("res://Assets/BYTEART/RADAR.png"),
preload("res://Assets/BYTEART/GERNADE.png")
]

var u_textures = [preload("res://Assets/BYTEART/ARMOR.png"),
preload("res://Assets/BYTEART/BOOTS.png"),
preload("res://Assets/BYTEART/BACKPACK.png")
]

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func update():
	for i in range(len(inventory["guns"])):	
		#print(str(inventory["guns"][i]))
		if inventory["guns"][i] != null:
			self.get_node("Inventory/Guns/Gun"+ str(i+1)).texture = textures[inventory["guns"][i]["gun_type"]-1][inventory["guns"][i]["level"]-1]
		else:
			self.get_node("Inventory/Guns/Gun" + str(i+1)).texture = null
	for i in range(len(inventory["consumables"])):
		if inventory["consumables"][i] != null:
			self.get_node("Inventory/Consumables/Consumable" + str(i)).texture = c_textures[inventory["consumables"][i]["consumable_type"]-1]
	for i in range(len(inventory["upgrades"])):
		if inventory["upgrades"][i] != null:
			self.get_node("Inventory/Upgrades/Upgrade" + str(i)).texture = u_textures[inventory["upgrades"][i]["upgrade_type"]-1]
	self.get_node("Inventory/Bars/Count/Background/Number").text = str(health)
	self.get_node("Inventory/Bars/Count2/Background2/Number").text = str(armor)
	self.get_node("Inventory/HBoxContainer/Label").text = str(money)
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
