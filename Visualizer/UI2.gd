extends CanvasLayer


var health = 0
var shield = false
var inventory = []
var armor = 0
var money = 0

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
		if inventory["guns"][i] != null:
			self.get_node("MarginContainer/Inventory/Guns/Gun"+ str(i+1)).texture = textures[inventory["guns"][i]["gun_type"]-1][inventory["guns"][i]["level"]-1]
			#self.get_node("MarginContainer/Inventory/Guns/Gun"+ str(i+1)).rect_scale.x = 2
			#self.get_node("MarginContainer/Inventory/Guns/Gun"+ str(i+1)).rect_scale.y = 2
		else:
			self.get_node("MarginContainer/Inventory/Guns/Gun" + str(i+1)).texture = null
	for i in range(len(inventory["consumables"])):
		if inventory["consumables"][i] != null:
			self.get_node("MarginContainer/Inventory/Consumables/Consumable" + str(i+1)).texture = c_textures[inventory["consumables"][i]["consumable_type"]-1]
			#self.get_node("MarginContainer/Inventory/Consumables/Consumable" + str(i+1)).rect_scale.x = 2
			#self.get_node("MarginContainer/Inventory/Consumables/Consumable" + str(i+1)).rect_scale.y = 2
		else:
			self.get_node("MarginContainer/Inventory/Consumables/Consumable" + str(i+1)).texture = null
	for i in range(len(inventory["upgrades"])):
		if inventory["upgrades"][i] != null:
			self.get_node("MarginContainer/Inventory/Upgrades/Upgrade" + str(i+1)).texture = u_textures[inventory["upgrades"][i]["upgrade_type"]-1]
			#self.get_node("MarginContainer/Inventory/Upgrades/Upgrade" + str(i+1)).rect_scale.x = 2
			#self.get_node("MarginContainer/Inventory/Upgrades/Upgrade" + str(i+1)).rect_scale.y = 2
		else:
			self.get_node("MarginContainer/Inventory/Upgrades/Upgrade" + str(i+1)).texture = null
	self.get_node("MarginContainer/Inventory/Bars/Count/Background/Number").text = str(health)
	self.get_node("MarginContainer/Inventory/Bars/Count2/Background2/Number").text = str(armor)
	self.get_node("MarginContainer/Inventory/Bars2/Count/Background/Number").text = str(money) 
	if shield:
		self.get_node("MarginContainer/Inventory/Bars/Count2/Background2").show()
	else:
		self.get_node("MarginContainer/Inventory/Bars/Count2/Background2").show()

