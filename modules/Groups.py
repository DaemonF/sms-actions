import os
import json
import smsUtils

data_folder = os.path.join(os.path.dirname(__file__), "groups-data" + os.sep)

def handleText(sender_num, sender_msg):
	msg = sender_msg.split(" ")
	if msg[1] == "create":
		return create(sender_num, msg[2])
	elif msg[1] == "read":
		return read(sender_num, msg[2])
	elif msg[1] == "update":
		return update(sender_num, msg[2], msg[3], msg[4], msg[5])
	elif msg[1] == "delete":
		return delete(sender_num, msg[2], msg[3])
	else:
		grp = msg[1]
		msg = " ".join(msg[2:])
		return send_msg(sender_num, grp, msg)


def send_msg(sender_num, group_num, msg):
	filename = group_exists(group_num)
	if filename:
		my_dict = {}
		group_file = open(filename, "r")
		for line in group_file:
			obj = json.loads(line)
			if obj[0] != sender_num:
				my_dict[obj[0]] = msg
		group_file.close()
		return my_dict
	else:
		return {sender_num : "Group does not exist."}
		

"""	while True:
		command = raw_input("Do what? ")
		if command == "q":
			break
		elif command == "create":
			g_n = raw_input("group_num ")
			create(g_n)
		elif command == "read":
			g_n = raw_input("group_num ")
			read(g_n)
		elif command == "update":
			g_n = raw_input("group_num ")
			p_n = raw_input("phone_num ")
			f_n = raw_input("first_name ")
			l_n = raw_input("last_name ")
			update(g_n, p_n, f_n, l_n)
		elif command == "delete":
			g_n = raw_input("group_num ")
			index = raw_input("index ")
			delete(g_n, index)
"""

def group_exists(group_num):
	filename = data_folder + "group_" + group_num + ".txt"
	if os.path.isfile(filename):
		return filename
	else:
		return False

def create(sender_num, group_num):
	exists = group_exists(group_num)
	if exists:
		return {sender_num : "Group already exists."}
	else:
		filename = data_folder + "group_" + group_num + ".txt"
		new_file = open(filename, "w")
		new_file.close()
		return {sender_num : "Group created."}

def read(sender_num, group_num):
	filename = group_exists(group_num)
	if filename:
		group_file = open(filename, "r")
		group_members = ""
		for line in group_file:
			obj = json.loads(line)
			group_members += obj[1], obj[2], ":", obj[0] + "\n"
		group_file.close()
		return {sender_num : group_members}
	else:
		return {sender_num : "Group does not exist."}

def update(sender_num, group_num, phone_num, first_name, last_name):
	filename = group_exists(group_num)
	if filename:
		fixed_phone_num = smsUtils.fix_phone_num(phone_num)
		if fixed_phone_num:
			obj = [fixed_phone_num, first_name, last_name]
			json_obj = json.dumps(obj)
			group_file = open(filename, "r+")
			exists = False
			for line in group_file:
				if json_obj == line:
					exists = True
			if not exists:
				group_file.write(json_obj + "\n")
			group_file.close()
			if exists:
				return {sender_num : fixed_phone_num + " already in group."}
			else:
				return {sender_num : fixed_phone_num + " added to group."}
		else:
			return {sender_num : "Invalid phone number."}
	else:
		return {sender_num : "Group does not exist."}

def delete(sender_num, group_num, index):
	filename = group_exists(group_num)
	if filename:
		index = int(index)
		index -= 1
		group_updated = ""
		group_file = open(filename, "r")
		for line in group_file:
			if index == 0:
				obj = json.loads(line)
				deleted = obj[1], obj[2], ":", obj[0]
				delete_number = obj[0]		
			if index != 0:
				group_updated += line
			index -= 1
		group_file.close()
		group_file = open(filename, "w")
		group_file.write(group_updated)
		group_file.close()
		return {sender_num: deleted + " has been removed from group " + group_num + ".", deleted_number : sender_num + " has deleted you from group " + group_num + "."}
	else:
		return {sender_num : "Group does not exist."}
