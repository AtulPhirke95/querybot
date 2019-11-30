import pyttsx3

chatbot = pyttsx3.init()

sound = chatbot.getProperty("voices")

chatbot.setProperty("voice",sound[1].id)

chatbot.setProperty("rate",150)

#chatbot.setProperty["volume",5]
