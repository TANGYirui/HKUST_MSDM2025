# -*- coding: utf-8 -*-
'''
@author: Junwei Liu
Question: Capitalize all words in a title entered, except a, an, the, at, by, for, in, of, on, to, up, and, as, but, or, and nor. Your output should look like as following.

Enter a title: Welcome to MSDM_5002 of data-driven modeling for master students offered by phys&math department in UST. We will continue to learn NumPy.
Capitalized: Welcome to MSDM_5002 of Data-Driven Modeling for Master Students Offered by Phys&Math Department in UST. We Will Continue to Learn NumPy.
'''


sep_words = ['a','an','the','at','by','for','in','of',\
             'on','to','up','and','as','but','or','nor']
# message = input('Enter a title: ')

# message = 'Welcome to the world of data-driven modeling \
# for MSc students offered by UST in a great and \
# green campus on the hill'
    
    
# message = 'Welcome to the world of data-driven modeling \
# for master students offered by HK-UST'

# message = 'Welcome to the world of data-driven modeling \
# for master students offered by dept-of-phys&math/HKUST'

# message = 'Welcome to MSDM_5002 for DDM master-students \
# offered by math&phys of UST@HK.\
# We have learned NumPy!'

# message = 'Welcome to MSDM_5002 for DDM master-students \
# offered by math&phys Of@UST@HK. \
# We have learned NumPy!'


message = 'Welcome To MSDM_5002 of data-driven modeling \
for MSc students offered by phys&math Department in UST. \
We will continue to learn NumPy and MatPlotLib.'

message = 'Welcome to MSDM_5002 of data-driven modeling \
for MSc students offered by phys&math Department in UST. \
We will continue the in-depth study'


# message_correct='Welcome to MSDM_5002 of Data-Driven Modeling \
# for MSc Students Offered by Phys&Math Department in UST. \
# We Will Continue to Learn NumPy and MatPlotLib.'

############# Example codes 0, correct??
msg_final0=message.title()
print("INPUT :",message)
print("OUTPUT:",msg_final0)

print('\n'*2)


print('Example codes 1')
############# Example codes 1, correct??
### deal with special words like "and"
msg = message.split()
msg_list = []
for word in msg:
    if word.lower() in sep_words:
        word = word.lower()
    else:
        # word = word.capitalize() #correct?
        word = word.title()
    msg_list.append(word)

msg_final1 = ' '.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final1)

print('\n'*2)

print('Example codes 2')
# ############# Example codes 2, correct??
### deal with "UST"
msg = message.split()
msg_list = []
for word in msg:
    
    if word.lower() in sep_words:
        word = word.lower()
    else:
        if word.upper() != word:  
            word = word.title()
        # if not word.isupper():
            # print(word)
            # word = word.capitalize() #correct?
            
    msg_list.append(word)

msg_final2 = ' '.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final2)

print('\n'*2)

print('Example codes 3')
############# Example codes 3, correct??
### deal with "MSc"
msg = message.split()
msg_list = []
for word in msg:
    if word.lower() not in sep_words:
        word_tmp = word.title()
        word=word_tmp[0]+word[1:len(word)] 
        ### is this good? or the following one better?
        # word_tmp2=word_tmp[0]+word[1:len(word)] 
        msg_list.append(word)
    else:
        msg_list.append(word.lower())

msg_final3 = ' '.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final3)

print('\n'*2)

print('Example codes 4')
############# Example codes 4, correct??
### deal with data-driven and phys&math
msg = message.split()
msg_list = []
for word in msg:
    if word.lower() not in sep_words:
        word_tmp = word.title()
        word=word_tmp[0]+word[1:len(word)]
    char='-'
    if word.find(char) != -1:
        word_list=word.replace(char,' ').split()
        # word_list=word.split(char)
        word2_list=[]
        for word2 in word_list:
            if word2.lower() not in sep_words:
                word2_tmp = word2.title()
                word2=word2_tmp[0]+word2[1:len(word)]
            word2_list.append(word2)
        word=char.join(word2_list)
    char='&'
    if word.find(char) != -1:
        word_list=word.replace(char,' ').split()
        # word_list=word.split(char)
        word2_list=[]
        for word2 in word_list:
            if word2.lower() not in sep_words:
                word2_tmp = word2.title()
                word2=word2_tmp[0]+word2[1:len(word)]
            word2_list.append(word2)
        word=char.join(word2_list)
    msg_list.append(word)
