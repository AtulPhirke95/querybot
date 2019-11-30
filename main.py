#tkinter-GUI modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image
from PIL import ImageTk
import glob
import tkinter.scrolledtext as ScrolledText
import time
import pyttsx3
import speech
import speech_recognition as sr
import os
import ast   #converting string representation of list to list data structures
from tkinter import simpledialog
import pyaudio


#import threading

#spacy related modules - For entity(column extraction)
import spacy

#for importing class EntityMatcher written under entity_extractor py file
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from entity_extractor import EntityMatcher as em

#NLTK module - for intent classification
import intent_classification_through_nltk as nl

#for returning queries which are created based on the intents and entities
import query_builder as query

#for extracting dates from natural language
import date_finder as df

#for connecting the front end with db and rerturning the results based on the sql queries
import db_processor as db

#chattebot module- for classifying other than aggrergate functions
from chatterbot.trainers import ListTrainer #method to train the chatterbot
from chatterbot import ChatBot   

#list of failureCategory which is a column and the assigned values are the filters applied on the columns
failureCategory = [u'functional defect', u'functional change', u'data issue', u'infrastucture issue', u'technical issue', u'environment issue', u'design update']
team = [u'motor',u'kraft', u'claims', u'schaden', u'kollektiv', u'life',u'leben', u'kranken', u'workflow',u'input and output', u'firmen', u'privat', u'kup', u'collections and disbursement', u'inex',u'cnd',u'provision',u'commission', u'oms',u'contract generally']
failureLogs = [u'retry',u'control',u'robot',u'rmi',u'controlnotfound',u'externalfunction']

#for manually identifying entities (columns) other than the ones which are predefined by scapy
entities_name = ['FAILURECATEGORY', 'TEAM','FAILURELOGS']

#for manually identifying entity values or filters fro columns
entities_value = [failureCategory,team,failureLogs]

#for storing the entities along with there values
entities_extraction_results =[]

#table in the database from which data is going to fetch
table_name="failedData"



#Module used for converting audio to test (use of mike symbol on the GUI)
text_to_audio = pyttsx3.init()
r = sr.Recognizer()


#Setting for chatter bot module used to classify intents like greeting, good bye, etc
bot = ChatBot('queryBot',logic_adapters=[
{
    "import_path": "chatterbot.logic.BestMatch",
    "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
    "response_selection_method": "chatterbot.response_selection.get_first_response"
},
{
    "import_path": 'chatterbot.logic.MathematicalEvaluation',
},
{
    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
    'threshold': 0.70,
    'default_response': 'Sorry I can not understand'
}
],
     storage_adapter="chatterbot.storage.SQLStorageAdapter"
)


#set the trainer for chatter bot module
bot.set_trainer(ListTrainer)   #set the trainer

#reading the conversation saved in the text file for giving replies
for filename in glob.glob('greeting.txt'):
    chats = open(filename , 'r').readlines()
    bot.train(chats)

#setting object for tkinter module (welcome window)
window = Tk()

window.title("Welcome to queryBot")

#disabling maximize button of the window
window.resizable(0,0)


response_list=[]

def text_to_speech(response,chk):
    """
        This function is used to read the user responses printed on the gui and converts it to audio format if checkbox is selected
    """
    if chk == True:
        text_to_audio.say(response)
        text_to_audio.runAndWait()

