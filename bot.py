import ch
import threading
import tkinter
import itertools
import time
#import webbrowser
from tkinter import *

class TestBot(ch.RoomManager):
  def onConnect(self, room):
    self.enableBg()
    listbox.config(state='normal')
    if NICK != "":
      self.setNameColor(Settings[5])
      self.setFontColor(Settings[6])
      self.setFontFace(Settings[7])
      self.setFontSize(int(Settings[8]))
    else:
      self.setNameColor("333333")
      self.setFontColor("FFFFFF")
      self.setFontFace("Latha")
      self.setFontSize(11)    
    self.ListNum = 0
    listbox.insert(END, 'Connected to '+room.name+'\n')
    listbox.config(state='disabled')


  def onMessage(self, room, user, message):
    listbox.config(state='normal')
    if user.name not in Ignored:
      self.ListNum += 1

      listbox.insert(END, user.name+'-'+time.strftime('%X')+'   '+message.body+'\n')
      Message = user.name+'-'+time.strftime('%X')+'   '+message.body+'\n'
      listbox.yview_scroll(self.ListNum, 'pages')
      listbox.tag_add(self.ListNum, float(self.ListNum+1), float(self.ListNum+2))
      listbox.tag_add(str(self.ListNum)+'a', float(self.ListNum+1), float((self.ListNum)+ 1 + float(str('0.'+str(Message.index(' '))))))
      Colour = user.fontColor[0]+user.fontColor[0]+user.fontColor[1]+user.fontColor[1]+user.fontColor[2]+user.fontColor[2]

      listbox.tag_configure(str(self.ListNum), font=user.fontFace.replace(' ','')+' 8 ', relief='raised', foreground='#'+Colour,)
      listbox.tag_configure(str(self.ListNum)+'a', font=user.fontFace.replace(' ','')+' 8 bold', relief='raised', foreground='White')
      listbox.config(state='disabled')
Ignored = []
NICK=""
PASS=""
ROOM=""

try:
  with open ('settings.txt', 'r') as f: 
    Settings=f.read().split('|')
    print (Settings)
    NICK= Settings[0]
    PASS = Settings[1]
    ROOM = Settings[2]
    Ignored = Settings[3]
except IOError:
  print ("Missing 'Settings.txt' file")

if NICK != "":
  TestBot = TestBot(NICK,PASS)
  TestBot.joinRoom(ROOM)
else:
  NICK = input("Your Account name: ")
  PASS = input("Your Password: ")
  ROOM = input("Room name: ")
  TestBot = TestBot(NICK,PASS)
  TestBot.joinRoom(ROOM)
  Settings = [NICK, PASS, ROOM, ' ', '333', '9c2afc', '2da446', '0', '11']
  with open ('settings.txt', 'w') as f: f.write(NICK+'|'+PASS+'|'+ROOM+'| |333|9c2afc|2da446|0|11')

TestBot_thread = threading.Thread(target=TestBot.main,)
TestBot_thread.setDaemon(True)
TestBot_thread.start()

class BotGUI(tkinter.Tk):
  def get(event):
    listbox.config(state='normal')
    try:
      if '!bg' in text.get(): 
        if text.get().split()[1].isdigit():
          listbox.config(bg='#'+str(text.get().split()[1]))
        else:
          listbox.config(bg=str(text.get().split()[1]))
      elif '!nc' in text.get():
        TestBot.setNameColor(text.get().split()[1])
      elif '!bc' in text.get():
        TestBot.setFontColor(text.get().split()[1])
      elif '!bs' in text.get():
        TestBot.setFontSize(int(text.get().split()[1]))
      elif '!font' in text.get():
        TestBot.setFontFace(text.get().split()[1])
      elif '!quit' in text.get():
        quit()
      elif '!ignore' in text.get():
        if text.get().split()[1] in TestBot.Ignored:
          TestBot.Ignored += text.get().split()[1]
        else:
          TestBot.Ignored = TestBot.Ignored.replace(text.get().split()[1],"")
      else:
        room = TestBot.getRoom(ROOM)
        room.message(text.get(), False)  
    except Exception as error: print (error)
    text.delete(0,20000) 
  
  GUI = tkinter.Tk()
  GUI.title(ROOM + ' Chat Client')
  GUI.geometry("300x660")
  GUI.minsize(100,100)
  GUI.wm_attributes("-topmost", 1)
  global listbox,text
  text = Entry(GUI)
  listbox = Text(GUI)
  text.bind('<Return>', get)
  text.pack(fill=BOTH, side='bottom')
  listbox.config(bg='#'+Settings[4], borderwidth=0, selectborderwidth=0, font=('Arial',8,'bold') )
  listbox.pack(side='right',fill=BOTH, expand=1)

gui_thread = threading.Thread(target=tkinter.mainloop(),)
gui_thread.setDaemon(True)
gui_thread.start()