msg_final4 = ' '.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final4)
print('\n'*2)


print('Example codes 5')
############ Example codes 5. 
#Treat old and new problems in the way
msg = message.split()
msg_list = []
for word in msg:
    if word.lower() not in sep_words:
        word_tmp = word.title()
        word=word_tmp[0]+word[1:len(word)]
    msg_list.append(word)

msg_final5 = ' '.join(msg_list)

msg = msg_final5.split('&')
msg_list = []
for word in msg:
    if word.lower() not in sep_words:
        word_tmp = word.title()
        word=word_tmp[0]+word[1:len(word)]
    msg_list.append(word)
msg_final5 = '&'.join(msg_list)

msg = msg_final5.split('-')
msg_list = []
for word in msg:
    if word.lower() not in sep_words:
        word_tmp = word.title()
        word=word_tmp[0]+word[1:len(word)]
    msg_list.append(word)
msg_final5 = '-'.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final5)
print('\n'*2)

print('Example codes 6')
############# Example codes 6. More organized.
msg_final6=message
all_char='- &'
for char in all_char:
    msg = msg_final6.split(char)
    msg_list = []
    for word in msg:
        if word.lower() not in sep_words:
            word_tmp = word.title()
            word=word_tmp[0]+word[1:len(word)]
        msg_list.append(word)
    msg_final6 = char.join(msg_list)
print("INPUT :",message)
print("OUTPUT:",msg_final6)
print('\n'*2)

print('Example codes 7')
############# Example codes 7. Use function
def change_upper(message, split_char):
    msg = message.split(split_char)
    msg_list = []
    for word in msg:
        if word.lower() not in sep_words:
            word_tmp = word.title()
            word=word_tmp[0]+word[1:len(word)]
        msg_list.append(word)
    return char.join(msg_list)

msg_final7=message
all_char='-& #*'
for char in all_char:
    msg_final7=change_upper(msg_final7, char)
print("INPUT :",message)
print("OUTPUT:",msg_final7)
print('\n'*2)

print('Example codes 8')
######### Example codes 8: rewrite functions by yourself
def change_upper(message, char):
    tmp=message;     char_pos=[]
    if tmp.find(char) != -1:
        char_pos.append(tmp.find(char))
        tmp=message[char_pos[-1]+1:len(message)]
    while tmp.find(char) != -1:
        char_pos.append(char_pos[-1]+tmp.find(char)+1)
        tmp=message[char_pos[-1]+1:len(message)]

    #tmp = message.title()  ##write the title() by yourself
    mlist=list(message)
    for n in char_pos:
        mlist[n+1]=mlist[n+1].upper()
        
    # tmp=''.join(mlist) ##write the join() by yourself
    tmp=''
    for ctmp in mlist: 
        tmp += ctmp
        
    # msg_list = tmp.split(char) #write the split()
    msg_list=[]; nstart=0
    for nend in char_pos:
        msg_list.append(tmp[nstart:nend])
        nstart=nend+1
    msg_list.append(tmp[nstart:])
    
    ##check whether the words belong to sep_words
    New_list=[]
    for word in msg_list:
        if word.lower() in sep_words:
            New_list.append(word.lower())
        else:
            New_list.append(word)
    # tmp=char.join(New_list) ##write the join() by yourself
    tmp=New_list[0]
    for ctmp in New_list[1:]: 
        tmp += char+ctmp
    return tmp

msg_final8=message
all_char='-&@ '
for char in all_char:
    msg_final8=change_upper(msg_final8, char)

print("INPUT :",message)
print("OUTPUT:",msg_final8)

# print('\n'*2)

######### Example codes 8-1: rewrite functions by yourself
def change_upper(message, char):
    ### this part is improved compare version 8
    tmp=message;     char_pos=[-1]
    while tmp.find(char) != -1:
        char_pos.append(char_pos[-1]+tmp.find(char)+1)
        tmp=message[char_pos[-1]+1:len(message)]
    char_pos=char_pos[1:]
    
    #tmp = message.title()  ##write the title() by yourself
    mlist=list(message)
    for n in char_pos:
        mlist[n+1]=mlist[n+1].upper()
        
    # tmp=''.join(mlist) ##write the join() by yourself
    tmp=''
    for ctmp in mlist: 
        tmp += ctmp
        
    # msg_list = tmp.split(char) #write the split()
    msg_list=[]; nstart=0
    for nend in char_pos:
        msg_list.append(tmp[nstart:nend])
        nstart=nend+1
    msg_list.append(tmp[nstart:])
    
    ##check whether the words belong to sep_words
    New_list=[]
    for word in msg_list:
        if word.lower() in sep_words:
            New_list.append(word.lower())
        else:
            New_list.append(word)
    # tmp=char.join(New_list) ##write the join() by yourself
    tmp=New_list[0]
    for ctmp in New_list[1:]: 
        tmp += char+ctmp
    return tmp