def show_query_result(query_display,conversation,chk):
    """
        This function is used to write the responses return by db in a user readable format on the conversation(scrolledttext)

    """
    if query_display != None:
        query_display = ast.literal_eval(query_display)
        len_query_display = len(query_display)
        #print(len(query_display))
        if type(query_display[0])==tuple:
            for i_items in query_display:
                items_count = 0
                
                for items in i_items:
                    
                    if items_count == len(i_items)-1:
                        if items == None:
                            conversation.insert(
                            END, "Not Analysed" + "\n"
                    )
                        else:
                            conversation.insert(
                            END, str(items) + "\n"
                    )
                        conversation.see(END)   
                    else:
                        if items == None:
                            conversation.insert(
                            END, "Not Analysed" + "->"
                    )
                        else:
                            conversation.insert(
                            END, str(items) + "->"
                    )
                        conversation.see(END)
                    items_count = items_count + 1
                    

                        
        elif type(query_display[0])==list:
            for len_list in range(len_query_display):
                
                for i_items in query_display[len_list]:
                    items_count = 0
                    
                    for items in i_items:
                        
                        if items_count == len(i_items)-1:
                            if items == None:
                                conversation.insert(
                                END, "Not Analysed" + "\n"
                        )
                            else:
                                conversation.insert(
                                END, str(items) + "\n"
                        )
                            conversation.see(END)   
                        else:
                            if items == None:
                                conversation.insert(
                                END, "Not Analysed" + "->"
                        )
                            else:
                                conversation.insert(
                                END, str(items) + "->"
                        )
                            conversation.see(END)
                        items_count = items_count + 1
        conversation.see(END)
        if len(query_display)<20:
            text_to_speech(query_display,chk)
    


def writing_to_conversation(name,request,response,windows,conversation,flag,chk):
    """
        This function is used to seperate the validations from the queries based on the flag set while calling this function
    """
    conversation['state'] = 'normal'
    if flag == 0:
        conversation.insert(
                END, "ChatBot: " + str(response) + "\n", 'validation_text'
        )
        conversation.tag_config('validation_text', foreground='red')
        conversation.see(END)                           #automatic scroll down to the latest linein conversation.
        text_to_speech(response,chk)
        
    elif flag == 1:
        conversation.insert(
                END, "ChatBot: ", "chatbot_name"
        )
        conversation.insert(
                END, "Have look on the requested results..." + "\n"
        )
        conversation.tag_config('chatbot_name', foreground='red')        
        conversation.see(END)
        show_query_result(str(response),conversation,chk)
        #text_to_speech(response,chk)

    elif flag == 2:
        conversation.insert(
                END, "ChatBot: ", "chatbot_name"
        )
        conversation.insert(
                END, str(response) + "\n"
        )
        conversation.tag_config('chatbot_name', foreground='red')        
        conversation.see(END)
        text_to_speech(response,chk)
        
