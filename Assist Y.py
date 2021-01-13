# Import Items
import datetime
import os
import wikipedia
import smtplib
import webbrowser
import pyttsx3
import speech_recognition as sr
import smtplib
import weather_forecast as wf
import file_search
import platform , socket , re , uuid , json , psutil
import fnmatch
import geocoder
import requests
import random
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image , ImageTk
from time import strftime
from tkinter.filedialog import askopenfilename
import textwrap
import time
import urllib.request
# Start Programm
root = Tk()
root.geometry('850x500+250+100')
root.resizable(width = False , height = False)
root.title('Assist [Y]')
# Variables in Listen()
# Date & Time 
time = datetime.datetime.now().strftime("%H:%M:%S")
date_ymd = datetime.date.today()
str_year = date_ymd.year
str_month = strftime('%h')
str_date = date_ymd.day
weekday = strftime('%A')
bday = datetime.date(2017,12,21)
age_year = date_ymd.year-bday.year
age_month = date_ymd.month-bday.month
age_days = date_ymd.day-bday.day
age = age_year,age_month,age_days
greet = "Enjoy"
# Geo Location
#geoloc = geocoder.ip('me').latlng
#geoinfo = requests.get('https://api.ipdata.co?api-key=test').json()
#geoinfo['ip']
# Analizer file
filename = "Analize.txt"
f = open(filename, "a+")
# Week in Words
date = strftime('%Y-%M-%d')
# Network Info
def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        internet = 1
    except:
        None
    #except requests.ConnectionError:
    #    internet = 0
    #    messagebox.showwarning("warning", "show warning example in tkinter" ,icon = 'warning') 
    #    conf = messagebox.askyesno("Quit","Do You Want to Quite Assist [Y] ?")
    #    if conf ==True :
    #        root.destroy()
    #    else:
    #        check_internet()
    #    return False
# System Info
check_internet()
C_path = "C:\\Users\\Yuwan\\Documents\\Visual Studio Projects\\Python\\Assist"
def get_user_data():
    user = Toplevel()
    user.title("Settings")
    user.geometry("500x600+435+75")
    name = StringVar()
    prog = StringVar()
    mynamelbl = Label(user, text = "  Your Name   :",width = 20,font =("bold"))
    mynamelbl.place(x = 100,y = 292)
    pronamelbl = Label(user, text = "Set My Name  :",width = 20,font =("bold"))
    pronamelbl.place(x= 100,y = 372 )
    mynameentry = Entry(user, width = 20,textvariable = name)
    mynameentry.place(x = 250,y = 295)
    mynameentry.focus_force()
    pronameentry = Entry(user, width = 20, textvariable = prog)
    pronameentry.place(x=250,y= 375)
    pronameentry.focus_force()
    def save_user_data():
        f = open(C_path + "\\User_Data\\User_Data.txt",'r+')
        f.write(f"user_name = {name.get()} = prog_name = {prog.get()}")
        f.close
        user.destroy()
    but = Button(user, text = "Save",font=("bold",20),border = 0.7, command = save_user_data)
    but.place(x= 200,y = 500)
def user_data_check():
    if os.path.getsize(C_path + "\\User_Data\\User_Data.txt") == 0:
        get_user_data()
    else:
        try:
           f = open(C_path + "\\User_Data\\User_Data.txt","r")
           data = f.read()
           dat = data.split('=')
           dic = {dat[0]:dat[1],dat[2]:dat[3]}
           master = dic['user_name ']
           prog = dic[' prog_name ']  
        except:
            get_user_data()      
def getSystemInfo():
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['hostname']=socket.gethostname()
            info['ip-address']=socket.gethostbyname(socket.gethostname())
            info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']=platform.processor()
            info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
            # Print
            print("Platform         : "+info['platform'])
            print("Platform Release : "+info['platform-release'])
            print("Platform Version : "+info['platform-version'])
            print("Architecture     : "+info['architecture'])
            print("Host Name        : "+info['hostname'])
            print("IP Address       : "+info['ip-address'])
            print("Mac Address      : "+info['mac-address'])
            print("Processor        : "+info['processor'])
            print("RAM              : "+info['ram'])
# Battery Percentage
def batterypercent():
   battery = psutil.sensors_battery()
   plugged = battery.power_plugged
   percent = str(battery.percent)
   if plugged==False: plugged="Not Plugged In"
   else: plugged="Plugged In"

