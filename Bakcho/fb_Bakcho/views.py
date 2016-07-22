from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import MySQLdb

# Create your views here.
class BakchoView(generic.View):
	
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == '5432167890':
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Error, invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		counts = dict()
		max = 0
		maxTextID = 0
		db = MySQLdb.connect("localhost", "root", "root", "hackday")
		cursor = db.cursor()
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					tokens = message['message']['text'].split()
					for t in tokens:
						sql = "select textID from invertedIndex where keyword = '%s'" % t
						try:
							cursor.execute(sql)
							results = cursor.fetchall()
							for row in results:
								textID = row[0]
								print "textID %d" % textID
								counts[textID] = counts.get(textID, 0) + 1
								if(max < counts.get(textID, 0)):
									max = counts.get(textID, 0)
									maxTextID = textID
						except:
							print "Error1: unable to fetch data"

					sql = "select text from textDescription where textID = '%d'" % maxTextID
					try:
						cursor.execute(sql)
						results = cursor.fetchall()
						for row in results:
							text1 = row[0]
					except:
						print "Error: unable to fetch data"
					db.close()
					print text1
					post_facebook_message(message['sender']['id'], text1)
		return HttpResponse()


def post_facebook_message(fbid, recevied_message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAZAQbUnxhbcBANlEiKtXb6o97ElUGs0ZB4twcOzO0qukVH2amRAZB39ZArmdBLFKZBrEO9xZAWMkjtjL8CJwIxfpucLvjhCrL61LlkRcopVMXpiMVyILvW2QohyxfnNwQzKQyyhsoNwnLTpW0o9XLXXFcYbkC1OwqYYJvrx2wUwZDZD'
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print(status.json())