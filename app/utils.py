from random import randint

def get_random_index(a, b):
    return randint(a, b)

def find(letter, word):
    pos = []
    for i, ltr in enumerate(word):
        if ltr == letter:
            pos.append(i)
    return pos        

def replace(letters, letter, replace):
    for i in range(0, len(letters)):
        for j in range(0, len(letters[i])):
            if letters[i][j] == letter:        
                letters[i][j] = replace 
             

def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def get_alphabet():
    return [['a','b','c','d','e','f','g','h','i','j'],['k','l','m','n','o','p','q','r'],['s','t','u','v','w','x','y','z']]

def prepare_word(secret_word):
    guessed_word = ''
    for c in secret_word:
        if c == ' ':
            guessed_word += ' '
        else:    
            guessed_word += '_'
    return guessed_word