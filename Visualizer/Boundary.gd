extends Node2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var radius = 500

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _draw():
	draw_circle(Vector2(500.0, 500.0), 100, Color(255, 0, 0))

func update():
	radius -= 1
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
