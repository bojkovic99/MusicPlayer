from tkinter import *
from PIL import ImageTk, Image
import pygame
from tkinter import filedialog
from Database import *

curUser = User("", "", "")

pathSongFile = 'C:/Users/Korisnik/Desktop/faks/music'


def contain(item):
    iscontain = item in app.getFrame2().getSL().get(0, "end")
    return iscontain

def showMySongs():
    app.getFrame2().addSongsFromDB()
    app.getFrame2().tkraise()


def addSongFun():
    app.getFrame2().addSongsFromDB()
    song = filedialog.askopenfilename(initialdir=f'{pathSongFile}', title="Choos a song",
                                      filetypes=(("mp3 files", "*.mp3"),))

    song = song.replace(f"{pathSongFile}/", "")
    song = song.replace(".mp3", "")
    allPathSong = song
    if (not (contain(song))):
        addSongDB(allPathSong, app.getLoginPage().getCurusername())

        app.getFrame2().getSL().insert(END, song)

    app.getFrame2().tkraise()


def playSongF2():
    selection = app.getFrame2().getSL().curselection()
    if selection:
        song = app.getFrame2().getSL().get(ACTIVE)
        songCut = song
        song = f'{pathSongFile}/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        app.getFrame1().songName.configure(text=f'{songCut}')
        app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)
        app.getFrame1().tkraise()
    else:
        print("Nista nije selektovano")


def playSongF1():
    pygame.mixer.music.unpause()
    app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)


def pauseSongF1():
    pygame.mixer.music.pause()
    app.getFrame1().playBtn.configure(image=app.getFrame1().playImg, command=playSongF1)


