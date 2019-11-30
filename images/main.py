import speech_recognition as sr

import re
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
try:
    #user_query = "How many test cases are failed are failed for craft and ibn"
    user_query = r.recognize_google(audio,language = 'en-IN')
    #print(user_query)
    #hin_word = r.recognize_google(audio,language = 'hi-IN')
    kranken_list = ['drunken', 'franken','cranking','company','cancun']
    privat_list = ['prabhat']
    koll_list = ['colective']
    kraft_list = ['craft']
    firmen_list = ['Perman']
    leben_list = ['libin','ribbon','Lebanon','IBN','Livon']
    schaden_list = ['shadan']

    user_query_temp=[re.sub(word.lower(),"kranken",user_query) for word in kranken_list if word.lower() in user_query]
    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_temp=[re.sub(word.lower(),"privat",user_query) for word in privat_list if word.lower() in user_query]

    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_1=[re.sub(word.lower(),"kollektiv",user_query) for word in koll_list if word.lower() in user_query]

    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_temp=[re.sub(word.lower(),"kraft",user_query) for word in kraft_list if word.lower() in user_query]
    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_temp=[re.sub(word.lower(),"firmen",user_query) for word in firmen_list if word.lower() in user_query]
    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_temp=[re.sub(word.lower(),"leben",user_query) for word in leben_list if word.lower() in user_query]
    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
        
    user_query_temp=[re.sub(word.lower(),"schaden",user_query) for word in schaden_list if word.lower() in user_query]
    if(len(user_query_temp)>0):
        user_query = "".join(user_query_temp)
    print(user_query)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
##import re
##user_query = "Hello my name is cranking"
##kranken_list = ['drunken', 'franken','cranking','company']
##end_1=[re.sub(word,"kranken",user_query) for word in kranken_list if word in user_query]
##print(end_1[0])

