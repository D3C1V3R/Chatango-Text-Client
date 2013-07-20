import ch
import threading
import tkinter
import time
import webbrowser
from tkinter import *

class TestBot(ch.RoomManager):
  def onConnect(self, room):
    self.setNameColor("333333")
    self.setFontColor("FFFFFF")
    self.setFontFace("Latha")
    self.setFontSize(11)
    TestBot.joinRoom('iwbtschat')
    self.ListNum = 0
    listbox.insert(END, 'Connected to '+room.name+'\n')
    with open ('ignored.txt', 'r') as f: self.GUIIgnored = f.read()

  def onMessage(self, room, user, message):
    if user.name not in self.GUIIgnored:
      self.ListNum += 1
      listbox.insert(END, user.name+'-'+time.strftime('%X')+'   '+message.body+'\n')
      listbox.itemconfig(self.ListNum,fg='#'+user.fontColor)
      listbox.yview_scroll(self.ListNum, 'p')
NICK = input("your account name: ")
PASS = input("your password: ")
TestBot = TestBot(NICK,PASS)

TestBot_thread = threading.Thread(target=TestBot.main,)
TestBot_thread.setDaemon(True)
TestBot_thread.start()
class BotGUI(tkinter.Tk):

  def Select(event):
    if 'http' in '\n'.join([listbox.get(x) for x in listbox.curselection()]):
      for i in '\n'.join([listbox.get(x) for x in listbox.curselection()]).split():
        if 'http' in i:
          webbrowser.open(i)
          return

  def get(event):

    if text.get() == '!connect':
      TestBot.joinRoom('iwbtschat')
    else:
      room = TestBot.getRoom('iwbtschat')
      room.message(text.get(), False)  
    text.delete(0,20000)
  
  GUI = tkinter.Tk()
  GUI.title('Bot Client')
  GUI.geometry("500x500+300+300")
  GUI.minsize(100,100)
  global listbox,text
  text = Entry(GUI)
  text.bind('<Return>', get)
  listbox = Listbox(GUI)
  listbox.bind('<<ListboxSelect>>',Select)
  text.pack(fill=BOTH, side='bottom')
  listbox.config(bg='#484848', borderwidth=0, selectborderwidth=0, height=20)
  listbox.pack(side='right',fill=BOTH, expand=1)

  GUI.update()

gui_thread = threading.Thread(target=tkinter.mainloop(),)
gui_thread.setDaemon(True)
gui_thread.start()
