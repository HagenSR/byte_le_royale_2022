extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var radius = 478.5533905932738

# Called when the node enters the scene tree for the first time.
func _ready():
	
	self.position = (Vector2(500.0, 500.0))
	#self.get_node("Sprite").scale.x = (1/472)
	#self.get_node("Sprite").scale.y = (1/472)

#func _draw():
#	draw_circle(Vector2(500.0, 500.0), 100, Color(255, 0, 0))

func update():
	self.position = (Vector2(500.0, 500.0))
	#self.get_node("Sprite").scale = Vector2(1, 1)
	print(str(float(radius)/472))
	self.get_node("Sprite").scale = Vector2(float(4*radius)/472, float(4*radius)/472)
	radius -= 5

# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
