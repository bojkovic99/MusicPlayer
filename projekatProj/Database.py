import pymongo
from io import BytesIO
import numpy as np
from scipy.io.wavfile import read
import gridfs

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
    mycol.update_one({"username": username}, {"$push": {"songs": song}})
    mycol.update_one({"username": username}, {"$inc": {"numSong": 1}})
    print(username)


def deleteSongDB(song, username):
    print(song + " " + username)
    mycol.update_one({"username": username}, {"$pull": {"songs": song}})
    mycol.update_one({"username": username}, {"$inc": {"numSong": (-1)}})


def getAllSongs(username):
    res = mycol.find_one({"username": username})
    if res is None:
        return None

    else:
        if res["numSong"] == 0:
            return None
        else:
            return res["songs"]


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


# mycol2.insert_one(t.__dict__)
# mycol2.update_one({"_id":1},{"$push":{"niz":5}})
# mycol.update_one({"username":"astakic"},{"$inc":{"numSong":1}})
