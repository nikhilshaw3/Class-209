from cProfile import label
from msilib.schema import ListBox
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Separator
from turtle import title
from unicodedata import name
from pip import main

PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
name = None
listbox = None
labelchat = None
text_message = None

def receiveMessage():
    global SERVER
    global BUFFER_SIZE

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
            else:
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass

def ConnectToServer():
    
    global SERVER
    global name
    global sending_file

    cname = name.get()

    SERVER.send(cname.encode())
    

def openChatWindow():
    
    print("\n\t\t\t\tIP MESSENGER")

    window = Tk()
    window.title('Messenger')
    window.geometry("500x350")

    global name
    global listbox
    global text_area
    global labelchat
    global text_message
    global filePathLabel

    name_label = Label(window , text="ENTER YOUR NAME" , font=("Calibri",10))
    name_label.place(x=10 , y=8)

    name = Entry(window , width=30 , font=("Calibri",10))
    name.place(x=120 , y=8)
    name.focus()

    connect_server = Button(window , text="Connect To Chat Server" , bd = 1 , font=("Calibri",10) , command=ConnectToServer)
    connect_server.place(x=350 , y=6)

    separator = ttk.Separator(window , orient='horizontal')
    separator.place(x=0 , y=35 , relwidth=1 , height=0.1)

    label_users = Label(window , text="Active Users" , font=("Calibri",10))
    label_users.place(x=10 , y=50)

    listbox = Listbox(window , height=5 , width = 67 , activestyle = 'dotbox' , font=("Calibri",10))
    listbox.place(x=10 , y=70)

    scrollbar_1 = Scrollbar(listbox)
    scrollbar_1.place(relheight=1 , relx=1)
    scrollbar_1.config(command=listbox.yview)

    connect_button = Button(window , text="Connect" , bd=1 , font=("Calibri",10))
    connect_button.place(x=282 , y=160)

    disconnect_button = Button(window , text="Disconnect" , bd=1 , font=("Calibri",10))
    disconnect_button.place(x=350 , y=160)

    refresh_button = Button(window , text="Refresh" , bd=1 , font=("Calibri",10) , command=showClientList)
    refresh_button.place(x=435 , y=160)

    labelchat = Label(window, text="Chat Window" , font=("Calibri",10))
    labelchat.place(x=10 , y=180)

    text_area = Text(window , width=67 , height=6 , font=("Calibri",10))
    text_area.place(x=10 , y=200)

    scrollbar_2 = Scrollbar(text_area)
    scrollbar_2.place(relheight=1 , relx=1)
    scrollbar_2.config(command=text_area.yview)

    attach = Button(window,text="Attach & Send" , bd=1 , font=("Calibri",10))
    attach.place(x=10 , y=305)

    text_message = Entry(window , width = 43 , font=("Calibri",12))
    text_message.pack()
    text_message.place(x=98 , y=306)

    send_button = Button(window , text="Send" , bd=1 , font=("Calibri",10))
    send_button.place(x=450 , y=305)

    file_path_label = Label(window, text="" , fg="blue" , font=("Calibri",8))
    file_path_label.place(x=10 , y=330)

    window.mainloop()

def showClientList():
    global listbox

    listbox.delete(0,"end")

    SERVER.send("show list".encode('ascii'))


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    recive_thread = Thread(target = receiveMessage)
    recive_thread.start()
    
    openChatWindow()

setup()