import ch, re, json
import threading
import time
import webbrowser

import tkinter as tk
try:
  from tkinter import ttk
  spawner = tk.ttk
except:
  spawner = tk

try:
  with open ('settingss.json') as f:
    settings = json.loads (f.read ())
except:
  settings = {
    'name': input ('user name'),
    'password': input ('password'),
    'room': input ('room'),
    'ignored': []
  }

class TestBot(ch.RoomManager):
  def onConnect (self, room):
    self.setNameColor ("333333")
    self.setFontColor ("FFFFFF")
    self.setFontFace ("Latha")
    self.setFontSize (11)
    self.gui.post ('connected to {}'.format (room.name))

  def onMessage (self, room, user, message):
    if user.name not in settings['ignored']:
      self.gui.post ('{}: {}'.format (user.name, message.body))

class BotGUI (tk.Frame):
  def __init__ (self, master = None):
    spawner.Frame.__init__ (self, master)
    self.pack (fill = tk.BOTH, expand = True)
    self.createWidgets ()

    self.bot = TestBot (settings['name'], settings['password'])
    self.bot.gui = self
    self.bot.joinRoom (settings['room'])
    self.botThread = threading.Thread (target = self.bot.main,)
    self.botThread.start ()

  def get (self, event):
    message = self.text.get ()
    post = False
    r = re.match (r'^!(\w+) (.+)', message)
    if not r:
      post = True
    elif r.group (1) == 'bg':
      self.helperCanvas.config (bg = r.group (2))
    elif r.group (1) == 'nc':
      pass
    elif r.group (1) == 'bc':
      pass
    elif r.group (1) == 'bs':
      pass
    elif r.group (1) == 'font':
      pass
    elif r.group (1) == 'ignore':
      pass
    else:
      post = True

    if post:
      self.bot.getRoom (settings['room']).message (message, False)

    self.text.delete (0,20000) #Clears Textfield

  def post (self, message):
    w = self.helperCanvas.winfo_width ()
    newEntry = spawner.Label (self.messageStream, text = message,
      justify = tk.LEFT, width = w, wraplength = w)
    newEntry.pack (side = tk.TOP)
    self.messageStream.update_idletasks ()
    self.helperCanvas.configure (scrollregion = (0, 0,
      self.messageStream.winfo_width (), self.messageStream.winfo_height ()))

  def createWidgets (self):
    self.messageFrame = spawner.Frame (self)
    self.messageFrame.pack (side = tk.TOP, fill = tk.BOTH, expand = True)
    self.messageFrame.grid_rowconfigure (0, weight = 1)
    self.messageFrame.grid_columnconfigure (0, weight = 1)

    self.helperCanvas = tk.Canvas (self.messageFrame)
    self.helperCanvas.grid (row = 0, column = 0, sticky = tk.NSEW)

    vsb = spawner.Scrollbar (self.messageFrame, orient = tk.VERTICAL,
      command = self.helperCanvas.yview)
    vsb.grid (row = 0, column = 1, sticky = tk.NS)
    self.helperCanvas.configure (yscrollcommand = vsb.set)

    self.messageStream = spawner.Frame (self.helperCanvas)
    self.helperCanvas.create_window (0, 0, window = self.messageStream,
      anchor = tk.NW)

    self.messageStream.update_idletasks ()
    self.helperCanvas.configure (scrollregion = (0, 0,
      self.messageStream.winfo_width (), self.messageStream.winfo_height ()))

    #listbox = Listbox (root)
    #listbox.bind ('<<ListboxSelect>>',Select)
    self.text = spawner.Entry (root, width = '0')
    self.text.pack (side = tk.LEFT, fill = tk.X, expand = True)
    self.text.bind ('<Return>', self.get)
    #listbox.config (bg='#484848', borderwidth=0, selectborderwidth=0)
    #listbox.pack (side='right', fill=BOTH, expand=1)
    self.post ('test')

root = tk.Tk ()
root.title ('Chat Client')
root.geometry ("360x660")
root.minsize (100,100)
gui = BotGUI (master = root)
gui.mainloop ()

# gui_thread = threading.Thread (target = gui.mainloop,)
# gui_thread.setDaemon (True)
# gui_thread.start ()
