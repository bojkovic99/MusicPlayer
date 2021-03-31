from tkinter import *
from PIL import ImageTk, Image
import pygame
from tkinter import filedialog

root = Tk()
root.title('MusicPlayer')
root.geometry('500x300')
root.resizable(0, 0)
root.configure(bg='#f2f0ed')

f2 = Frame(root)
f1 = Frame(root)

f1.grid(row=0, column=0, sticky="nsew")
f2.grid(row=0, column=0, sticky="nsew")


def contain(item):
    iscontain = item in songList.get(0, "end")
    return iscontain


def addSondFun():
    song = filedialog.askopenfilename(initialdir='C:/Users/Korisnik/Desktop/faks/music', title="Choos a song",
                                      filetypes=(("mp3 files", "*.mp3"),))

    song = song.replace("C:/Users/Korisnik/Desktop/faks/music/", "")
    song = song.replace(".mp3", "")
    if (not (contain(song))):
        songList.insert(END, song)

    print("Caoo")

    f2.tkraise()


# Play choosen song

def playSongF2():
    selection = songList.curselection()
    if selection:
        song = songList.get(ACTIVE)
        songCut = song
        song = f'C:/Users/Korisnik/Desktop/faks/music/{song}.mp3'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        songName.configure(text=f'{songCut}')
        playBtn.configure(image=pauseImg, command=pauseSongF1)
        f1.tkraise()
    else:
        print("Nista nije selektovano")


def playSongF1():
    pygame.mixer.music.unpause()
    playBtn.configure(image=pauseImg, command=pauseSongF1)


def pauseSongF1():
    pygame.mixer.music.pause()
    playBtn.configure(image=playImg, command=playSongF1)


pygame.mixer.init()

# Images
playImg = ImageTk.PhotoImage(Image.open('images/blackPlay.png').resize((60, 60)))
nextImg = ImageTk.PhotoImage(Image.open('images/blackNext.png').resize((40, 40)))

prevImg = ImageTk.PhotoImage(Image.open('images/prevBlack.png').resize((40, 40)))
pauseImg = ImageTk.PhotoImage(Image.open('images/blackPauzica.png').resize((60, 60)))
pozadina = ImageTk.PhotoImage(Image.open('images/slika.jpg').resize((450, 200)))

# bg image

labela = Label(f1, image=pozadina)
labela.grid(row=1, column=0, columnspan=3, padx=25)

# SongName
songName = Label(f1, text=" ... ", fg="black")
songName.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

# F1 Buttons


prevBtn = Button(f1, image=prevImg, bg='#f2f0ed', borderwidth=0)
nextBtn = Button(f1, image=nextImg, bg='#f2f0ed', borderwidth=0)
playBtn = Button(f1, image=playImg, bg='#f2f0ed', borderwidth=0, command=playSongF1)

pauseBtn = Button(f1, image=pauseImg, bg='#f2f0ed', borderwidth=0)

prevBtn.grid(row=3, column=0, pady=5)
playBtn.grid(row=3, column=1)
nextBtn.grid(row=3, column=2)

# pauseBtn.grid(row=2, column=1)

# F2 SongList


# songList = Listbox(f2, bg='#492a57', fg="white", width=80, height=12, selectforeground="red") #5e3670
songList = Listbox(f2, bg='#5e3670', fg="white", width=80, height=12, selectbackground="#adacad")
songList.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

playBtn2 = Button(f2, text="Play song", bg='#adacad', width=12, pady=5 ,highlightbackground="#918e91", fg="#5e3670",
                  font=('bold'), command=playSongF2)
playBtn2.grid(row=2, column=1)

# Menu

myMenu = Menu(f1)
root.config(menu=myMenu)

addSong = Menu(myMenu)
myMenu.add_cascade(label="Add Song", menu=addSong)
addSong.add_command(label="Add one song", command=addSondFun)

f1.tkraise()

root.mainloop()
