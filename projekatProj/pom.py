from tkinter import *
from PIL import ImageTk, Image
import pygame
from tkinter import filedialog

from click import command

from FaceRecognition import *
from Database import *
from emotionDetection import *

curUser = User("", "", "")

pathSongFile = 'C:/Users/Korisnik/Desktop/faks/music'
FIRST_MENU = 1

def contain(item):
    iscontain = item in app.getFrame2().getSL().get(0, "end")
    return iscontain


def showMySongs():
    app.getFrame2().addSongsFromDB()
    app.getFrame2().replace_menu()
    app.getFrame2().tkraise()


def removeSongFun():
    pygame.mixer.music.stop()
    app.getFrame1().songName = ""
    song = app.getFrame2().getSL().get(ANCHOR)
    app.getFrame2().getSL().delete(ANCHOR)
    if song is not None:
        deleteSongDB(song, app.getLoginPage().getCurusername())

    app.getFrame2().tkraise()

def logOut():
    pygame.mixer.music.stop()
    app.getFrame1().songName = "..."
    app.getLoginPage().curUsername = ""
    curUser = User("", "", "")
    # app.getFrame1().menubar.delete(1)
    # app.getFrame1().menubar.delete(2)
    # app.getFrame1().menubar.delete(3)
    # app.getFrame1().menubar.delete(4)
    # app.getFrame1().menubar.delete(5)


    app.getStartPage().tkraise()
    emptyEmptyMenu = Menu(app.root)
    app.root.config(menu=emptyEmptyMenu)
    # app.getStartPage().master.menu = app.getFrame1().menubar

def emotionDetectionFun():
    print("emotionDetectionFun")
    app.getFaceEmotionPage().tkraise()

def addSongFun():
    app.getFrame2().addSongsFromDB()
    song = filedialog.askopenfilename(initialdir=f'{pathSongFile}', title="Choos a song",
                                      filetypes=(("mp3 files", "*.mp3"),))

    song = song.replace(f"{pathSongFile}/", "")
    song = song.replace(".mp3", "")
    allPathSong = song
    if (not (contain(song))):
        print("Nije nasao pesmu")
        addSongDB(allPathSong, app.getLoginPage().getCurusername())

        app.getFrame2().getSL().insert(END, song)
    app.getFrame2().replace_menu()
    app.getFrame2().tkraise()


def playSongEmotion():
    song = app.getFrame2().getSL().get(0)
    songCut = song
    song = f'{pathSongFile}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    app.getFrame1().songName.configure(text=f'{songCut}')
    app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)
    app.getFrame1().removeSongs.entryconfig("Remove One Song", state="disabled")
    app.getFrame1().tkraise()

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
        app.getFrame1().removeSongs.entryconfig("Remove One Song", state="disabled")
        app.getFrame1().tkraise()
    else:
        print("Nista nije selektovano")


def playSongF1():
    pygame.mixer.music.unpause()
    app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)


def pauseSongF1():
    pygame.mixer.music.pause()
    app.getFrame1().playBtn.configure(image=app.getFrame1().playImg, command=playSongF1)


def playPrevSong():
    song2 = app.getFrame2().getSL().get(ACTIVE)
    if song2 == app.getFrame2().getSL().get(0):
        song = app.getFrame2().getSL().get("end")
        nextOne = app.getFrame2().getSL().index("end") - 1  # index dohvata duzinu
        print(nextOne)
    else:
        nextOne = app.getFrame2().getSL().curselection()
        nextOne = nextOne[0] - 1
        song = app.getFrame2().getSL().get(nextOne)

    songCut = song
    song = f'{pathSongFile}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    app.getFrame1().songName.configure(text=f'{songCut}')
    app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)

    app.getFrame2().getSL().selection_clear(0, END)
    app.getFrame2().getSL().activate(nextOne)
    app.getFrame2().getSL().selection_set(nextOne, last=None)


