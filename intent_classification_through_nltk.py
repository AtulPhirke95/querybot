# use natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

import glob

#nltk.download('punkt')
# word stemmer
stemmer = LancasterStemmer()


training_data = []
"""
for filename in glob.glob('train.txt'):
    chats = open(filename , 'r').readlines()
    training_data.append({"class":"greeting", "sentence":str(chats)})
    #print(len(chats))
"""
training_data.append({"class":"greeting", "sentence":"Hi"})
training_data.append({"class":"greeting", "sentence":"Hello"})
training_data.append({"class":"greeting", "sentence":"Who are you?"})
training_data.append({"class":"greeting", "sentence":"how are you?"})
training_data.append({"class":"greeting", "sentence":"how is your day?"})
training_data.append({"class":"greeting", "sentence":"good day"})
training_data.append({"class":"greeting", "sentence":"how is it going today?"})
training_data.append({"class":"greeting", "sentence":"Hey buddy"})
training_data.append({"class":"greeting", "sentence":"What's up?"})
training_data.append({"class":"greeting", "sentence":"I am fine"})
training_data.append({"class":"greeting", "sentence":"I am good"})
training_data.append({"class":"greeting", "sentence":"fine"})



##training_data.append({"class":"goodbye", "sentence":"have a nice day"})
##training_data.append({"class":"goodbye", "sentence":"see you later"})
##training_data.append({"class":"goodbye", "sentence":"have a nice day"})
##training_data.append({"class":"goodbye", "sentence":"talk to you soon"})

training_data.append({"class":"count", "sentence":"how many number of test cases"})
training_data.append({"class":"count", "sentence":"count of failed test cases"})
training_data.append({"class":"count", "sentence":"cnt of failed test cases"})
training_data.append({"class":"count", "sentence":"conut of failed test cases"})
training_data.append({"class":"count", "sentence":"total number of failed test cases"})
training_data.append({"class":"count", "sentence":"number of failed test cases"})
training_data.append({"class":"count", "sentence":"amount of failed test cases"})
training_data.append({"class":"count", "sentence":"is there any"})
training_data.append({"class":"count", "sentence":"are there any"})



training_data.append({"class":"min", "sentence":"minimum"})
training_data.append({"class":"min", "sentence":"min"})


training_data.append({"class":"max", "sentence":"maximum"})
training_data.append({"class":"max", "sentence":"max"})



corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
#print(classes)
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])


#print(class_words)
#print(corpus_words)
# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            #if show_details:
                #print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score



def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=True)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score

#print(classify("how many number of failed test cases"))
