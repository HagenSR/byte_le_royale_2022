extends MarginContainer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"\
var health = 0


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func update():
	self.get_node("Bars/Bar/Count/Background/Number").text = str(health)
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass
