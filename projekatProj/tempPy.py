
from pydub import *
# assign files
# input_file = "C:/Users/Korisnik/Desktop/faks/music/Billie Eilish, Khalid - lovely.mp3"
# output_file = "C:/Users/Korisnik/Desktop/faks/music/Billie Eilish, Khalid - lovely - wav.wav"


src = "C:/Users/Korisnik/Desktop/faks/music/Billie Eilish, Khalid - lovely.mp3"
dst = "C:/Users/Korisnik/Desktop/faks/music/Billie Eilish, Khalid - lovely - wav.wav"

sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
