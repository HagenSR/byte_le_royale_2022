extends Node2D

onready var log_path = "./logs"
onready var player = preload("res://Player.tscn")
onready var wall = preload("res://Wall.tscn")
onready var door = preload("res://Door.tscn")
onready var money = preload("res://Money.tscn")
onready var gun = preload("res://Gun.tscn")
onready var consumable = preload("res://Consumable.tscn")
onready var ray = preload("res://Ray.tscn")
onready var teleporter = preload("res://Teleporter.tscn")

onready var tile = preload("res://Tile.tscn")
onready var boundary = preload("res://Boundary.tscn")
onready var gui = preload("res://GUI.tscn")
onready var gui2 = preload("res://GUI2.tscn")
onready var grenade = preload("res://Grenade.tscn")

onready var files = load_json(log_path)

onready var map_objects = {}
onready var players = {}
onready var rays = []

onready var log_i = 2


func load_json(path):
	var f = []
	var dir = Directory.new()
	dir.open(path)
	dir.list_dir_begin()
	while true:
		var file = dir.get_next()
		if file == "":
			break
		elif not file.begins_with(".") and not file == "turn_logs.json":
			if file == "game_map.json":
				f.insert(0, file)
			elif file == "results.json":
				if f.size() > 0:
					f.insert(1, file)
				else:
					f.insert(0,file)
			else:
				f.append(file)
	dir.list_dir_end()
	return f

func instantiate(object):
	var ids = []
	var out = null
	if object["object_type"] == 13:
		if not object["id"] in map_objects.keys():
			var new_wall = wall.instance()
			new_wall.id = object["id"]
			new_wall.health = object["health"]
			new_wall.collidable = object["collidable"]
			new_wall.destructible = object["destructible"]
			new_wall.width = object["hitbox"]["width"]
			new_wall.height = object["hitbox"]["height"]
			# TODO: Convert to float
			var pos = object["hitbox"]["position"]
			new_wall.game_position = [(pos[0]), (pos[1])]
			new_wall.update()
			ids.append(new_wall.id)
			out = new_wall
		else:
			return null
	elif object["object_type"] == 15:
		if not object["id"] in map_objects.keys():
			var new_door = door.instance()
			new_door.id = object["id"]
			new_door.opening_speed = object["opening_speed"]
			new_door.open_state = object["open_state"]
			new_door.width = object["hitbox"]["width"]
			new_door.height = object["hitbox"]["height"]
			var pos = object["hitbox"]["position"]
			new_door.game_position = [(pos[0]), (pos[1])]
			ids.append(new_door.id)
			out = new_door
		else:
			return null
	elif object["object_type"] == 18:
		if not object["id"] in map_objects.keys():
			var new_money = money.instance()
			new_money.id = object["id"]
			new_money.amount = object["amount"]
			var pos = object["hitbox"]["position"]
			new_money.game_position = [(pos[0]), (pos[1])]
			new_money.update()
			ids.append(new_money.id)
			out = new_money
	elif object["object_type"] == 12:
		if not object["id"] in map_objects.keys():
			var new_gun = gun.instance()
			new_gun.id = object["id"]
			new_gun.gun_type = object["gun_type"]
			new_gun.level = object["level"]
			new_gun.pattern = object["pattern"]
			new_gun.damage = object["damage"]
			new_gun.fire_rate = object["fire_rate"]
			new_gun.gun_range = object["range"]
			new_gun.mag_size = object["mag_size"]
			new_gun.width = object["hitbox"]["width"]
			new_gun.height = object["hitbox"]["height"]
			var pos = object["hitbox"]["position"]
			new_gun.game_position = [(pos[0]), (pos[1])]
			#new_gun.mag_ammo = object["mag_ammo"]
			ids.append(new_gun.id)
			out = new_gun
	elif object["object_type"] == 17:
		if not object["id"] in map_objects.keys():
			var new_consumable = consumable.instance()
			new_consumable.consumable_type = object["consumable_type"]
			new_consumable.width = object["hitbox"]["width"]
			new_consumable.height = object["hitbox"]["height"]
			var pos = object["hitbox"]["position"]
			new_consumable.game_position = [(pos[0]), (pos[1])]
			new_consumable.update()
			self.add_child(new_consumable)
			ids.append(new_consumable.id)
			out = new_consumable
	elif object["object_type"] == 19:
		if not object["id"] in map_objects.keys():
			var new_teleporter = teleporter.instance()
			new_teleporter.width = object["hitbox"]["width"]
			new_teleporter.height = object["hitbox"]["height"]
			new_teleporter.countdown = object["countdown"]
			new_teleporter.turn_cooldown = object["turn_cooldown"]
			var pos = object["hitbox"]["position"]
			new_teleporter.game_position = [(pos[0]), (pos[1])]
			new_teleporter.update()
			
			ids.append(new_teleporter.id)
			out = new_teleporter
	elif object["object_type"] == 7:
		if not object["id"] in map_objects.keys():
			var new_grenade = grenade.instance()
			new_grenade.fuse_time = object["fuse_time"]
			new_grenade.width = object["hitbox"]["width"]
			new_grenade.height = object["hitbox"]["height"]
			var pos = object["hitbox"]["position"]
			new_grenade.game_position = [(pos[0]), (pos[1])]
			new_grenade.update()
			self.add_child(new_grenade)
			ids.append(new_grenade.id)
			out = new_grenade
	#for id in map_objects.keys():
		#if not id in ids:
			#map_objects.erase(id)
	return out

