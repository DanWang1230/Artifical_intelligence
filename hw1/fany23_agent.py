from string import punctuation
import re
import random

'''
MEMORY
Using two map to remember the order detail and the customer information.
'''
drink = {"type" : "", "size" : "", "syrup" : ""}
mem = {"name": "", "paymnet" : ""}

def agentName():
	return "Buck"

def introduce():
	intro = "My name is Buck, I am a Barista in Starbucks located in the Suzallo Library \n\
I was programmed by Yu Fan (UWNetID: fany23). \n\
I hope I can get the right coffee for you today. \n\
Don't hesitate to ask for a personalized drink. \n\
So what can I get for you today?"
	return intro

def respond(str):
	r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
	wordlist = r.split(str)
	wordlist = [word.lower() for word in wordlist]
	if wordlist[0:2] == ["i", "am"]:
		mem["name"] = wordlist[2]
	if wordlist[0] == "":
		# RANDOM FEATURE
		return "I am Buck. " + randomIntroduction()
	if "coffee" in wordlist and drink["type"] == "":
		# CYCLE FEATURE
		# MEMORY FEATURE
		if drink["type"] == "":
		 	drink["type"] = "coffee"
		return "Sure " + mem["name"] + ". How about add some " + cycleSyrup() + " syrup?"
	if "lemonade" in wordlist:
		# CYCLE FEATURE
		# MEMORY FEATURE
		if drink["type"] == "tea":
			drink["syrup"] = "lemonade"
			return "No Problem."
		return "Sorry, this is for tea. We have " + cycleSyrup() + " for coffee."

	if "vanilla" in wordlist:
		# MEMORY FEATURE
		if drink["type"] == "coffee":
			drink["syrup"] = "vanilla"
			return "Copy that. Whcih size do you prefer？"
		return "This is for coffee, what about some lemonade?"
	if "caramel" in wordlist:
		# MEMORY FEATURE
		if drink["type"] == "coffee":
			drink["syrup"] = "caramel"
			return "Copy that. Whcih size do you prefer？"
		return "This is for coffee, what about some lemonade?"
	if wordlist[0:2] == ["how", "much"]:
		# MEMORY FEATURE
		if drink["size"] == "small":
			return "2 dollars for small."
		if drink["size"] == "medium":
			return "4 dollars for medium."
		if drink["size"] == "large":
			return "6 dollars for large."
		if wordlist[2] == "coffee" or wordlist[2] == "tea":
			return "Which size?"
		return "It is not avaliable yet."

	if "small" in wordlist:
		drink["size"] = "small"
		return "Sure, can I have your name?"
	if "medium" in wordlist:
		drink["size"] = "medium"
		return "Sure, can I have your name?"
	if "large" in wordlist:
		drink["size"] = "large"
		return "Sure, can I have your name?"
	if "wait" in wordlist:
		# CYCLE FEATURE
		return waitCycle() + " Would you like to pay with " + payCycle() + " ?";
	if "cash" in wordlist:
		# MEMORY FEATURE
		mem["paymnet"] = "cash"
		if drink["type"] == "":
			return "You have not ordered yet."
		return "Here is your receipt and your " + drink["syrup"] + " " + drink["type"] + "."
	if "card" in wordlist:
		# MEMORY FEATURE
		mem["paymnet"] = "card"
		if drink["type"] == "":
			return "You have not ordered yet."
		return "Here is your " + drink["syrup"] + " " + drink["type"] + "."
	if "hurry" in wordlist or "faster" in wordlist:
		# RANDOM FEATURE
		return "Do not worry. " + randomWords()
	if "thank" in wordlist or "thanks" in wordlist:
		# MEMORY FEATURE
		if drink["type"] == "":
			return "You are welcome!"
		return "You are welcome! Here is your " + drink["type"] + ". "
	if wordlist[0] == "what":
		# MEMORY FEATURE
		if drink["type"] == "coffee" or drink["type"] == "tea":
			return "You just ordered " + drink["type"] + "."
	if "no" in wordlist:
		return "Let me check, could you please repeat your order? Tea or Coffee."
	if "tea" in wordlist and drink["type"] == "":
		drink["type"] = "tea"
		return "Sure. Whant some lemonade?"
	if wordlist[0:4] == ["have", "a", "good", "day"]:
		return "you too"
	return introduce();




'''
RANDOM
'''
random_introduction = ["Nice to see you.",
						"Nice weather isn't it?",
						"Do you want some drinks?"]
def randomIntroduction():
	curr = random.randint(0, 2)
	return random_introduction[curr]

some_random_sentense = ["It will be good.", 
						"I'm pro.", 
						"Count on me, you will like it.", 
						"Good coffee, good day."]
def randomWords():
	curr = random.randint(0, 3)
	return some_random_sentense[curr]

'''
CYCLE
'''
wait_index = 0
waitlist = ["It is busy today, you may have to wait 20 minitus.",
			"Just 2 minitus, it will be ready for you.",
			"Em, around 5 minitus."]
def waitCycle():
	global wait_index
	global waitlist
	wait_index = (wait_index + 1) % 3
	return waitlist[wait_index]

style_index = 0
style = ["lemonade", "caramel", "vanilla"]
def cycleSyrup():
	global style_index
	global style
	style_index = (style_index + 1) % 3
	return style[style_index]


pay_index = 0
payments = ["credit card", "cash", "check"]
def payCycle():
	global pay_index
	global payments
	pay_index = (pay_index + 1) % 3
	return payments[pay_index]
