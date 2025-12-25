# Quiz 2
import string

def capitalize_title(title):
    exceptions = ['a', 'an', 'the', 'at', 'by', 'for', 'in', 'of',
                  'on', 'to', 'up', 'and', 'as', 'but', 'or', 'nor']
    
    words = title.split()
    result = []
    
    for word in words:
        clean_word = word.rstrip(string.punctuation)
        punct = word[len(clean_word):]  
        if clean_word.lower() in exceptions:
            new_word = clean_word.lower() + punct
            result.append(new_word)
            continue
        
        # Test for special characters
        length1 = len(clean_word.split('_'))
        length2 = len(clean_word.split('-'))
        length3 = len(clean_word.split('&'))
        
        if length1 == 1 and length2 == 1 and length3 == 1:
            # First letter capitalized
            if clean_word:
                new_clean = clean_word[0].upper() + clean_word[1:]
            else:
                new_clean = clean_word
            result.append(new_clean + punct)
        else:
            current = clean_word
            if '_' in current:
                part = []
                for i in current.split('_'):
                    if i:  
                        i = i[0].upper() + i[1:]
                    part.append(i)
                current = '_'.join(part)
            if '-' in current:
                part = []
                for i in current.split('-'):
                    if i:
                        i = i[0].upper() + i[1:]
                    part.append(i)
                current = '-'.join(part)
            if '&' in current:
                part = []
                for i in current.split('&'):
                    if i:
                        i = i[0].upper() + i[1:]
                    part.append(i)
                current = '&'.join(part)
            result.append(current + punct)
    
    return ' '.join(result)

# Test the function
title = 'Welcome to MSDM_5002 of data-driven modeling \
for MSc students offered by phys&math Department in UST. \
We will continue to learn NumPy and MatPlotLib.'

capitalized = capitalize_title(title)
print("Capitalized:", capitalized)