# Part A
#1
def five_x_cubed_plus_2(x): return 5*x**3+2

#2
def triple_up(l):
    n = 3
    output = [l[i*n:(i + 1)*n] for i in range((len(l)+n-1)//n)]
    return output

#3
def mystery_code(input):
    key = -5
    output = ''
    for char in input:
        if char.isalpha():
            num = ord(char)
            num += key

            if char.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif char.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            output += chr(num)
        else:
            output += char
    return output.swapcase()

#4
def future_tense(stri):
    output = []
    for i in range(len(stri)):
        if stri[i] in ['is','am','are','were','was']:
            furt = ['will','be']
            output.extend(furt)
        elif stri[i] in ['eat','eats','ate']:
            furt = ['will','eat']
            output.extend(furt)
        elif stri[i] in ['go','goes','went']:
            furt = ['will','go']
            output.extend(furt)
        elif stri[i] in ['have','has','had']:
            furt = ['will','have']
            output.extend(furt)
        elif stri[i] in ['do','does','did']:
            furt = ['will','do']
            output.extend(furt)
        elif stri[i] in ['Today','Yesterday','Now']:
            furt = 'Tomorrow'
            output.append(furt)
        elif stri[i] in ['today','yesterday','now']:
            furt = 'tomorrow'
            output.append(furt)
        else:
            output.append(stri[i])
    return output
    
