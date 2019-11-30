import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

try:
    eng_word = r.recognize_google(audio,language = 'en-IN')
    print(eng_word)
    #hin_word = r.recognize_google(audio,language = 'hi-IN')
    kranken_list = ['drunken', 'franken','cranking','company']
    privat_list = ['Prabhat']
    koll_list = ['colective']
    kraft_list = ['craft']
    firmen_list = ['Perman']
    leben_list = ['Libin','ribbon','Lebanon','IBN','Livon']
    schaden_list = ['Shadan']
    if eng_word in kranken_list:
        print('kranken')
    if eng_word in privat_list:
        print('privat')
    if eng_word in koll_list:
        print('kollektiv')
    if eng_word in kraft_list:
        print('kraft')
    if eng_word in firmen_list:
        print('firmen')
    if eng_word in leben_list:
        print('leben')
    if eng_word in schaden_list:
        
        print('schaden')
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