def intent_entity_extractor(name,request_entry,user_query,windows,conversation,chk):
    """
        This function extract the entities from the natuaral language and store them in the list entities_extraction_results as [Entity,Entity_value]
    """
    entities_extraction_results =[]
    user_query=user_query.lower()
    for loops in range(len(entities_name)):
        nlp = spacy.load('en_core_web_sm')
        entity_matcher = em(nlp, entities_value[loops], entities_name[loops])
        nlp.add_pipe(entity_matcher, after='ner')
        doc = nlp(u"{}".format(user_query))
        for ent in doc.ents:
            entities_extraction_results.append([ent.label_,ent.text])
        

    #calling classify function which returns the intent of the query
    intent_name_tuple=nl.classify(user_query)

    intent_name = intent_name_tuple[0]       

    #print(intent_name)

    
    #extract date from the user query
    date_entity = df.date_picker(user_query)

    
    #storing executiondate entity to the existing list of entity if date is present in the user query
    if (date_entity !=None):
        entities_extraction_results.append(['EXECUTIONDATE',date_entity])

    #classification based on the intent       
    if intent_name == 'count':
        query_extracted = query.query_builder(user_query,intent_name,entities_extraction_results,table_name,date_entity)
        
        if "SELECT" in query_extracted:
            query_display = db.db_processor(query_extracted)
            
            if len(query_display) != 0:
                writing_to_conversation(name,user_query,query_display,windows,conversation,1,chk)
                
            else :
                writing_to_conversation(name,user_query,"No records found",windows,conversation,0,chk)
                
        else:
            writing_to_conversation(name,user_query,"Please try out something different query...",windows,conversation,0,chk)
            #print("queryBot: Please try out something different query...")
            


    elif intent_name == 'greeting':
        response=bot.get_response(user_query)
        writing_to_conversation(name,user_query,response,windows,conversation,2,chk)


    elif intent_name == 'min':
        query_extracted = query.query_builder(user_query,intent_name,entities_extraction_results,table_name,date_entity)
        query_extracted_temp=str(query_extracted)
        if query_extracted!=None:
            if "SELECT" in query_extracted:
                query_display = db.db_processor(query_extracted)
                
                if (len(query_display)!=0):
                    writing_to_conversation(name,user_query,query_display,windows,conversation,1,chk)
                else:
                    writing_to_conversation(name,user_query,"Sorry we dont find any records for your query. Please try something else.",windows,conversation,0,chk)
                    #print("Sorry we dont find any records for your query. Please try something else.")

            elif "(" in query_extracted_temp:
                writing_to_conversation(name,user_query,query_extracted,windows,conversation,1,chk)
                
            elif "queryBot" in query_extracted:
                writing_to_conversation(name,user_query,"Please try asking different things",windows,conversation,0,chk)
                #print("queryBot : Please try asking different things")
                
        else:
            writing_to_conversation(name,user_query,"Sorry we do not have any data to show. Please try entering the query in other way.",windows,conversation,0,chk)            



    elif intent_name == 'max':
        query_extracted = query.query_builder(user_query,intent_name,entities_extraction_results,table_name,date_entity)
        query_extracted_temp=str(query_extracted)
        if query_extracted!=None:
            if "SELECT" in query_extracted:
                query_display = db.db_processor(query_extracted)
                
                if (len(query_display)!=0):
                    writing_to_conversation(name,user_query,query_display,windows,conversation,1,chk)
                else:
                    writing_to_conversation(name,user_query,"Sorry we dont find any records for your query. Please try something else.",windows,conversation,0,chk)
                    #print("Sorry we dont find any records for your query. Please try something else.")

            elif "(" in query_extracted_temp:
                writing_to_conversation(name,user_query,query_extracted,windows,conversation,1,chk)
                
            elif "queryBot" not in query_extracted:
                writing_to_conversation(name,user_query,"Please try asking different things",windows,conversation,0,chk)
                #print("queryBot : Please try asking different things")
                
        else:
            writing_to_conversation(name,user_query,"Sorry we do not have any data to show. Please try entering the query in other way.",windows,conversation,0,chk)

    elif intent_name == None:
        writing_to_conversation(name,user_query,"Sorry I dont understand. Please ask me in some different way.",windows,conversation,0,chk)
        #print("queryBot : Sorry I dont understand. Please ask me in some different way.")
        
    #text_to_speech(user_query,chk)

    
def click(name,request_entry,user_query,windows,conversation,chk):
    """
        This function is triggred when ENTER is pressed or when send button is clicked and forwards the control for nlp
    """
    conversation['state'] = 'normal'  #open conversation in edit mode
    request_entry.delete(0,'end')   #removing the query after hitting ENTER key from keyword or by clicking button
    if len(user_query)==0:
        conversation.insert(
            END, "Please enter something in the query box before hitting ENTER or pressing \"Ask Something?\" button. " + "\n", "validation_text"
    )
        conversation.tag_config('validation_text', foreground='red')
    else:
        conversation.insert(
                 END, name + ": ", "user_name"
       )
        conversation.insert(
                 END, user_query + "\n"
       )
        conversation.tag_config('user_name', foreground='green')
        intent_entity_extractor(name,request_entry,user_query,windows,conversation,chk)
    conversation['state'] = 'disabled'  #set conversation to read only mode  

def say_identify_team(user_query):
    kranken_list = ['drunken', 'franken','cranking','company','cancun','chicken','priyanka','uncle','franklin']
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
    return user_query
    