def playNextSong():
    song2 = app.getFrame2().getSL().get(ACTIVE)
    if song2 == app.getFrame2().getSL().get("end"):
        song = app.getFrame2().getSL().get(0)
        nextOne = 0
    else:
        nextOne = app.getFrame2().getSL().curselection()
        nextOne = nextOne[0] + 1
        song = app.getFrame2().getSL().get(nextOne)

    songCut = song
    song = f'{pathSongFile}/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    app.getFrame1().songName.configure(text=f'{songCut}')
    app.getFrame1().playBtn.configure(image=app.getFrame1().pauseImg, command=pauseSongF1)

    app.getFrame2().getSL().selection_clear(0, END)
    app.getFrame2().getSL().activate(nextOne)
    app.getFrame2().getSL().selection_set(nextOne, last=None)


class MusicPlayerApp:
    root1 = Tk()
    def __init__(self):
        self.root = self.root1
        container = Frame(self.root, width=250, height=150)

        self.root.title('MusicPlayer')
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#f2f0ed')

        pygame.init()
        self.frames = {}

        for F in (StartPage, Page1, Page2, RegisterPage, LoginPage, FaceEmotionPage):
            frame = F(self.root, self, container)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        pygame.mixer.init()
        self.frames[StartPage].tkraise()

        self.create_menu()

    def create_menu(self):
        print("Create menu")
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        # self.menubar.add_command(label='')
        self.menu = self.menubar

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

    def getFaceEmotionPage(self):
        return self.frames[FaceEmotionPage]


class Page1(Frame):
    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)

        # Images
        self.parent = parent
        self.root = root
        self.playImg = ImageTk.PhotoImage(Image.open('images/blackPlay.png').resize((60, 60)))
        self.nextImg = ImageTk.PhotoImage(Image.open('images/blackNext.png').resize((40, 40)))

        self.prevImg = ImageTk.PhotoImage(Image.open('images/prevBlack.png').resize((40, 40)))
        self.pauseImg = ImageTk.PhotoImage(Image.open('images/blackPauzica.png').resize((60, 60)))
        self.pozadina = ImageTk.PhotoImage(Image.open('images/slika.jpg').resize((450, 200)))
        self.emotionImg = ImageTk.PhotoImage(Image.open('images/blackPauzica.png').resize((40, 40)))

        # bg image

        labela = Label(self, image=self.pozadina)
        labela.grid(row=1, column=0, columnspan=3, padx=25)

        # SongName
        self.songName = Label(self, text=" ... ", fg="black")
        self.songName.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        # F1 Buttons

        self.prevBtn = Button(self, image=self.prevImg, bg='#f2f0ed', borderwidth=0, command=playPrevSong)
        self.nextBtn = Button(self, image=self.nextImg, bg='#f2f0ed', borderwidth=0, command=playNextSong)
        self.playBtn = Button(self, image=self.playImg, bg='#f2f0ed', borderwidth=0, command=playSongF1)


        self.pauseBtn = Button(self, image=self.pauseImg, bg='#f2f0ed', borderwidth=0)

        self.prevBtn.grid(row=3, column=0, pady=5)
        self.playBtn.grid(row=3, column=1)
        self.nextBtn.grid(row=3, column=2)

        self.fistMenu = 1


    def replace_menu(self):
        if(self.fistMenu == 1):
            self.fistMenu = 0
            self.menubar = app.menubar
            #self.menubar = app.emptyMenu
            addSong = Menu(self.menubar)
            shSongs = Menu(self.menubar)
            smartPlayer = Menu(self.menubar)
            self.removeSongs = Menu(self.menubar)
            userMenu = Menu(self.menubar)




            self.menubar.add_cascade(label="Add Song", menu=addSong)
            addSong.add_command(label="Add one song", command=addSongFun)
            self.menubar.add_cascade(label="Remove Song", menu=self.removeSongs)
            self.removeSongs.add_command(label="Remove One Song", command=removeSongFun)

            self.removeSongs.entryconfig("Remove One Song", state="disabled")

            self.menubar.add_cascade(label="My Songs", menu=shSongs)
            shSongs.add_command(label="Show My Songs", command=showMySongs)

            self.menubar.add_cascade(label="Smart Player", menu=smartPlayer)
            smartPlayer.add_command(label="Face Emotion", command=emotionDetectionFun)

            blankmenu = Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label=" ".ljust(40), menu=blankmenu)

            self.master.userIcon = ImageTk.PhotoImage(Image.open(r'images/blackPauzica.png').resize((20,20)))
            # self.labela3 = Label(self, text="AaAaaaa")
            # self.labela3.place(relx=1.0,
            #        rely=0.0,
            #        anchor='ne')
            self.menubar.add_cascade(label="Profile",  menu=userMenu)
            self.userNameLabel = Label(self, text=app.getLoginPage().getCurusername(), fg="#5e3670",font=('bold'))
            userMenu.add_command(label="* "+app.getLoginPage().getCurusername()+" *")
            userMenu.add_command(label="  Log out", command=logOut)


           # self.master.menu = self.menubar

        app.root.config(menu=self.menubar)
    def getSName(self):
        return self.songName


