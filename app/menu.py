try:
    from tkinter import *
    import os
    import pyautogui as pg
    import PIL
    import pygame
    import time
    import random
except ModuleNotFoundError:
    os.system('python install.py')

name = pg.prompt('Enter your name:', title = 'Hello!)')
if name == 'Cancel' or name == None:
    name = 'Anonymus'

record = 0

try:
    with open('log.txt', 'r') as fr:
        s = fr.readlines()
        s[0] = s[0][:-1]
        if s[0] == name:
            record = int(s[1])
except:
    with open('log.txt','w') as fw:
        fw.write('{}\n0'.format(name))


root = Tk()
root.title('Main Menu')
root.geometry('400x300')

def startgame():
    global lab_record
    root.withdraw()
    os.system('python game.py')
    root.deiconify()
    lab_record.destroy()
    with open('log.txt', 'r') as fr:
        s = fr.readlines()
        record = s[1]
    lab_record = Label(root, font = ('Arial',18), text = 'Your record score: {}'.format(record))
    lab_record.pack()

btn = Button(root, text = 'START',bg = 'lightblue',fg = 'black',command = startgame, width = 15,height = 3)
btn.place(x = 50,y = 200)

lab_name = Label(root, font = ('Arial',18), text = 'Your name >>> {}'.format(name.upper()))
lab_name.pack()

lab_record = Label(root, font = ('Arial',18), text = 'Your record score: {}'.format(record))
lab_record.pack()

ext_btn = Button(root, width = 15, height = 3, text = 'EXIT', bg = 'orange', fg = 'black', command = exit)
ext_btn.place(x = 200, y = 200)

root.mainloop()