msg_final8_1=message
all_char='-&@ #'
for char in all_char:
    msg_final8_1=change_upper(msg_final8_1, char)

print("INPUT :",message)
print("OUTPUT:",msg_final8_1)

print('\n'*2)

print('Example codes 8-2')
######### Example codes 8-2: rewrite functions by yourself
def change_upper(message, char):
    ### this part is improved compare version 8 and 8-1
    char_pos=[]
    for nr in range(len(message)):
        if message[nr]==char:
            char_pos.append(nr)
            
    #tmp = message.title()  ##write the title() by yourself
    mlist=list(message)
    for n in char_pos:
        mlist[n+1]=mlist[n+1].upper()
    # tmp=''.join(mlist) ##write the join() by yourself
    tmp=''
    for ctmp in mlist:
        tmp += ctmp
        
    # msg_list = tmp.split(char) #write the split()
    msg_list=[]; nstart=0
    for nend in char_pos:
        msg_list.append(tmp[nstart:nend])
        nstart=nend+1
    msg_list.append(tmp[nstart:])
    
    ##check whether the words belong to sep_words
    New_list=[]
    for word in msg_list:
        if word.lower() in sep_words:
            New_list.append(word.lower())
        else:
            New_list.append(word)
    # tmp=char.join(New_list) ##write the join() by yourself
    tmp=New_list[0]
    for ctmp in New_list[1:]:
        tmp += char+ctmp
    return tmp

msg_final8_2=message
all_char='-&@ #'
for char in all_char:
    msg_final8_2=change_upper(msg_final8_2, char)

print("INPUT :",message)
print("OUTPUT:",msg_final8_2)

print('\n'*2)

print('Example codes 9')
######### Example codes 9: simplify
def change_upper(message, char):
    char_pos=[]
    for nr in range(len(message)):
        if message[nr]==char:
            char_pos.append(nr)
    ### add part to deal with exceptional case
    if len(char_pos)==0:
        print('There is no "'+char+'" in '+ message)
        return -1
    
    mlist=list(message)
    for n in char_pos: 
        mlist[n+1]=mlist[n+1].upper()
        
    nstart=0
    for nend in char_pos:
        word=message[nstart:nend]
        if word.lower() in sep_words:
            mlist[nstart:nend]=list(word.lower())
        nstart=nend+1

    tmp=''
    for mr in mlist: 
        tmp += mr
    return tmp

msg_final9=message
all_char='-&@ #()'
for char in all_char:
    # msg_final=change_upper(msg_final, char)
    tmp=change_upper(msg_final9, char)
    if tmp!=-1:
        msg_final9=tmp

print("INPUT :",message)
print("OUTPUT:",msg_final9)

print('\n'*2)

print('Example codes 10')
######### Example codes 10: Better
def change_upper(message, chars):
    char_pos=[]
    for nr in range(len(message)):
        ### deal with all the special characters together 
        if message[nr] in chars:
            char_pos.append(nr)
    if len(char_pos)==0:
        print('There is no "'+chars+'"in '+message)
        return -1
    
    mlist=list(message)
    for n in char_pos: 
        mlist[n+1]=mlist[n+1].upper()
        
    np=0
    for nq in char_pos:
        word=message[np:nq]
        if word.lower() in sep_words:
            mlist[np:nq]=list(word.lower())
        np=nq+1

    tmp=''
    for mr in mlist: 
        tmp += mr
    return tmp

msg_final10=change_upper(message, '-&@ ()')

print("INPUT :",message)
print("OUTPUT:",msg_final10)

print('\n'*2)

# def str_diff(str1,str2):
#     if len(str1)!=len(str2):
#         return True    ##completely different
#     POS_diff=[]
#     for n in range(len(str1)):
#         if str1[n]!=str2[n]:
#             POS_diff.append(n)
#     if POS_diff==[]:
#         return False   ##no difference
#     return POS_diff

# str_diff(msg_final4,message_correct)