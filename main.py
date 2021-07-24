from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

ver='v0.1.5a'
username=''
settings={}
chat=[]
icon='./assets/icon.ico'

#get the previous chats locally
log=open('log.txt','r')
chat=log.readlines()
log.close()

def prev_chat():
    lines=''
    for i in chat:
        lines=lines+i
    return lines

def remove_spaces(sentence):
    return sentence.replace(' ','')

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


#sign-in window
def signin_win():
    global username
    def signin_entry():
        global username
        if(remove_spaces(signin_win_input.get())!=''):
            username=signin_win_input.get()
            signin_win.destroy()
            main_window()
        else:
            signin_win_input.delete(0,END)

    if(settings['remember_user']=='true'):
        username=settings['username']
        main_window()
    else:
        signin_win=Tk()
        signin_win.rowconfigure(0,weight=1)
        signin_win.rowconfigure(1,weight=1)
        signin_win.rowconfigure(2,weight=1)
        signin_win.columnconfigure(0,weight=1)
        signin_win.title('Sign In to Pycord')
        signin_win.iconbitmap(icon)
        signin_win.geometry('300x100')
        signin_win.resizable(False,False)
        Label(signin_win,text='Enter a username to continue').grid(row=0,column=0)
        signin_win_input=Entry(signin_win)
        signin_win_input.grid(row=1,column=0)
        Button(signin_win,text='Sign In',command=signin_entry).grid(row=2,column=0)
        signin_win.mainloop()

def main_window():
    global settings
    global chat

    #main window    
    root = Tk()
    root.title('Pycord')
    root.geometry('800x600')  
    root.iconbitmap(icon)
    root.resizable(False,False)
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=1)
    root.rowconfigure(2,weight=1)
    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=1)
    root.columnconfigure(2,weight=1)

    #main window draw   
    def send():
        if(remove_spaces(input.get())!=''):
            msg='['+username+']'+input.get()+'\n'
            chatbox.config(state=NORMAL)
            chatbox.insert(END,msg)
            chat.append(msg)
        input.delete(0,END)
        chatbox.config(state=DISABLED)

    chatbox=Text(root,state=DISABLED,bg=settings['chat_bg'],fg=settings['chat_fg'],font=(settings['font']+' 14'))
    Scrollbar(root,command=chatbox.yview).grid(row=0,column=1,sticky='nse')
    input=Entry(root,text='Type a message to send')
    Button(root,text='send',command=send).grid(row=1,column=1,sticky='e')
    Label(root,text='Signed in as: '+username).grid(row=2,column=0,sticky='w')
    Label(root,text=ver).grid(row=2,column=1,columnspan=1,sticky='e')
    chatbox.grid(row=0,columnspan=2,sticky='nsew')
    chatbox.yview_pickplace('end')
    input.grid(row=1,column=0,columnspan=2,sticky='ew')

    chatbox.config(state=NORMAL)
    chatbox.insert(END,prev_chat())
    chatbox.config(state=DISABLED)

    def preferences():
        remember_user=BooleanVar()
        user_color_scheme=IntVar()
        if(settings['chat_bg']=='#000000' and settings['chat_fg']=='#ffffff'):
            user_color_scheme.set(1)
        elif(settings['chat_bg']=='#676767' and settings['chat_fg']=='#E2E5DE'):
            user_color_scheme.set(2)
        elif(settings['chat_bg']=='#FBF2FF' and settings['chat_fg']=='#C030ED'):
            user_color_scheme.set(3)
        if(settings['remember_user']=='true'):
            remember_user.set(True)
        def apply():
            if(remember_user.get()==True):
                settings['remember_user']='true'
                settings['username']=username
            else:
                if(settings['remember_user']=='true'):
                    settings['remember_user']='false'
                    settings.pop('username')
            if(user_color_scheme.get()==1):
                settings['chat_bg']='#000000'
                settings['chat_fg']='#ffffff'
            elif(user_color_scheme.get()==2):
                settings['chat_bg']='#676767'
                settings['chat_fg']='#E2E5DE'
            elif(user_color_scheme.get()==3):
                settings['chat_bg']='#FBF2FF'
                settings['chat_fg']='#C030ED'
            chatbox.config(bg=settings['chat_bg'],fg=settings['chat_fg'])


        pref_win=Toplevel(root)
        pref_win.rowconfigure(0,weight=1)
        pref_win.rowconfigure(1,weight=1)
        pref_win.rowconfigure(2,weight=1)
        pref_win.rowconfigure(3,weight=1)
        pref_win.rowconfigure(4,weight=1)
        pref_win.columnconfigure(0,weight=1)
        pref_win.columnconfigure(1,weight=1)
        pref_win.columnconfigure(2,weight=1)
        pref_win.columnconfigure(3,weight=1)
        pref_win.title('Pycord preferences')
        pref_win.iconbitmap(icon)
        pref_win.geometry('350x150')
        pref_win.resizable(False,False)
        pref_win_remember_user=Checkbutton(pref_win,text='Remember this account?',variable=remember_user)
        pref_win_remember_user.var=remember_user
        pref_win_remember_user.grid(row=0,column=0,padx=(3,3))
        pref_win_frame=LabelFrame(pref_win,text='Colors')
        pref_win_frame.grid(row=1,column=0,columnspan=4,sticky='ew',padx=(5,5))
        colorscheme1,colorscheme2,colorscheme3=Radiobutton(pref_win_frame, text="Dark Mode",  variable = user_color_scheme, value = 1),Radiobutton(pref_win_frame, text="Normal Mode", variable = user_color_scheme, value = 2),Radiobutton(pref_win_frame, text="Light Mode",  variable = user_color_scheme, value = 3)
        colorscheme1.grid(row=0,column=0,sticky='w')
        colorscheme2.grid(row=1,column=0,sticky='w')
        colorscheme3.grid(row=2,column=0,sticky='w')
        colorscheme1.var,colorscheme2.var,colorscheme3.var=user_color_scheme,user_color_scheme,user_color_scheme
        Button(pref_win,text='Apply',command=apply).grid(row=4,column=2)
        Button(pref_win,text='OK',command=pref_win.destroy).grid(row=4,column=3)
    def signout():
        root.destroy()
        signin_win()
    def about():
        messagebox.showinfo('About','Pycord\n\nCopyright(c) 2021\nVersion: '+ver)
    menubar=Menu(root)
    options=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Options',menu=options)
    options.add_command(label='Preferences',command=preferences)
    options.add_command(label='Sign Out',command=signout)
    options.add_command(label='About',command=about)
    options.add_separator()
    options.add_command(label='Exit',command=root.destroy)
    root.config(menu=menubar)
    
    root.mainloop()

signin_win()

settings_line=''
for i in settings:
    settings_line=settings_line+i+'='+settings[i]+'\n'
settings_file=open('settings.txt','w')
settings_file.write(settings_line)
settings_file.close()

log=open('log.txt','w')
log.write(prev_chat())
log.close()