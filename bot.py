import ch
import threading
import tkinter
import itertools
import time
import webbrowser
import tkHyperlinkManager
from tkinter import *

class TestBot(ch.RoomManager):
  def onLoginFail(self, room):
    print ('Login Combination of Username/Password Failed, Check your Settings.txt \n #########################################                                                                                  ')
  def onConnect(self, room):
    #GUI.title(ROOM + ' Chat Client')
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
      listbox.tag_add(str(self.ListNum)+'a', float(self.ListNum+1), float((self.ListNum)+ 1 + float(str('0.'+str(Message.index(' ')+1)))))
      Colour = user.fontColor[0]+user.fontColor[0]+user.fontColor[1]+user.fontColor[1]+user.fontColor[2]+user.fontColor[2]
      listbox.tag_configure(str(self.ListNum), font=user.fontFace.replace(' ','')+' '+str(Size)+' ', relief='raised', foreground='#'+Colour,)
      listbox.tag_configure(str(self.ListNum)+'a', font=user.fontFace.replace(' ','')+' '+str(Size)+' bold', relief='raised', foreground='White')
      print(str('0.'+str(Message.index(' '))))

      listbox.config(state='disabled')
Ignored,NICK,PASS,ROOM = [],"","",""

try:
  with open ('settings.txt', 'r') as f: 
    Settings=f.read().split('|')
    NICK= Settings[0]
    PASS = Settings[1]
    ROOM = Settings[2]
    Ignored = Settings[3]
    Size = Settings[9]
    TestBot = TestBot(NICK,PASS)
    TestBot.joinRoom(ROOM)
except IOError:
  with open ('settings.txt', 'w+') as f: f.write('USERNAME|PASSWORD|ROOMNAME|IGNOREDUSERS|333|9c2afc|2da446|0|11')
  print ('Creating Settings.txt file, Please edit the Settings.txt file and reopen')
  input ('Press Enter to quit.')
  quit()

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
      elif '!size' in text.get():
        Size = (int(text.get().split()[1]))
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
    listbox.config(state='disabled')
  
  GUI = tkinter.Tk()
  GUI.title(ROOM.upper() + ' Chat Client')
  GUI.geometry("300x660")
  GUI.minsize(100,100)
  GUI.wm_attributes("-topmost", 1)
  global listbox,text
  text = Entry(GUI)
  listbox = Text(GUI)
  text.bind('<Return>', get)
  text.pack(fill=BOTH, side='bottom')
  listbox.config(bg='#'+Settings[4], borderwidth=0, selectborderwidth=0, font=('Arial',str(Size),'bold') )
  listbox.pack(side='right',fill=BOTH, expand=1)

gui_thread = threading.Thread(target=tkinter.mainloop(),)
gui_thread.setDaemon(True)
gui_thread.start()
