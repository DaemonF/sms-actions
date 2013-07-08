def fix_phone_num(phone_num):
	if len(phone_num) == 10:
		try:
			int(phone_num)
			is_good = True
		except:
			is_good = False
		if is_good:
			return "+1" + phone_num
		#return "ERROR: 10 length but isn't all numbers"
		return False
	elif len(phone_num) == 11:
		if phone_num[0] == "1":
			try:
				int(phone_num)
				is_good = True
			except:
				is_good = False
			if is_good:
				return "+" + phone_num
			#else:
			#	return "ERROR: phone # part isn't all numbers"
		#return "ERROR: 11 length but doesn't start with 1"
		return False
	elif len(phone_num) == 12:
		if phone_num[0] == "+" and phone_num[1] == "1":
			try:
				int(phone_num[1:])
				is_good = True
			except:
				is_good = False
			if is_good:
				return phone_num
			#else:
			#	return "ERROR: phone # part isn't all numbers"
		#return "ERROR: 12 length but doesn't start with +1"
		return False
	else:
		#return "ERROR: Not of 10, 11, or 12 length."
		return False