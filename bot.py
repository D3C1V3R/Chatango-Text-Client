import ch
import threading
import tkinter
import time
import webbrowser
from tkinter import *

class TestBot(ch.RoomManager):
  def onConnect(self, room):
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


  def onMessage(self, room, user, message):
    if user.name not in Ignored:
      self.ListNum += 1
      listbox.insert(END, user.name+'-'+time.strftime('%X')+'   '+message.body+'\n')
      listbox.itemconfig(self.ListNum,fg='#'+user.fontColor)
      listbox.yview_scroll(self.ListNum, 'p')
Ignored = []

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
  Settings = [NICK, PASS, ROOM, ' ', '999', '9c2afc', '2da446', '0', '11']
  with open ('settings.txt', 'w') as f: f.write(NICK+'|'+PASS+'|'+ROOM+'| |999|9c2afc|2da446|0|11')

TestBot_thread = threading.Thread(target=TestBot.main,)
TestBot_thread.setDaemon(True)
TestBot_thread.start()

class BotGUI(tkinter.Tk):

  def Select(event):
    if 'http' in '\n'.join([listbox.get(x) for x in listbox.curselection()]):
      for i in '\n'.join([listbox.get(x) for x in listbox.curselection()]).split():
        if 'http' in i:
          webbrowser.open(i)
          return #Return added so only uses one link in message

  def get(event):
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
      elif '!ignore' in text.get():
        if text.get().split()[1] in TestBot.Ignored:
          TestBot.Ignored += text.get().split()[1]
        else:
          TestBot.Ignored = TestBot.Ignored.replace(text.get().split()[1],"")
      else:
        room = TestBot.getRoom(ROOM)
        room.message(text.get(), False)  
    except Exception as error: print (error)
    text.delete(0,20000) #Clears Textfield
  
  GUI = tkinter.Tk()
  GUI.title('Chat Client')
  GUI.geometry("360x660")
  GUI.minsize(100,100)
  GUI.wm_attributes("-topmost", 1)
  global listbox,text
  text = Entry(GUI)
  text.bind('<Return>', get)
  listbox = Listbox(GUI)
  listbox.bind('<<ListboxSelect>>',Select)
  text.pack(fill=BOTH, side='bottom')
  listbox.config(bg='#'+Settings[4], borderwidth=0, selectborderwidth=0, height=20)
  listbox.pack(side='right',fill=BOTH, expand=1)

gui_thread = threading.Thread(target=tkinter.mainloop(),)
gui_thread.setDaemon(True)
gui_thread.start()