class Page2(Frame):

    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)
        # F2 SongList
        self.songList = Listbox(self, bg='#492a57', fg="white", width=80, height=12, selectforeground="white",
                                selectbackground="#918e91")

        self.songList.grid(row=1, column=0, columnspan=3, pady=10, padx=10)
        self.playBtn2 = Button(self, text="Play song", bg='#adacad', width=12, pady=5, highlightbackground="#918e91",
                               fg="#5e3670",
                               font=('bold'), command=playSongF2)
        self.playBtn2.grid(row=2, column=1)

    def replace_menu(self):
        self.menubar = app.getFrame1().menubar
        addSong = Menu(self.menubar)
        shSongs = Menu(self.menubar)
        removeSongs = Menu(self.menubar)
        smartPlayer = Menu(self.menubar)

        app.getFrame1().removeSongs.entryconfig("Remove One Song", state="normal")

        self.master.menu = self.menubar

    def getSL(self):
        return self.songList

    def addSongsFromDB(self):
        songs = getAllSongs(app.getLoginPage().getCurusername())
        if songs is not None:
            for s in songs:
                if (not (contain(s))):
                    self.songList.insert(END, s)


class StartPage(Frame):
    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)
        self.grid_propagate(False)

        self.configure(bg="#0a3f6b")

        # bg image
        self.pozadina = ImageTk.PhotoImage(Image.open('images/StartPageBg.jpeg').resize((500, 240)))
        labela = Label(self, image=self.pozadina, bg="#0a3f6b")
        labela.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        # btn for LOGIN
        self.btn1Img = ImageTk.PhotoImage(Image.open('images/LoginButton.png').resize((200, 60)))
        self.btn1 = Button(self, image=self.btn1Img, bg='#0a3f6b', borderwidth=0, command=self.loginFun,
                           activebackground="#0a3f6b")
        self.btn1.grid(row=1, column=0, padx=25, pady=10)

        # btn for REGISTER
        self.btn2Img = ImageTk.PhotoImage(Image.open('images/RegisterButton.png').resize((200, 60)))
        self.btn2 = Button(self, image=self.btn2Img, bg='#0a3f6b', borderwidth=0, command=self.registerFun,
                           activebackground="#0a3f6b")
        self.btn2.grid(row=1, column=1, padx=25, pady=10)

    def registerFun(self):
        app.getRegisterPage().tkraise()

    def loginFun(self):
        app.getLoginPage().tkraise()
        # app.getLoginPage().faceR.run()


