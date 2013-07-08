import time
from googlevoice import Voice
from googlevoice.util import input

import modules.Groups

handlers = {}
handlers['group'] = modules.Groups.handleText

print "Handlers: %s"%handlers ###

def main():
	voice = Voice()
	voice.login()

	while 1:
		print "Starting loop\n" ### 
		for message in voice.inbox().messages:
			# Get text
			msg = message['messageText']
			phoneNumber = message['phoneNumber']
			
			# Pass to appropriate handler
			keyword = msg.split(" ")[0].lower()
			print "Keyword: %s\n\n"%keyword ###
			if keyword in handlers:
				replies = handlers[keyword](phoneNumber, msg)
			else:
				replies = {phoneNumber:"Command not found. Try these: %s"%(str(handlers.keys()))}			

			print "Replies: %s\n\n"%replies ###
			for phoneNum in replies:
				voice.send_sms(phoneNum, replies[phoneNum])	

			message.delete()
		time.sleep(1)

main()
