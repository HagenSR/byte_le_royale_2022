extends Node2D

var selected_menu = 0
onready var global = get_node("/root/Global")

func change_menu_color():
	$Delay.color = Color.gray
	$Tick.color = Color.gray
	$Start.color = Color.gray
	
	match selected_menu:
		0:
			$Delay.color = Color.greenyellow
		1:
			$Tick.color = Color.greenyellow
		2:
			$Start.color = Color.greenyellow

func _ready():
	change_menu_color()

func _input(event):
	if Input.is_action_just_pressed("ui_down"):
		selected_menu = (selected_menu + 1) % 3;
		change_menu_color()
	elif Input.is_action_just_pressed("ui_up"):
		if selected_menu > 0:
			selected_menu = selected_menu - 1
		else:
			selected_menu = 2
		change_menu_color()
	elif Input.is_action_just_pressed("ui_accept"):
		print(str(selected_menu))
		match selected_menu:
			2:
				if int(self.get_node("Delay/TextEdit").text) > 0:
					global.speed = int(self.get_node("Delay/TextEdit").text)
				if int(self.get_node("Tick/TextEdit").text) > 0:
					global.tick = int(self.get_node("Tick/TextEdit").text) + 2
				# New game
				get_tree().change_scene("res://Main.tscn")
				self.hide()