class RegisterPage(Frame):
    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)
        self.configure(bg="#103748")

        # bg image
        self.pozadina = ImageTk.PhotoImage(Image.open('images/regImg3.png').resize((200, 350)))
        labela = Label(self, image=self.pozadina, bg="#103748")
        labela.grid(row=0, column=0, padx=0, pady=0, rowspan=8)

        self.emptyL = Label(self, text="     ", bg="#103748")
        self.emptyL.grid(row=0, column=1)
        self.name = Label(self, text="Name      ", bg='#103748', fg="white")
        self.surname = Label(self, text="Surname ", bg='#103748', fg="white")
        self.username = Label(self, text="Username", bg='#103748', fg="white")
        self.name.grid(row=1, column=1, padx=20)
        self.surname.grid(row=2, column=1, padx=20)
        self.username.grid(row=3, column=1, padx=20)
        self.nameVar = StringVar
        self.surnameVar = StringVar
        self.usernameVar = StringVar

        self.nameentry = Entry(self, textvariable=self.nameVar)
        self.surnameentry = Entry(self, textvariable=self.surnameVar)
        self.usernameentry = Entry(self, textvariable=self.usernameVar)
        self.nameentry.grid(row=1, column=2)
        self.surnameentry.grid(row=2, column=2)
        self.usernameentry.grid(row=3, column=2)
        # self.empty = Label(self, text="     ", bg='#103748')
        # self.empty.grid(row=4, column=1)

        # submit button
        self.submitImg = ImageTk.PhotoImage(Image.open('images/submitPNG.png').resize((80, 60)))
        self.btn = Button(self, image=self.submitImg, bg='#103748', borderwidth=0, activebackground="#103748",
                          command=self.submitFun, state="disabled")
        self.btn.grid(row=5, column=1)

        # check button
        self.checkImg = ImageTk.PhotoImage(Image.open('images/checkImg.png').resize((30, 30)))
        self.checkOkImg = ImageTk.PhotoImage(Image.open('images/checkOK.png').resize((30, 30)))
        self.checkXImg = ImageTk.PhotoImage(Image.open('images/redXbutton.png').resize((30, 30)))
        self.checkUsernameBtn = Button(self, image=self.checkImg, bg='#103748', borderwidth=0,
                                       activebackground="#103748", command=self.checkUsername)
        self.checkUsernameBtn.grid(row=3, column=3)

        # web cam button
        self.camImg = ImageTk.PhotoImage(Image.open('images/cam3.png').resize((80, 60)))
        self.btnWebCam = Button(self, image=self.camImg, bg='#103748', borderwidth=0, activebackground="#103748",
                                command=self.openWebCam,
                                state="disabled")
        self.btnWebCam.grid(row=5, column=2)

        # self.empty = Label(self, text="     ", bg='#103748')
        # self.empty.grid(row=6, column=1)
        self.emptyInput = Label(self, text="Please, first enter your username!", bg='#103748', fg="white")
        self.emptyInput.grid(row=6, column=1, columnspan=2)

    def submitFun(self):
        if (self.nameentry.get() == "" or self.surnameentry.get() == "" or self.usernameentry.get() == ""):
            self.emptyLabel.configure(text="Please, fill the all fields!", fg="white")
            return

        u = User(self.nameentry.get(), self.surnameentry.get(), self.usernameentry.get())
        correct = insert(u)
        if correct == 1:
            app.getFrame1().replace_menu()
            app.getLoginPage().curUsername = self.usernameentry.get()
            app.getFrame1().tkraise()
        else:
            self.emptyLabel.configure(text="Username already exists!", fg="white")
            return

    def checkUsername(self):

        if self.usernameentry.get() == "":
            self.emptyInput.configure(text="Please, first enter your username!", fg="white")
            self.checkUsernameBtn.configure(image=self.checkXImg)
            return

        correct = findUser(self.usernameentry.get())
        if correct == 1 :
            # menja se izgled CheckUsernameBtn
            self.btnWebCam.configure(state="normal")
            self.emptyInput.configure(text="")
            self.usernameentry.configure(state="disable")
            self.infoImg = ImageTk.PhotoImage(Image.open('images/infoPNG.png').resize((25, 25)))

            # self.emptyLabel = Label(self,
            #                         text=" Please, click on camera icon to open  your web \n camera. Press 'q' when  you want to take picture, \n and after that press submit for registration!",
            #                         bg="#103748", fg="white")
            self.emptyLabel = Label(self,
                                    text=" Please, click on camera icon to open  your web \n camera. Press 'q' when  you want to take picture!",
                                    bg="#103748", fg="white")
            self.emptyLabel.grid(row=6, column=1, columnspan=3)
            self.emptyLabel["compound"] = LEFT
            self.emptyLabel["image"] = self.infoImg
            self.checkUsernameBtn.configure(image=self.checkOkImg)
        else:
            # CheckUsernameBtn postaje crven
            self.emptyInput.configure(text="Username already exists!", fg="white")
            self.checkUsernameBtn.configure(image=self.checkXImg)

    def openWebCam(self):
        # self.emptyLabel.configure(text="Please, press 'q' if you want to take a picture!")
        app.getLoginPage().faceR.regRun(self.usernameentry.get())
        self.emptyLabel.configure(text="Your picture is taken and saved! \nPress submit for registration.", fg="white")
        self.btn.configure(state="normal")


