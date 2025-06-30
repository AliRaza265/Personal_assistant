import pyttsx3 as speaker
import speech_recognition as sr
import pygame
import webbrowser
import time
import openai
import api_key 
from twilio.rest import Client
import os
import pyautogui
import serial
import pywhatkit 
# function for system voice
def Say(input):
    engine = speaker.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 130)
    engine.say(input)
    engine.runAndWait()


# function for recognized user input 
def Hear(lop):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        if lop:
            Say("What’s your query, Ali?")
            pass
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
    try:
        query = rec.recognize_google(audio, language="en-US")
        print(query)
        return query
    except:
        return "I apologize, but I didn't hear you very well."


# chat gpt functionality
def chat_api(say):
    openai.api_key = api_key.chat_key
    # Make the API request
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": say}],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print the content of the response
    data =  response.choices[0].message.content
    print(data)
    return(data)


# mobile messageing function
def mobile_message(remind_message):
    try:
        print(remind_message)
        clients = Client(api_key.Account_SID,api_key.Auth_Token)
        message = clients.messages.create(
            from_=api_key.twilio_number,
            to = api_key.my_phone_number,
            body = remind_message
        )
    except :
           Say("I couldn't send the message via Twilio due to some critical network issues")
    

# function for mp3 play sounds    
def sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()   
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)

message = Hear(False)

# condition mark for statup the bot 
if "wake up brain" in message.lower() or "backup brain" in message.lower() :
    sound("audio/startup.mp3")
    sound("audio/brain.mp3")
    Say("I'm up and ready to assist") 
    while True:
        say = Hear(True)
        # condition  for open the website
        if "open" in say:
            site_name = say.split(" ")
            print(site_name[-1])
            Say(f"open {site_name[-1]}") 
            webbrowser.open(f"https://www.{site_name[-1]}.com/")

        # condition  for play the music
        elif "play music" in say:
            webbrowser.open("https://www.youtube.com/watch?v=OGH8j3z9IoU&list=PL-f4mDUcYvWzn4kag-6SfPnOcpIlrBf8U")
            Say("play music")
                
        # condition  for searching from youtube & google
        elif "search from youtube" in say.lower() or "search from google" in say.lower():
            platform = say.split(" ")
            print(platform[-1])
            Say(f"what you want search from {platform[-1]}")
            search_qurey = Hear(False)
            if platform[-1].lower() == "google":
                webbrowser.open(f"https://www.google.com/search?q={search_qurey}")
            elif platform[-1].lower() == "youtube":
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_qurey}")
               
        # condition  for send msg
        elif "send message" in say.lower():
            Say("Select a contact number.")
            contect_num  = Hear(False)
            contect_dic = {
                "tayyab":"+923057364689",
                "father":"+923090659089",
                "ali":"+923086835659",
                "hasnain":"+923220938189",
            }
            
            Say("What’s your note?")
            note_msg = Hear(False)
            try:
                contact_number = contect_dic[contect_num.lower()]
                # Send the message with a delay of at least 2 minutes ahead from current time
                current_hour = int(time.strftime("%H"))
                current_minute = int(time.strftime("%M"))
                Say("Give me a moment, please.")
                pywhatkit.sendwhatmsg(contact_number, note_msg, current_hour, current_minute + 2)
                pyautogui.hotkey('enter')
                Say("Your message is on its way")
                
            except KeyError:
                Say(f"Error: Contact name '{contect_num}' not found in the dictionary.")
            except Exception as e:
                Say(f"There seems to be an issue {e}")

        # condition  for ask the time
        elif "tell me the time" in say.lower():
            times = time.strftime("%H %M %S")
            timer = times.split(" ")
            if int(timer[0]) > 12:
                hours = int(timer[0]) % 12
            else:
                hours = timer[0]
            Say(f"{hours}:{timer[1]}:{timer[2]} o'clock")
        elif "pause brain" in say.lower() :
            Say("The system is on hold for a while")
            lops = True
            while lops:
              print("listening...")
              pause_system = Hear(False)
              if "restart brain" in pause_system.lower() :
                Say("The system is rebooting")
                lops = False
              else : 
                lops = True
        # condition  for ask the  date
        elif "tell me the date" in say.lower():
            date = time.strftime('%Y-%m-%d')
            date_stu = date.split("-")
            Say(f"{date_stu[1]}/{date_stu[2]}/{date_stu[0]}")

        # condition for send mobile message
        elif "send me a reminder" in say.lower():
            Say("What would you like me to remind you about?")
            remind_message = Hear(False)
            mobile_message(remind_message)

        # condition for stored data
        elif "memorize brain" in say.lower():
            Say("Understood, I'll adapt to this new information.")
            memory_message  = Hear(False) 
            with open("memory.txt",'a') as memory_file:
                memory_file.write(f"{memory_message}\n")
                print(memory_message)
 
        # condition for seach data from jarvis memory 
        elif "search from memory" in say.lower():
            Say("what you wana search from my memory")
            search_message = Hear(False)
            with open("memory.txt",'r') as file_reader:
                all_files = file_reader.read()
                single_file = all_files.split("\n")
                find_msg = False 
                for index,file in enumerate(single_file):
                    if(search_message.lower() in file):
                       Say(file)
                       find_msg = True
                if find_msg == False:
                        Say("Sorry, I don't have information on that topic in my memory.")
       
        #condition close webtabs
        elif "close tab" in say.lower():
            Say("ok close tab")
            pyautogui.hotkey("ctrl","w")
        
        #condition change tab
        elif "switch tab" in say.lower():
            Say("ok switch tab")
            pyautogui.hotkey("ctrl","tab")

        #condition change tab
        elif "switch app" in say.lower():
            Say("ok switch app")
            pyautogui.hotkey("alt","tab")

        #condition change tab
        elif "copy data" in say.lower():
            pyautogui.hotkey("ctrl","a")
            pyautogui.hotkey("ctrl","c")
            Say("ok copy data") 

        #condition change tab
        elif "paste data" in say.lower():
            pyautogui.hotkey("ctrl","v")
            Say("ok paste data")

        # condition for open apps 
        elif "visit" in say.lower():
            app = say.split(" ")
            app[-1]
            print(app[-1])
            try:
                Say(f"open {app[-1]}")
                os.system(f"start {app[-1]}")
            except:
                Say("sorry i can't open this app due to some privacy issues")

        # condition for shutdown system
        elif "shutdown the system" in say.lower():
            Say("Are you sure you wana shutdown the system")
            answer = Hear(False)
            print(answer)
            if "absolutely" in answer.lower():
                os.system("shutdown /s /t 1")
                
        # condition  for break the  loop
        elif "sleep brain" in say.lower():
            Say("Goodbye!")
            exit()
     
        # take information from api 
        else:
                cht_gpt = chat_api(say)
                Say(cht_gpt)
        