class MusicPlayerApp:
    root1 = Tk()

    def __init__(self):
        root = self.root1
        root.title('MusicPlayer')
        root.geometry('500x300')
        root.resizable(0, 0)
        root.configure(bg='#f2f0ed')

        self.frames = {}

        for F in (StartPage, Page1, Page2, RegisterPage, LoginPage):
            frame = F(root, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(Page1)
        # Menu
        myMenu = Menu(root)
        root.config(menu=myMenu)

        addSong = Menu(myMenu)
        shSongs = Menu(myMenu)
        myMenu.add_cascade(label="Add Song", menu=addSong)
        addSong.add_command(label="Add one song", command=addSongFun)
        myMenu.add_cascade(label="My Songs", menu=shSongs)
        shSongs.add_command(label="Show My Songs", command=showMySongs)
        pygame.mixer.init()
        self.frames[StartPage].tkraise()


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def getFrame1(self):
        return self.frames[Page1]

    def getFrame2(self):
        return self.frames[Page2]

    def getStartPage(self):
        return self.frames[StartPage]

    def getRegisterPage(self):
        return self.frames[RegisterPage]

    def getLoginPage(self):
        return self.frames[LoginPage]


class Page1(Frame):
    def __init__(self, parent, root):
        Frame.__init__(self, parent)


        # Images
        self.playImg = ImageTk.PhotoImage(Image.open('images/blackPlay.png').resize((60, 60)))
        self.nextImg = ImageTk.PhotoImage(Image.open('images/blackNext.png').resize((40, 40)))

        self.prevImg = ImageTk.PhotoImage(Image.open('images/prevBlack.png').resize((40, 40)))
        self.pauseImg = ImageTk.PhotoImage(Image.open('images/blackPauzica.png').resize((60, 60)))
        self.pozadina = ImageTk.PhotoImage(Image.open('images/slika.jpg').resize((450, 200)))

        # bg image

        labela = Label(self, image=self.pozadina)
        labela.grid(row=1, column=0, columnspan=3, padx=25)

        # SongName
        self.songName = Label(self, text=" ... ", fg="black")
        self.songName.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # F1 Buttons

        self.prevBtn = Button(self, image=self.prevImg, bg='#f2f0ed', borderwidth=0)
        self.nextBtn = Button(self, image=self.nextImg, bg='#f2f0ed', borderwidth=0)
        self.playBtn = Button(self, image=self.playImg, bg='#f2f0ed', borderwidth=0, command=playSongF1)

        self.pauseBtn = Button(self, image=self.pauseImg, bg='#f2f0ed', borderwidth=0)

        self.prevBtn.grid(row=3, column=0, pady=5)
        self.playBtn.grid(row=3, column=1)
        self.nextBtn.grid(row=3, column=2)



    def getSName(self):
        return self.songName


class Page2(Frame):

    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        # F2 SongList
        self.songList = Listbox(self, bg='#492a57', fg="white", width=80, height=12, selectforeground="red")

        self.songList.grid(row=1, column=0, columnspan=3, pady=10, padx=10)
        self.playBtn2 = Button(self, text="Play song", bg='#adacad', width=12, pady=5, highlightbackground="#918e91",
                               fg="#5e3670",
                               font=('bold'), command=playSongF2)
        self.playBtn2.grid(row=2, column=1)

    def getSL(self):
        return self.songList

    def addSongsFromDB(self):
        songs = getAllSongs(app.getLoginPage().getCurusername())
        if songs is not None:
            for s in songs:
                if (not (contain(s))):
                    self.songList.insert(END, s)


class StartPage(Frame):
    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        self.btn1Img = ImageTk.PhotoImage(Image.open('images/Register-Now2.png').resize((200, 150)))
        self.btn2Img = ImageTk.PhotoImage(Image.open('images/li2.png').resize((200, 200)))
        self.btn1 = Button(self, image=self.btn1Img, bg='#f2f0ed', borderwidth=0, command=self.registerFun)
        self.btn2 = Button(self, image=self.btn2Img, bg='#f2f0ed', borderwidth=0, command=self.loginFun)
        self.btn2.pack(side="left", padx=25)
        self.btn1.pack(side="left", padx=25)

    def registerFun(self):
        app.getRegisterPage().tkraise()

    def loginFun(self):
        app.getLoginPage().tkraise()



class RegisterPage(Frame):
    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        self.emptyL = Label(self, text="     ")
        self.emptyL.grid(row=0, column=0)
        self.name = Label(self, text="Name      ")
        self.surname = Label(self, text="Surname ")
        self.username = Label(self, text="Username")
        self.name.grid(row=1, column=0, padx=20)
        self.surname.grid(row=2, column=0, padx=20)
        self.username.grid(row=3, column=0, padx=20)
        self.nameVar = StringVar
        self.surnameVar = StringVar
        self.usernameVar = StringVar

        self.nameentry = Entry(self, textvariable=self.nameVar)
        self.surnameentry = Entry(self, textvariable=self.surnameVar)
        self.usernameentry = Entry(self, textvariable=self.usernameVar)
        self.nameentry.grid(row=1, column=1)
        self.surnameentry.grid(row=2, column=1)
        self.usernameentry.grid(row=3, column=1)
        self.empty = Label(self, text="     ")
        self.empty.grid(row=4, column=0)

        self.btn = Button(self, text="Submit", bg='#f2f0ed', fg="black", command=self.submitFun)
        self.btn.grid(row=5, column=1)

        self.empty = Label(self, text="     ")
        self.empty.grid(row=6, column=0)

    def submitFun(self):
        if (self.nameentry.get() == "" or self.surnameentry.get() == "" or self.usernameentry.get() == ""):
            emptyInput = Label(self, text="Please, fill the all fields!")
            emptyInput.grid(row=7, column=1)
            return

        u = User(self.nameentry.get(), self.surnameentry.get(), self.usernameentry.get())
        correct = insert(u)
        if correct == 1:
            app.getFrame1().tkraise()
        else:
            userExist = Label(self, text="Username already exists!")
            userExist.grid(row=7, column=1)
            return


class LoginPage(Frame):
    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        self.curUsername = ""
        self.emptyL = Label(self, text="     ")
        self.emptyL.grid(row=0, column=0)
        self.username = Label(self, text="Userame      ")
        self.username.grid(row=1, column=0, padx=20)

        self.usernameVar = StringVar
        self.usernameentry = Entry(self, textvariable=self.usernameVar)
        self.usernameentry.grid(row=1, column=1)

        self.empty = Label(self, text="     ")
        self.empty.grid(row=2, column=0)

        self.btn = Button(self, text="Login", bg='#f2f0ed', fg="black", command=self.loginFun)
        self.btn.grid(row=3, column=1)

    def loginFun(self):
        pomUser = loginDb(self.usernameentry.get())
        if pomUser is None:
            app.getLoginPage()
            print("Prazan User")
        else:
            curUser = pomUser
            self.curUsername = self.usernameentry.get()

            app.getFrame1().tkraise()

    def getCurusername(self):
        return self.curUsername


app = MusicPlayerApp()
app.root1.mainloop()