def say(name,request_entry,windows,conversation,chk):
    """
        This function is triggered after clicking mike button and converts the audio from user to text and prints it on the conversation
    """

    conversation['state'] = 'normal'
    
    request_entry.delete(0,'end')
    
    
    with sr.Microphone() as source:
        
        r.adjust_for_ambient_noise(source, duration=1)
        CHUNK = 1024
        FORMAT = pyaudio.paInt16 # the Format is picked up from the pyaudio
        CHANNELS = 2
        RATE = 44100
        source.CHUNK = CHUNK
        source.format = FORMAT # FORMATING THE SOURCE FILE
        r.energy_threshold += 280
        audio = r.listen(source,phrase_time_limit=2)
        
    try:
        user_query = r.recognize_google(audio,language="en-IN") #r.recognize_sphinx(audio)
        if len(user_query)==0:
            conversation.insert(
                END, "Please enter something in the query box before hitting ENTER or pressing \"Ask Something?\" button. " + "\n", "validation_text"
        )
            conversation.tag_config('validation_text', foreground='red')   
        else:
            user_query=say_identify_team(user_query)
            conversation.insert(
                 END, name + ": ", "user_name"
           )
            conversation.insert(
                 END, user_query + "\n"
           )
            conversation.tag_config('user_name', foreground='green')
            #time.sleep(5)
            intent_entity_extractor(name,request_entry,user_query,windows,conversation,chk)

    except sr.UnknownValueError:
        conversation.insert(
            END, "ChatBot: " + "Our machine says it could not understand the audio. Please speak louder orelse speak clearer" + "\n", "validation_text"
        )
        conversation.tag_config('validation_text', foreground='red')
        conversation.see(END)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
 
    conversation['state'] = 'disabled'
    
def getting_started(name):
    """
        This function mainly deals with the gui part and handling of conversation
    """
    if len(name)>0:
        #destroying start window so that new conversation window will open
        window.destroy()

        #initializing new object for new window(conversation window)
        windows=Tk()
        windows.resizable(0,0)
        windows.title("queryBot " + "(Conversation with " + name + ")")

        windows=Frame(windows)
        conversation = ScrolledText.ScrolledText(windows,state="disabled")
        conversation.pack()

        request_entry = Entry(windows,width=70)
        request_entry.pack(side=LEFT,ipadx=60)

        #gui setting for mike button
        width = 25
        height = 25
        img = Image.open("./images/mike_1.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        photoImg =  ImageTk.PhotoImage(img)

        sayBtn = Button(windows, text="Say", activebackground="green", fg="black",image=photoImg,command=lambda :say(name,request_entry,windows,conversation,chk_state.get()))
        sayBtn.pack(side=LEFT)

            
        #used for triggering code after hitting enter from keyboard
        request_entry.bind("<Return>",lambda _ :click(name,request_entry,request_entry.get(),windows,conversation,chk_state.get()))

        #gui setting for send button
        width_send = 25
        height_send = 25
        img = Image.open("./images/send_1.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        photoImg_send =  ImageTk.PhotoImage(img)
        
        sendBtn = Button(windows, text="Ask something?", activebackground="green", fg="black",image=photoImg_send,command=lambda :click(name,request_entry,request_entry.get(),windows,conversation,chk_state.get()))
        sendBtn.pack(side=LEFT)
        chk_state =BooleanVar()
        chk_state.set(False) #set check state to unselected by default

        #gui setting for Voice checkbox
        width = 30
        height = 30
        img = Image.open("./images/voice.png")
        img = img.resize((width,height), Image.ANTIALIAS)
        photoImg_voice =  ImageTk.PhotoImage(img)
        
        chk = Checkbutton(windows, text='Voice?',image=photoImg_voice, var=chk_state)
        chk.pack(side=LEFT)
        
        windows.pack()
        windows.mainloop()
        
    elif len(name)==0:
        #deals with empty name field
        lbl_name_validation = Label(window, text="Name cannot be empty.")
        lbl_name_validation.grid(column=1, row=2)

        

lbl_name = Label(window, text="Please enter user name*")
lbl_name.grid(column=0, row=1)
name_entry = Entry(window,width=40)
name_entry.grid(column=1, row=1, sticky='nesw')
name_entry.bind("<Return>", lambda _ : getting_started(name_entry.get()))

#gui setting for start button
##width = 120
##height = 50
##img = Image.open("./images/start.png")
##img = img.resize((width,height), Image.ANTIALIAS)
##photoImg_start =  ImageTk.PhotoImage(img)
btn_getting_started = Button(window, text="Continue", command=lambda:getting_started(name_entry.get()))

btn_getting_started.grid(column=1, row=3)
window.mainloop()

