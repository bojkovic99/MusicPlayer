import pymongo
from io import BytesIO
import numpy as np
from scipy.io.wavfile import read
import gridfs
from musicGenreTest import *

client = pymongo.MongoClient()

mydb = client["userdb"]
mycol = mydb["users"]
mycol2 = mydb["facerec"]
fs = gridfs.GridFS(mydb)


class User:
    def __init__(self, name, surname, username):
        self.name = name
        self.surname = surname
        self.username = username
        self.numSong = 0
        self.songs = []
        self.genres = ["rock", "serbian country", "classical", "pop"]

class User2:
    def __init__(self, name):
        self.ime = name
        self.face = []

def addFaceEnc(coordinate, name):
    u = User2(name)
    mycol2.insert({"pole":str(coordinate), "ime":name})

    #      mycol2.update({"ime":name}, {"$push": {"face": coor}})

def getFace(name):
    res = mycol2.find_one({"ime":name})
    if res is None:
        return None

    else:
       return res["pole"]



def insert(u):
    res = mycol.find_one({"username": u.username})
    if res is None:
        mycol.insert_one(u.__dict__)
        return 1
    else:
        print("Postoji korisnicko ime")
        return 0

def findUser(username):
    res = mycol.find_one({"username": username})
    if res is None:
        return 1
    else:
        return 0

def loginDb(username):
    res = mycol.find_one({"username": username})

    if res is None:
        return None

    for x in res:
        print(x)
        return x


def addSongDB(song, username):
    # rate, data = read(BytesIO(song))
    # mycol.update_one({"username": "valz"}, {"$push": {"songs": data.tolist(), "rate": rate}})

    # PRVO TREBA DA SE POZOVE FUNKCIJA ZA ODREDJIVANJE ZANRA!
    res = findGenre(song)
    print(res)

    mycol.update_one({"username": username}, {"$push": {"songs": {"nameSong":song, "genre": res} } })
    mycol.update_one({"username": username}, {"$inc": {"numSong": 1}})
    print(username)

def addGenreDB(array,username):
    mycol.update_one({"username": username}, {"$set": {"genres.0": array[0]}})
    mycol.update_one({"username": username}, {"$set": {"genres.1": array[1]}})
    mycol.update_one({"username": username}, {"$set": {"genres.2": array[2]}})
    mycol.update_one({"username": username}, {"$set": {"genres.3": array[3]}})


def deleteSongDB(song, username):
    print(song + " " + username)
    mycol.update_one({"username": username}, {"$pull": {"songs": { "nameSong": song} }})
    mycol.update_one({"username": username}, {"$inc": {"numSong": (-1)}})


def getAllSongs(username):
    res = mycol.find_one({"username": username})
    if res is None:
        return None

    else:
        if res["numSong"] == 0:
            return None
        else:
            print(res["songs"][0]["nameSong"])
            return (res["songs"])


def getAllUsernames():
    res = mycol.find({})
    if res is None:
        return None

    else:
        usernames = []
        for r in res:
            print(r["username"])
            usernames.append(r["username"])


        return usernames

def getGenreByEmotion(username,emotion):
    res = mycol.find_one({"username": username})
    if res is None:
        return -1
    else:
        return (res["genres"][emotion])

# def getSongsByGenre(username,genre):
#     res = mycol.find_one({"username": username , "songs": { "genre": genre} })
#     print(res)
#     if res is None:
#         return None
#
#     else:
#
#
#             return (res["songs"])

# mycol2.insert_one(t.__dict__)
# mycol2.update_one({"_id":1},{"$push":{"niz":5}})
# mycol.update_one({"username":"astakic"},{"$inc":{"numSong":1}})
