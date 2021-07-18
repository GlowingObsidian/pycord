from tkinter import *
from tkinter import messagebox

ver='0.1.3a'
username=''
settings={}

#get the previous chats locally
log=open('log.txt','r')
prev_chat=log.read()
log.close()

#open chat log to write
log=open('log.txt','a')

settings_file=open('settings.txt','r')
settings_string=settings_file.read()
word,key,value='','',''
for i in settings_string:
    if(i=='='):
        key=word
        word=''
    elif(i=='\n'):
        value=word
        settings[key]=value
        key,value,word='','',''
    else:
        word=word+i
settings_file.close()

#main window
root = Tk()
root.title('Pycord')
#root.geometry('480x480')
root.iconbitmap('./icon.ico')
root.resizable(False,False)
remember_me=IntVar()


#main window draw
def send():
    value=input.get()
    if(value!='' and value!=' '):
        msg='<'+username+'>'+value+'\n'
        text.config(state=NORMAL)
        text.insert(END,msg)
        log.write(msg)
    input.delete(0,END)
    text.config(state=DISABLED)

text=Text(root,state=DISABLED,width=50,bg='#EEA47F',fg='#00539C')
scrollbar=Scrollbar(root,command=text.yview).grid(row=0,column=2,sticky='ns')
input=Entry(root,text='Type a message to send',state=DISABLED)
enter=Button(root,text='send',command=send).grid(row=1,column=1,columnspan=2,sticky='ew')
version=Label(root,text='ver'+ver).grid(row=2,column=1,columnspan=2,sticky='e')
text.grid(row=0,columnspan=2,sticky='ew')
input.grid(row=1,column=0,sticky='nsew')

#add menu bar
def signout():
    settings['remember_user']='false'
    settings.pop('username')
    root.destroy()

def about():
    messagebox.showinfo('About','Pycord\n\nCopyright(c) 2021\nCoded by The Glowing Obsidian\nVersion: '+ver)

menubar=Menu(root)
options=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Options',menu=options)
options.add_command(label='Sign Out',command=signout)
options.add_command(label='About',command=about)
options.add_separator()
options.add_command(label='Exit',command=root.destroy)
root.config(menu=menubar)

#sign-in popup window draw
def get_username():
    global username
    if(settings['remember_user']=='false'):
        username=signin_win_input.get()
        signin_win.destroy()
    name=Label(root,text='Signed in as: '+username).grid(row=2,column=0,sticky='w')
    input.config(state=NORMAL)
    text.config(state=NORMAL)
    text.insert(END,prev_chat)
    text.config(state=DISABLED)
    if(remember_me.get()==1):
        settings['remember_user']='true'
        settings['username']=username
    
if(settings['remember_user']=='true'):
    username=settings['username']
    get_username()
else:
    signin_win=Toplevel(root)
    signin_win.columnconfigure(0,weight=1)
    signin_win.title('Sign In to Pycord')
    signin_win.iconbitmap('./icon.ico')
    signin_win.geometry('300x100')
    signin_win.resizable(False,False)
    signin_win_intro=Label(signin_win,text='Enter a username to continue').grid(row=0,column=0)
    signin_win_input=Entry(signin_win)
    signin_win_input.grid(row=1,column=0)
    signin_win_button=Button(signin_win,text='Sign In',command=get_username).grid(row=2,column=0)
    signin_win_remember_me=Checkbutton(signin_win,text='Remember me',variable=remember_me).grid(row=3,column=0)

mainloop()
log.close()
settings_line=''
for i in settings:
    settings_line=settings_line+i+'='+settings[i]+'\n'
settings_file=open('settings.txt','w')
settings_file.write(settings_line)
settings_file.close()