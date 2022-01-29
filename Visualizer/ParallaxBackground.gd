extends ParallaxBackground


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
onready var tile = preload("res://Tile.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	for i in range(32):
		for j in range(32):
			var new_tile = tile.instance()
			new_tile.position = (Vector2(float((1000/32)*i), float(j*(1000/32))))

	#self.get_node("Sprite").scale.x = width/16
	#self.get_node("Sprite").scale.y = height/16
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
