# daw1230_agent.py
# A conversational agent that simulates a Starbucks customer

from re import *   # Loads the regular expression module.

def introduce():
    return """Hello! I'm Didi designed by Dan Wang, who can be reached at
daw123@uw.edu. Now I'm buying some coffee at Starbucks."""

def agentName():
    return "Didi"

Memory  = []
def respond(the_input):
    if match('bye',the_input):
            return 'Goodbye!'
    # MEMORY
    if the_input in Memory:
        return 'We have discussed this.'
    else:
        Memory.append(the_input)
    
    wordlist = split(' ',remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0]=wordlist[0].lower()
    # exchange 1st and 2nd person
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0]=mapped_wordlist[0].capitalize()

    if wordlist[0]=='':
        return ("Please say something."+punt())

    if wordlist[0:2] == ['i','am']:
        return("Please tell me why you are " +\
              stringify(mapped_wordlist[2:]) + '.')

    if wpred(wordlist[0]):
        return("You tell me " + wordlist[0] + ".")

    if wordlist[0:2] == ['i','have']:
        return("How long have you had " +\
              stringify(mapped_wordlist[2:]) + '.')
    
    if wordlist[0:2] == ['i','feel']:
        return("I sometimes feel the same way.")

    if 'morning' in wordlist:
        return("Good morning!")
            
    if 'yes' in wordlist:
        return("How can you be so sure?")

    if wordlist[0:2] == ['you','are']:
        return("Oh yeah, I am " +\
              stringify(mapped_wordlist[2:]) + '.')

    if verbp(wordlist[0]):
        return("Why do you want me to " +\
              stringify(mapped_wordlist) + '?')
         
    if wordlist[0:3] == ['do','you','think']:
        return("I think you should answer that yourself.")
        
    if wordlist[0:2]==['can','you'] or wordlist[0:2]==['could','you']:
        return("Perhaps I " + wordlist[0] + ' ' +\
              stringify(mapped_wordlist[2:]) + '.')

    if 'dream' in wordlist:
        return("For dream analysis see Freud.")
        
    if 'love' in wordlist:
        return("All's fair in love and war.")
        
    if 'no' in wordlist:
        return("Don't be so negative.")
        
    if 'maybe' in wordlist:
        return("Be more decisive.")
        
    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        return(stringify(mapped_wordlist) + '.')
    
    
punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:|\)") 
def remove_punctuation(text):
    'Returns a string without defined punctuations.'
    return sub(punctuation_pattern,'', text)

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}
def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

PUNTS = ['Please go on.',
         'Tell me more.',
         'I see.',
         'What does that indicate?',
         'But why be concerned about it?',
         'Just tell me how you feel.']

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]
