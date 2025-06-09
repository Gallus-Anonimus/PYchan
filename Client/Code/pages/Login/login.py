import tkinter as tk
from tkinter import *
from time import sleep
from tkinter import messagebox


class Login():
    def __init__(self,server):
        self.logged = False
        self.server=server
        self.okno = "login"

    def start(self):
        self.root = tk.Tk()
        self.root.geometry("300x150")
        self.root.resizable(Settings.RESIZEX, Settings.RESIZEY)
        self.okno="login"

        self.LoginScreen()

    def LoginScreen(self):
        dev_clear(self.root)
        self.root.title("Login to PYchan")

        self.labelName=Label(self.root,text="Login")
        self.entryName=Entry(self.root)
        self.labelPassword = Label(self.root, text="Password")
        self.entryPassword= Entry(self.root,show=u"\u25CF")
        self.labelName.pack()
        self.entryName.pack()
        self.labelPassword.pack()
        self.entryPassword.pack()

        self.btns()

    def Login(self):
        name=self.entryName.get()
        password=self.entryPassword.get()
        res=self.server.login(name,password)
        if not res.get("status")=="success":
            messagebox.showerror(title="Login Unsuccessful",message=res.get("message"))
        else:
            self.logged=True
            self.root.destroy()


    def RegisterScreen(self):
        dev_clear(self.root)
        self.root.title("Register to ZSEkret")

        self.labelName=Label(self.root,text="Name")
        self.entryName=Entry(self.root)
        self.labelPassword = Label(self.root, text="Password")
        self.entryPassword= Entry(self.root,show=u"\u25CF")
        self.labelName.pack()
        self.entryName.pack()
        self.labelPassword.pack()
        self.entryPassword.pack()
        self.btns()

    def Register(self):
        pass

    def IsLogged(self):
        return self.logged

    def btns(self):
        self.frame=Frame(self.root)
        self.loginbtn=Button(self.frame,text="Login")
        self.loginbtn.configure(bg="#37FD12")
        self.loginbtn.grid(row=0, column=0,pady=10,padx=10,ipadx=15,ipady=8,)

        self.registerbtn = Button(self.frame, text="Register")
        self.registerbtn.grid(row=0, column=1,pady=10,padx=10,ipadx=15,ipady=8)
        
        self.exitbtn = Button(self.frame,text="exit",command=lambda:self.root.destroy())
        self.exitbtn.configure(bg="#F72119",)
        self.exitbtn.grid(row=0, column=2,pady=10,padx=10,ipadx=15,ipady=8)

        if self.okno=="login":
            self.loginbtn.configure(command=self.Login)
            self.registerbtn.configure(command=self.RegisterScreen)
            self.okno="register"
        else:
            self.loginbtn.configure(command=self.LoginScreen)
            self.registerbtn.configure(command=self.Register)
            self.okno="login"            


        self.frame.pack()


def dev_clear(root):
    sleep(0.034)
    for w in root.winfo_children():
        w.destroy()


if __name__=="__main__":
    login=Login()
    login.start()
    