func initialize(results, game_map):
	for player_log in results["players"]:
		var new_player = player.instance()
		new_player.id = player_log["id"]
		new_player.team_name = player_log["team_name"]
		players[new_player.id] = new_player
		self.add_child(new_player)
	for partition_set in game_map["game_map"]["partition"]["partition_grid"]:
		for partition in partition_set:
			for object in partition:
				var obj = instantiate(object)
				if obj != null:
					map_objects[obj.id] = obj
					self.add_child(obj)
	return [players, map_objects]
	
func run_tick(json_log):
	var clients = json_log["clients"]
	for client in clients:
		players[client["id"]].heading = client["shooter"]["heading"]
		players[client["id"]].health = client["shooter"]["health"]
		players[client["id"]].speed = client["shooter"]["speed"]
		players[client["id"]].money = client["shooter"]["money"]
		players[client["id"]].armor = client["shooter"]["armor"]
		players[client["id"]].width = client["shooter"]["hitbox"]["width"]
		players[client["id"]].height = client["shooter"]["hitbox"]["height"]
		players[client["id"]].game_position = client["shooter"]["hitbox"]["position"]

		players[client["id"]].inventory = client["shooter"]["inventory"]
	
	for nray in json_log["game_map"]["ray_list"]:
		var r = ray.instance()
		var origin = nray["origin"]
		var endpoint = nray["endpoint"]
		r.add_point((Vector2(float(2*origin[0]), float(2*origin[1]))))
		r.add_point((Vector2(float(2*endpoint[0]), float(2*endpoint[1]))))
		rays.append(r)

	for partition_set in json_log["game_map"]["partition"]["partition_grid"]:
		for partition in partition_set:
			for object in partition:
				var tmp = instantiate(object)
				if not tmp == null:
					if not tmp.id in map_objects.keys():
						self.add_child(tmp)
					map_objects[tmp.id] = tmp
					
func tiling():
	for i in range(33):
		for j in range(33):
			var new_tile = tile.instance()
			new_tile.position = (Vector2(float((1000/32)*i), float(j*(1000/32))))
			self.add_child(new_tile)

#func move_boundary(tick):
#	draw_circle(Vector2(500.0, 500.0), 600-tick, Color(255, 0, 0))
	
# Called when the node enters the scene tree for the first time.
func _ready():
	var game_boundary = boundary.instance()
	self.add_child(game_boundary)
	tiling()
	var ui1 = gui.instance()
	self.add_child(ui1)
	var ui2 = gui2.instance()
	self.add_child(ui2)
	load_json(log_path)
	var file = File.new()
	files.sort()
	print(str(files))
	file.open(log_path + "/" + "results.json", File.READ)
	print(str(files[1]))
	var file_text = file.get_as_text()
	var results = parse_json(file_text)
	file.close()
	file.open(log_path + "/" + "game_map.json", File.READ)
	file_text = file.get_as_text()
	file.close()
	var game_map = parse_json(file_text)
	initialize(results, game_map)
	files.sort()
	
	for i in range(2, len(files)):
		print(str(i))
		for r in rays:
			self.remove_child(r)
		rays.clear()
		file = File.new()
		file.open(log_path + "/" + files[i], File.READ)
		file_text = file.get_as_text()
		var json_log = parse_json(file_text)

		run_tick(json_log)

		ui1.health = players.values()[0].health
		ui1.inventory = players.values()[0].inventory
		ui2.health = players.values()[1].health
		ui2.inventory = players.values()[1].inventory
		ui2.inventory = players.values()[1].inventory
		ui1.update()
		ui2.update()

		for object in map_objects.values():
			object.update()
		for p in players.values():
			p.update()
		for ray in rays:
			self.add_child(ray)			
		game_boundary.update()
		var t = Timer.new()
		t.set_wait_time(.5)
		t.set_one_shot(true)
		self.add_child(t)
		t.start()
		yield(t, "timeout")
		t.queue_free()