class LoginPage(Frame):
    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)

        self.configure(bg="#24244a")

        # bg image
        self.pozadina = ImageTk.PhotoImage(Image.open('images/faceRecognition.jpg').resize((300, 350)))
        labela = Label(self, image=self.pozadina, bg="#24244a")
        labela.grid(row=0, column=0, padx=0, pady=0, rowspan=3)

        # controlFrame.grid(row=0, column=1, pady=50)
        # controlFrame.configure(bg="#24244a")
        # self.curUsername = ""
        # self.emptyL = Label(self, text="     ")
        # self.emptyL.grid(row=0, column=0)

        # web cam button

        self.camImg = ImageTk.PhotoImage(Image.open('images/cam3.png').resize((90, 65)))
        # self.btn2 = Button(self, image=self.btn2Img, bg='#0a3f6b', borderwidth=0, command=self.registerFun,
        #                  activebackground="#0a3f6b")
        self.btnWebCam = Button(self, image=self.camImg, bg='#24244a', fg="white", command=self.setLabel,
                                activebackground="#24244a", borderwidth=0)
        self.btnWebCam.grid(row=0, column=1, pady=0)

        self.eL = Label(self, bg="#24244a", text="     ")
        self.eL.grid(row=2, column=1)

        self.infoImg = ImageTk.PhotoImage(Image.open('images/infoPNG.png').resize((25, 25)))

        self.emptyLabel = Label(self,
                                text=" Please, click on camera icon to\n open your web camera.",
                                bg="#24244a", fg="white")
        self.emptyLabel.grid(row=2, column=1)
        self.emptyLabel["compound"] = LEFT
        self.emptyLabel["image"] = self.infoImg

        self.faceR = FaceRecog()

    def setLabel(self):
        self.emptyLabel.configure(text=" Press 'q' when you \n want to log in!")
        self.openWebCam()

    def openWebCam(self):
        # Pozivom run fje otvara se kamerica
        loginUsername = app.getLoginPage().faceR.run()
        if loginUsername != "":
            foundUser = loginDb(loginUsername)
            print(loginUsername)
            if foundUser is None:
                app.getLoginPage()
                print("Prazan User")
            else:
                curUser = foundUser
                self.curUsername = loginUsername

                app.getFrame1().replace_menu()
                app.getFrame1().tkraise()
        else:
            app.getStartPage().tkraise()

    def getCurusername(self):
        return self.curUsername

class FaceEmotionPage(Frame):
    def __init__(self, parent, root, container):
        Frame.__init__(self, parent)

        self.configure(bg="#325c86")
        self.pozadina = ImageTk.PhotoImage(Image.open('images/emotionPageCrop.jpg').resize((300, 300)))
        labela = Label(self, image=self.pozadina, bg="#325c86")
        labela.grid(row=0, column=0, padx=0, pady=0, rowspan=3)

        self.camImg = ImageTk.PhotoImage(Image.open('images/emDetectionIconWhite.png').resize((75, 70)))
        # self.btn2 = Button(self, image=self.btn2Img, bg='#0a3f6b', borderwidth=0, command=self.registerFun,
        #                  activebackground="#0a3f6b")
        self.btnWebCam = Button(self, image=self.camImg, bg='#325c86', fg="white", command=self.faceDetBtn,
                                activebackground="#325c86", borderwidth=0)
        self.btnWebCam.grid(row=0, column=1, pady=0)

        self.eL = Label(self, bg="#325c86", text="     ")
        self.eL.grid(row=2, column=1)

        self.infoImg = ImageTk.PhotoImage(Image.open('images/infoPNG.png').resize((25, 25)))

        self.emptyLabel = Label(self,
                                text=" Please, click on camera icon to\n open your web camera.",
                                bg="#325c86", fg="white")
        self.emptyLabel.grid(row=2, column=1)
        self.emptyLabel["compound"] = LEFT
        self.emptyLabel["image"] = self.infoImg

    def faceDetBtn(self):
        self.emotion = DetectionFun()
        playSongEmotion()



app = MusicPlayerApp()
app.root1.mainloop()
