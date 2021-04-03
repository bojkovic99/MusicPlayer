import pymongo
from io import BytesIO
import numpy as np
from scipy.io.wavfile import read

client = pymongo.MongoClient()

mydb = client["userdb"]
mycol = mydb["users"]


class User:
    def __init__(self, name, surname, username):
        self.name = name
        self.surname = surname
        self.username = username
        self.numSong = 0
        self.songs = []


def insert(u):
    res = mycol.find_one({"username": u.username})
    if res is None:
        mycol.insert_one(u.__dict__)
        return 1
    else:
        print("Postoji korisnicko ime")
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


def getAllSongs(username):
    res = mycol.find_one({"username": username})
    if res is None:
        return None

    else:
        if res["numSong"] == 0:
            return None
        else:
            return res["songs"]

# mycol2.insert_one(t.__dict__)
# mycol2.update_one({"_id":1},{"$push":{"niz":5}})
# mycol.update_one({"username":"astakic"},{"$inc":{"numSong":1}})
