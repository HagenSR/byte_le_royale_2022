extends Camera2D


# Declare member variables here. Examples:
# var a = 2
# var b = "text"


# Called when the node enters the scene tree for the first time.
func _ready():
	self.make_current()



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
		if (Input.is_action_pressed("ui_page_down")):
			self.zoom.x += 0.05
			self.zoom.y += 0.05
		elif (Input.is_action_pressed("ui_page_up")):
			self.zoom.x -= 0.05
			self.zoom.y -= 0.05
		if(Input.is_action_pressed("ui_left")):
			self.position.x -= 5
		elif(Input.is_action_pressed("ui_right")):
			self.position.x += 5
		if(Input.is_action_pressed("ui_up")):
			self.position.y -= 5
		elif(Input.is_action_pressed("ui_down")):
			self.position.y += 5
