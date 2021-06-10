# daw1230_agent.py
# A conversational agent that simulates a Starbucks customer

from re import *   # Loads the regular expression module.
from random import choice

def introduce():
    return """Hello! I'm Didi designed by Dan Wang, who can be reached at
daw123@uw.edu. Now I'm buying some coffee at Starbucks."""

def agentName():
    return "Didi"

Memory  = ''
def respond(the_input):
    if match('bye',the_input):
        # response to bye
        return 'Goodbye!'
    
    wordlist = split(' ',remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0]=wordlist[0].lower()

    if wordlist[0:2] == ['i','am']:
        # CHOICE choose one coffee type
        coffee = choice(['drip', 'iced', 'Espresso', 'Latte'])
        return("Hello, "+wordlist[2]+". Can I have "+coffee+" coffee?")
    elif 'syrup' in wordlist:
        # CYCLE FEATURE choose one syrup type
        return('Let me think about it. Can I have some '+punt()+" syrup?")
    elif 'tea' in wordlist:
        # CYCLE FEATURE choose another syrup type in a cycle
        return("Got it! How about some "+punt()+" syrup?")
    elif 'size' in wordlist:
        global Memory
        # CHOICE choose cup size and use Memory to store cup size
        size = choice(['small', 'medium', 'large'])
        Memory += size
        size = size.capitalize()
        return(size+" size please.")
    elif 'name' in wordlist:
        # answer to the question of asking name
        return("I am Didi. May I ask how long do I have to wait?")
    elif 'pay' in wordlist:
        # MEMORY ask for price of the coffee with a certain size
        return("How much is the "+Memory+" coffee?")
    elif 'dollars' in wordlist:
        # CHOICE choose a payment method
        return("Sure. I'll use "+choice(['credit', 'cash'])+".")
    elif 'receipt' in wordlist:
        # skip receipt and ask as an expedited case
        return("That's OK. I don't need the receipt. One more thing. I'm heading to a meeting. "+
               "Would you mind making the coffee a little faster?")
    elif 'worry' in wordlist:
        # response to "don't worry"
        return("Thank you so much.")
    elif wordlist[0:3] == ['you','are','welcome']:
        # response to "you are welcome"
        return("Have a good day!")
    elif 'rain' in wordlist:
        # response to "rain"
        return("I don't like raining.")
    elif 'seattle' in wordlist:
        # response to "seattle"
        return("The city is cool.")
    elif 'morning' in wordlist:
        # response to "morning"
        return("Good morning!")
    elif 'afternoon' in wordlist:
        # response to "afternoon"
        return("Good afternoon!")
    else:
        return("Bye.")   
    
punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:|\)") 
def remove_punctuation(text):
    'Returns a string without defined punctuations.'
    return sub(punctuation_pattern,'', text)

PUNTS = ['vanilla','lemonade']

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 2]