def Assist():
    # Controller "Name"
    f = open(C_path+ "\\User_Data\\User_Data.txt","r")
    data = f.read()
    dat = data.split('=')
    dic = {dat[0]:dat[1],dat[2]:dat[3]}
    master = dic['user_name ']
    prog = dic[' prog_name ']  
    v = 0  
    # Speak Engine
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[v].id)
    # Wishes from Ultron
    def wishme():
        hour = datetime.datetime.now().hour
        if hour >= 0 and hour <12:
            say("Good Morning "+ master)
        elif hour >=12 and hour <18:
            say("Good Afternoon "+master)
        else: say("Good Afternoon "+ master)
    # Bettery Alart
    def bettery_alert():
        if (psutil.sensors_battery().percent<=30) and (psutil.sensors_battery().power_plugged == False):
            say("Sir, Only "+str(psutil.sensors_battery().percent)+"available. please Plug in Charger")
    # Listen as mast
    def listen():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            #statuslab = Label(root,text = "Listening...")
            #statuslab.place(x= 1, y = 1)
            f = open(filename,"a+")
            f.write(f"Listening...\n")
            audio = r.listen(source)
        try :
            print("Recognizing...")
            statuslab = Label(root,text = "Recognizing...")
            statuslab.place(x= 1, y = 1)
            f = open(filename,"a+")
            f.write(f"Recognizing...\n")
            mas = r.recognize_google(audio, language = 'en-in')
            print(f"Master : {mas}\n")
            f = open(filename, "a+")
            f.write("  Master : "+ mas+ "\n")
        except:
            print("Recognization failed!")
            say("Sir, I don't Feel So Good ")
            f = open(filename, "a+")
            f.write(f":=Ended With Error.\n")
    # Speak as say
    def say(text):
        voiceEng = pyttsx3.init()
        voiceEng.getProperty('rate')
        engine.say(text)
        engine.runAndWait()
        f = open(filename, "a+")
        f.write('  Ultron : '+text+  "\n")
    # write Date & Time to Analizer
    def printtxt():
        f= open(filename,'a+')
        datestr = str(date)
        datestr = datestr.replace("'","")
        datestr = datestr.replace(",","") 
        days = date_ymd.day-bday.day
        f.write(f"\n")
        f.write(f"date : {datestr} Time : {time}   Day : {days}\n")      
        f.write(f"========================================\n")
    printtxt()
    print("Starting...")
    check_internet()
    #say("Starting..."+ master)
    wishme()
    #say("I'm Your Programm. Name Ultron")
    bettery_alert()
    # Reactions
    masty = listen()
    mast = masty.lower()
    # Get Time
    if  "time now" in mast:
       say(f"The Time is {time}")
       contlbl = Label(root,text = time ,font = ('bold'))
       contlbl.place(x = 300,y = 100)
    # Get Date
    elif "today date" in mast:
       say(f"Today date is {date},{weekday}")
       contlbl = Label(root,text = date + weekday ,font = ('bold'))
       contlbl.place(x = 300,y = 100)
    # Search Wikipedia
    elif ("wikipedia" in mast)or ("what is" in mast)or("who is"in mast):
       say("Searching in Wikipedia...")
       statuslab = Label(root,text = "Searching on Wikipeia...")
       statuslab.place(x= 1, y = 1)
       mast = mast.replace("wikipedia", "")
       mast = mast.replace("what is ", "")
       mast = mast.replace("who is ", "")
       results = wikipedia.summary(mast, sentences =2)
       page = wikipedia.page(mast)
       image_link = page.images[0]
       n = 0
       while True:
           a = page.images[n]
           n = n - 1
           if (".jpg" in  a)or(".png"in a):
               image_link = a
               break
       a = image_link.split('/')
       a = a[-1]
       urllib.request.urlretrieve(image_link , C_path+"\\WPP\\"+a)
       #wpp = Image.open(C_path+ "\\WPP\\wpp.jpg")
       #wpp = ImageTk.PhotoImage(wpp)
       class App(Frame):
            def __init__(self, master):
                Frame.__init__(self, master)
                self.columnconfigure(0,weight=1)
                self.rowconfigure(0,weight=1)
                self.original = Image.open(C_path + "\\WPP\\"+ a)
                self.image = ImageTk.PhotoImage(self.original)
                self.display = Canvas(self, bd=0, highlightthickness=0)
                self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
                self.display.grid(row=0, sticky=N+S)
                self.place(x=150,y=100)
                self.bind("<Configure>", self.resize)
                statuslab = Label(root,text = a)
                statuslab.pack()
        
            def resize(self, event):
                size = (event.width//2, event.height//2)
                resized = self.original.resize(size,Image.ANTIALIAS)
                self.image = ImageTk.PhotoImage(resized)
                self.display.delete("IMG")
                self.display.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")
       App(root)
       wrapper = textwrap.TextWrapper(width=50) 
       word_list = wrapper.wrap(text=results)
       elements = '\n'.join(map(str,word_list))
       contlbl = Label(root, text = elements  ,justify = LEFT,font = ('bold'))
       contlbl.place(x= 400,y = 100)
       def read():
           say(results)
       speackbut = Button(root,text = "Read It",command = read ,border = 1,font =("bold"))
       speackbut.place(x = 450,y = 350)       
    # Search Google
    elif "search" in mast:
       say("searching on google...")
       mast = mast.replace("search ","")
       url = "https:///www.google.com//search?q="+mast
       webbrowser.open_new(url)
    # Open Websites    
    elif (".com" in mast)or(".org" in mast)or(".in" in mast)or(".lk" in mast):
       say("Opening website..."+ greet)
       if "open" in mast:
          mast = mast.replace("open ","")
       url = mast
       webbrowser.open_new("http:///www."+ url)
    # Play Music    
    elif ("play music" in mast)or("play song" in mast):
       try:
            f = open(C_path+"\\User_Data\\User_Data.txt","r")
            data = f.read()
            dat = data.split('=')
            dic = {dat[0]:dat[1],dat[2]:dat[3],dat[4]:dat[5]}
            song_path = dic['song_path ']
            songs = os.listdir(song_path)
            songs = random.choice(songs)
            os.startfile(os.path.join(song_path, songs))
       except:
            song_path = filedialog.askdirectory()
            f = open(C_path + "\\User_Data\\User_Data.txt",'a+')
            f.write("=song_path ="+ song_path)
            f.close
            f = open(C_path+"\\User_Data\\User_Data.txt","r")
            data = f.read()
            dat = data.split('=')
            dic = {dat[0]:dat[1],dat[2]:dat[3],dat[4]:dat[5]}
            song_path = dic['song_path ']
            songs = os.listdir(song_path)
            songs = random.choice(songs)
            os.startfile(os.path.join(song_path, songs))
       mast = mast.replace("play ","")
       say("Playing "+ mast)
       say(greet)
    # Open Movies    
    elif ("play movie" in mast)or("open movie" in mast):
        try:
            f = open(C_path+"\\User_Data\\User_Data.txt","r")
            data = f.read()
            dat = data.split('=')
            dic = {dat[0]:dat[1],dat[2]:dat[3],dat[4]:dat[5],dat[6]:dat[7]}
            film_path = dic['film_path ']
            films = os.listdir(film_path)
            films = random.choice(films)
            os.startfile(os.path.join(film_path, films))
        except:
            film_path = filedialog.askdirectory()
            f = open(C_path +"\\User_Data\\User_Data.txt",'a+')
            f.write("=film_path ="+ film_path)
            f.close
            f = open(C_path+"\\User_Data\\User_Data.txt","r")
            data = f.read()
            dat = data.split('=')
            dic = {dat[0]:dat[1],dat[2]:dat[3],dat[4]:dat[5],dat[6]:dat[7]}
            film_path = dic['film_path ']
            films = os.listdir(film_path)
            films = random.choice(films)
            os.startfile(os.path.join(film_path, films))
        mast = mast.replace("play ","")
        say("Playing "+ mast)
        say(greet)
    # Open Websites & Applications & Files
    elif "open" in mast:
       mast = mast.replace("open ","")
       say("Opening "+ mast +" "+ master)
       say(greet)
       # Websites
       if ("youtube" in mast) or ("youtube.com" in mast):
           url = "http:///www.youtube.com"
           webbrowser.open_new(url)
       elif ("pinterest" in mast) or ("pinterest.com" in mast):
           url = "http:///www.pinterest.com"
           webbrowser.open_new(url)
       # Applications
       elif "settings" in mast:
           path = "C:\\WINDOWS\\System32\\Control.exe"
           os.startfile(path)
       elif "calculator" in mast:
           path = "C:\\Windows\\System32\\calc.exe"
           os.startfile(path) 
       # Folders
       else:
        name = masty
        path = "C:\\Users\\Yuwan\\"
        folders = os.listdir(path)
        def find_all(name, path):
            if name in folders:
               print("It's Here") 
            else:
                result = []
                for root, dirs, files in os.walk(path):
                    if name in files:
                       result.append(os.path.join(root, name))
                       print(result)
                       os.startfile(result[0])
                return result
        find_all(name, path)
    # Weather
    elif "today weather" in mast:
       weather = wf.forecast(place = "Colombo", time = time , date = "2019-12-31" , forecast= "daily")
       a = "\n".join(map(str,weather))
       weatlab = Label(root,text = a)
       weatlab.pack()
    # Get System Info
    elif ("system info" in mast) or ("about" in mast) or ("system" in mast) or ("information" in mast):
     getSystemInfo()
     batterypercent()
    elif ("charg" in mast) or ("bettery"in mast):
        batterypercent()
        bettery_alert()
    # Location
    elif "location" in mast:
        say("Opening on googlemap...")
        geoloc = geoloc.replace("[","")
        geoloc = geoloc.replace("]","")
        url = "https:///www.google.com//search?q="+ geoloc
        print(url)
        webbrowser.open_new(url)
    # View IP-Adress
    elif ("my ip address"in mast) or ("view ip" in mast):
        print(platform.version())
        say("Your Ip address is "+socket.gethostbyname(socket.gethostname())+"sir")
    # Take Notes
    elif ("take notes"in mast) or ("note it"in mast):
        say("ready to take notes "+ master)
        say(f"give me a name {master}")
        masty = listen()
        name = masty
        file_name = masty + ".txt"
        n = open(file_name,"x")
        masty = None
        say("Say Something to Note."+master)
        masty = listen()
        n.write(masty)
        mast = None
        say("finished")
        n.close()
        masty = listen()
        mast = masty.lower()
        if ("view"in mast) or ("read" in mast):
            os.startfile("C:\\Users\\Yuwan\\Documents\\Projects\\Visual Studio\\Visual Studio Code\\"+file_name)
            say("Opening text file..."+greet)
    else:
       say("You Didn't Feed me this Command :Use Another Keyword Sir.")
       masty = listen()
       mast = masty.lower()
def tips():
    Tips = Label(root,text = "Time Now                       - Time\nDate today                     - Date\nWho is(or)What is + word - Search Wikipedia\nsearch + word            - Search Google\nopen + website domain    - open website\n(eg:- open youtube.com)\nPlay Music (or) Play song- Play Music\nPlay Movies              - Play Movies",justify = "left",font=('bold',11))
    Tips.place(x = 200,y = 100)
#user_data_check()
# Paths to Images
icon = Image.open(C_path+ "\\PNGs\\icon.png")
icon = ImageTk.PhotoImage(icon)
mic = Image.open(C_path + "\\PNGs\\mic.png")
mic = ImageTk.PhotoImage(mic)
check_for_update = Image.open(C_path + "\\PNGs\\Check_for_Update.png")
check_for_update = ImageTk.PhotoImage(check_for_update)
close = Image.open(C_path + "\\PNGs\\Close.png")
close = ImageTk.PhotoImage(close)
cmd_mode = Image.open(C_path + "\\PNGs\\CMD mode.png")
cmd_mode = ImageTk.PhotoImage(cmd_mode)
download = Image.open(C_path + "\\PNGs\\Download.png")
download = ImageTk.PhotoImage(download)
file = Image.open(C_path + "\\PNGs\\File.png")
file = ImageTk.PhotoImage(file)
help = Image.open(C_path + "\\PNGs\\Help.png")
help = ImageTk.PhotoImage(help)
search = Image.open(C_path + "\\PNGs\\Search.png")
search = ImageTk.PhotoImage(search)
settings = Image.open(C_path + "\\PNGs\\Settings.png")
settings = ImageTk.PhotoImage(settings)
volume = Image.open(C_path + "\\PNGs\\Volume.png")
volume = ImageTk.PhotoImage(volume)
mute = Image.open(C_path + "\\PNGs\\Volume_mute.png")
mute = ImageTk.PhotoImage(mute)

# GUIs
def openfile():
    root.filename =askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
def timer(): 
    string = strftime('%H:%M:%S %p') 
    timelbl.config(text = string) 
    timelbl.after(1000, timer)
timelbl = Label(root, font = 'bold')
timer()
timelbl.pack()
def battery():
    battery1 = psutil.sensors_battery()
    percent = str(battery1.percent) 
    batteryperc.config(text = percent + "%" )
    batteryperc.after(1000,battery)
batteryperc = Label(root, font = 'bold')
battery()
batteryperc.place(x = 800,y = 4)
root.iconphoto(False ,icon)
listenbutn = Button(root,image = mic , command = Assist, border = 0)
listenbutn.place(x = 380,y = 395)
quitbutn = Button(root,image = close , command = root.destroy, border = 0)
quitbutn.place(x = 40,y = 395)
filesearchbutn = Button(root,image = file ,border = 0,command = openfile)
filesearchbutn.place(x = 720,y = 395)
helpbutn = Button(root, image = help ,command = tips, border = 0)
helpbutn.place(x = 40 , y = 250)
settingsbutn = Button(root, image = settings, border = 0)
settingsbutn.place(x=40,y= 105)

root.mainloop()
