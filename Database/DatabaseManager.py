
from Logic.Player import Players
from pymongo import MongoClient
import json
with open("config.json", "r") as data:
	config = json.load(data)
client = MongoClient('localhost', serverSelectionTimeoutMS = 5000)
try:
	print("[DATABASE] Connecting to mongoDB cluster...")
	client.server_info()
except:
	print("[DATABASE] Failed to connect!")
	sys.exit()
print("[DATABASE] Succesfully connected to mongoDB cluster!")
db = client['dtale']
accounts = db['acc']
gamerooms = db['gamenrjejom']
clubs = db['clubs']
#accounts.create_index([('lowID', ASCENDING)], unique=True)

class DataBase:
    def loadAccount(self):
        user_data = accounts.find_one({'token': self.player.token})
        if user_data:
            self.player.name = user_data["name"]
            self.player.low_id = user_data["lowID"]
            self.player.vip = user_data["vip"]
            self.player.IsFacebookLinked = user_data["isFBLinked"]
            self.player.FacebookID = user_data["facebookID"]
            self.player.club_low_id = user_data["clubID"]
            self.player.club_role = user_data["clubRole"]
            self.player.player_experience = user_data["playerExp"]
            self.player.solo_wins = user_data["soloWins"]
            self.player.duo_wins = user_data["duoWins"]
            self.player.ThreeVSThree_wins = user_data["3vs3Wins"]
            self.player.gems = user_data["gems"]
            self.player.gold = user_data["gold"]
            self.player.star_points = user_data["starpoints"]
            self.player.tickets = user_data["tickets"]
            self.player.tokensdoubler = user_data["tokensdoubler"]
            self.player.player_tokens = user_data["playerTokens"]
            self.player.brawler_id = user_data["brawlerID"]
            self.player.skin_id = user_data["skinID"]
            self.player.profile_icon = user_data["profileIcon"]
            self.player.brawl_boxes = user_data["brawlBoxes"]
            self.player.big_boxes = user_data["bigBoxes"]
            self.player.brawlers_skins = user_data["brawlersSkins"]
            self.player.name_color = user_data["namecolor"]
            self.player.gadget = user_data["gadget"]
            self.player.links = user_data["links"]
            self.player.notifications = user_data["notifications"]
            self.player.Shop = user_data["Shop"]
            self.player.starpower = user_data["starpower"]
            self.player.DoNotDistrubMessage = user_data["DoNotDistrub"]
            self.player.UnlockedSkins = user_data["UnlockedSkins"]
            self.player.room_id = user_data["roomID"]
            self.player.brawlers_trophies_in_rank = user_data["brawlersTrophiesForRank"]
            self.player.brawlers_upgradium = user_data["brawlersUpgradePoints"]
            self.player.Brawler_level = user_data["brawlerPowerLevel"]
            self.player.brawlers_trophies = user_data["brawlersTrophies"]
            self.player.trophy_road = user_data["trophyRoad"]
            if self.player.UnlockType == "Off":
                self.player.BrawlersUnlockedState = user_data["UnlockedBrawlers"]
            player_total_trophies = 0
            for BrawlerID in self.player.brawlers_trophies.keys():
                player_total_trophies += self.player.brawlers_trophies[BrawlerID]
            self.player.trophies = player_total_trophies
            DataBase.replaceValue(self, 'trophies', self.player.trophies)
            if self.player.trophies < user_data["highesttrophies"]:
                self.player.highest_trophies = user_data["highesttrophies"]
            else:
                self.player.highest_trophies = self.player.trophies
                DataBase.replaceValue(self, 'highesttrophies', self.player.highest_trophies)
                
            
    def createAccount(self):
        Players.CreateNewBrawlersList()
        max_low_id_record = accounts.find_one({}, {"lowID": 1}, sort=[("lowID", -1)])
        self.player.low_id = (max_low_id_record["lowID"] + 1) if max_low_id_record else 1  # Увеличиваем на 1 или начинаем с 1
    
        data = {
            "token": str(self.player.token),
            "name": self.player.name,
            "lowID": self.player.low_id,
            "clubID": 0,
            "clubRole": 0,
            "isFBLinked": 0,
            "facebookID": self.player.FacebookID,
            "playerExp": self.player.max_experience,
            "experience": self.player.experience,
            "soloWins": self.player.solo_wins,
            "duoWins": self.player.duo_wins,
            "3vs3Wins": self.player.ThreeVSThree_wins,
            "gems": self.player.gems,
            "gold": self.player.gold,
            "notifications": self.player.notifications,
            "Shop": self.player.Shop,
            "starpoints": self.player.star_points,
            "tokensdoubler": self.player.tokensdoubler,
            "playerTokens": self.player.tokens,
            "tickets": self.player.tickets,
	    "UnlockedSkins": self.player.UnlockedSkins,
            "brawlerID": 0,
            "skinID": 0,
            "links": 0,
            "trophies": self.player.trophies,
            "highesttrophies": self.player.trophies,
            "profileIcon": 0,
            "namecolor": self.player.name_color,
            "brawlBoxes": self.player.brawl_boxes,
            "bigBoxes": self.player.big_boxes,
            "gadget": 255,
            "vip": self.player.vip,
            "starpower": 76,
            "DoNotDistrub": 0,
            "roomID": 0,
            "brawlersSkins": self.player.brawlers_skins,
            "brawlersTrophies": self.player.brawlers_trophies,
            "brawlersTrophiesForRank": self.player.brawlers_trophies_in_rank,
            "brawlersUpgradePoints": self.player.brawlers_upgradium,
            "brawlerPowerLevel": self.player.Brawler_level,
            "UnlockedBrawlers": self.player.BrawlersUnlockedState,
	    "SupportedContentCreator": self.player.content_creator,
	    "trophyRoad": self.player.trophy_road
        }
        existing_account = accounts.find_one({"lowID": data["lowID"]})
    
        if existing_account:
           print(f"Запись с lowID {data['lowID']} уже существует. Обновление записи...")
           accounts.update_one({"lowID": data["lowID"]}, {"$set": data})
           print("Запись успешно обновлена.")
        else:
            accounts.insert_one(data)
            print("Запись успешно добавлена.")
        
        
    def getAllPlayers(self):
        return list(accounts.find().sort("trophies", -1).limit(200))
        
    def getSpecifiedValue(self, value_name):
        account = accounts.find_one({'token': self.token})
        self.requested_val = account[value_name]
    def replaceValue(self, value_name, new_value):
        accounts.update_one(
            {'token': self.player.token},
            {'$set': {value_name: new_value}}
        )
        print("update ok!")

    def replaceOtherValue(self, target, value_name, new_value):
        accounts.update_one(
            {'lowID': target},
            {'$set': {value_name: new_value}}
        )    

    def addNotification(self, target, id, read=True, text="", sender=0):
        notif = DataBase.loadOtherAccount(self, target)["notifications"]
        notif.append({"id": id,
             "read": read,
             "time": Helpers.GetTime(self),
             "text": text,
             "sender": sender})
        DataBase.replaceOtherValue(self, target, "notifications", notif)
        
    def get_shop_offers():
        offers = list(db.acc.Shop.find({}))
        
        return offers    
    # Gameroom
    def createGameroomDB(self):
        data = { 
            "room_id": self.player.room_id,
            "mapID": self.player.map_id,
            "useGadget": 1,
            "players": {
                        str(self.player.low_id): {
                        "host": 1,
                        "lowID": self.player.low_id,
                        "name": self.player.name,
                        "Team": self.player.team,
                        "Ready": self.player.isReady,
                        "brawlerID": self.player.brawler_id,
                        "starpower": self.player.starpower,
                        "gadget": self.player.gadget,
                        "profileIcon": self.player.profile_icon,
                        "namecolor": self.player.name_color
                    }
                }
        }
        gamerooms.insert_one(data)
    def loadGameroom(self):
        gameroom_data = gamerooms.find_one({'room_id': self.player.room_id})
        if gameroom_data:
            self.mapID = gameroom_data["mapID"]
            self.useGadget = gameroom_data["useGadget"]
            self.playersdata = {}
            for low_id, info in gameroom_data["players"].items():
                self.playersdata[low_id] = {}
                self.playersdata[low_id]["IsHost"] = info["host"]
                self.playersdata[low_id]["name"] = info["name"]
                self.playersdata[low_id]["Team"] = info["Team"]
                self.playersdata[low_id]["Ready"] = info["Ready"]
                self.playersdata[low_id]["LowID"] = info["lowID"]
                self.playersdata[low_id]["profileIcon"] = info["profileIcon"]
                self.playersdata[low_id]["namecolor"] = info["namecolor"]
                self.playersdata[low_id]["brawlerID"] = info["brawlerID"]
                self.playersdata[low_id]["starpower"] = info["starpower"]
                self.playersdata[low_id]["gadget"] = info["gadget"]
            self.playerCount = len(self.playersdata)
        else:
            DataBase.replaceValue(self, 'roomID', 0)
            self.player.room_id = 0
    def replaceGameroomValue(self, value_name, new_value, type):
        gameroom_data = gamerooms.find_one({'room_id': self.player.room_id})
        if gameroom_data is None:
            DataBase.replaceValue(self, 'room_id', 0)
            return
        if type == "room" or type == "player":
            gamerooms.update_one(
            {'room_id': self.player.room_id},
            {'$set': {str(value_name): new_value}}
        )
        else:
            gamerooms.delete_one({'room_id': self.player.room_id})
    def UpdateGameroomPlayerInfo(self, low_id):
        gameroom_data = gamerooms.find_one({'room_id': self.player.room_id})
        gameroom_data["players"][str(low_id)]["Team"] = self.player.team
        gameroom_data["players"][str(low_id)]["Ready"] = self.player.isReady
        gameroom_data["players"][str(low_id)]["brawlerID"] = self.player.brawler_id
        gameroom_data["players"][str(low_id)]["starpower"] = self.player.starpower
        gameroom_data["players"][str(low_id)]["gadget"] = self.player.gadget
        gameroom_data["players"][str(low_id)]["profileIcon"] = self.player.profile_icon
        gameroom_data["players"][str(low_id)]["namecolor"] = self.player.name_color
        gamerooms.update_one({'room_id': self.player.room_id}, {'$set': gameroom_data})
    def createClub(self, clubid):
        data = {
            "clubID": clubid,
            "name": self.clubName,
            "description": self.clubdescription,
            "region": "RO",
            "badgeID": self.clubbadgeID,
            "type": self.clubtype,
            "trophiesneeded": self.clubtrophiesneeded,
            #"friendlyfamily": self.clubfriendlyfamily,
            "trophies": self.player.trophies,
            "members": {
                str(self.player.low_id): self.player.name
            },
            "chat": {
                "1": {
                    "Event": 2,
                    "Tick": 1,
                    "PlayerID": self.player.low_id,
                    "PlayerName": self.player.name,
                    "PlayerRole": 2,
                    "Message": "Добро пожаловать в клуб!"
                }
            }
        }
        clubs.insert_one(data)
    def CountClub(self, minMembers, maxMembers, clubType, maxListLength):
        print ("count xlub start")
        self.club_list = []
        self.club_data = []
        self.AllianceCount = 0
        for club in clubs.find():
            if self.AllianceCount == maxListLength:
                break
            if minMembers <= len(club['members']) < maxMembers and club['type'] <= clubType:
                self.club_list.append(club['clubID'])
                self.club_data.append(club)
                self.AllianceCount += 1
                print("ok? countclub")
                  
    def loadClub(self, clubid):
        club_data = clubs.find_one({'clubID': clubid})
        self.plrids = []
        self.clubName = club_data["name"]
        self.clubdescription = club_data["description"]
        self.clubregion = club_data["region"]
        self.clubbadgeID = club_data["badgeID"]
        self.clubtype = club_data["type"]
        self.clubtrophiesneeded = club_data["trophiesneeded"]
        self.clubfriendlyfamily = club_data["friendlyfamily"]
        self.clubtrophies = club_data["trophies"]
        self.clubmembercount = len(club_data["members"])
        for plridentifier, data in club_data["members"].items():
            if plridentifier != "totalmembers":
                self.plrids.append(int(plridentifier))
            
            
    def AddMember(self, AllianceID, PlayerID, PlayerName, Action):
        data = clubs.find_one({'clubID': AllianceID})
        if Action == 0:
            clubs.delete_one({'clubID': AllianceID})
        elif Action == 1:
            data['members'][str(PlayerID)] = PlayerName
            clubs.replace_one({'clubID': AllianceID}, data)
            accounts.update_one({'low_id': PlayerID}, {'$set': {'clubID': AllianceID, 'clubRole': 1}})
        elif Action == 2:
            try:
                data['members'].pop(str(PlayerID))
                clubs.replace_one({'clubID': AllianceID}, data)
                accounts.update_one({'low_id': PlayerID}, {'$set': {'clubID': 0, 'clubRole': 0}})
            except:
                pass
    def GetMemberData(self, Low_id):
        try:
            self.players = DataBase.getAllPlayers(self)
            for i in range(len(self.players)):
                if self.players[i]['lowID'] == int(Low_id):
                    self.lowplrid = self.players[i]['lowID']
                    self.plrrole = self.players[i]["clubRole"]
                    self.plrtrophies = self.players[i]["trophies"]
                    self.plrname = self.players[i]["name"]
                    self.plricon = self.players[i]["profileIcon"]
                    self.plrnamecolor = self.players[i]["namecolor"]
                    self.plrexperience = self.players[i]["playerExp"]
                    break
        except Exception as e:
            self.lowplrid = 1
            self.plrrole = 2
            self.plrtrophies = 0
            self.plrname = "Delete"
            self.plricon = 1
            self.plrnamecolor = 2
            self.plrexperience = 0
    def replaceClubValue(self, target, inf1, inf2, inf3, inf4, inf5):
        club_data = clubs.find_one({'clubID': target})
        club_data['description'] = inf1
        club_data['badgeID'] = inf2
        club_data['type'] = inf3
        club_data['trophiesneeded'] = inf4
        club_data['friendlyfamily'] = inf5
        clubs.replace_one({'clubID': target}, club_data)
    def GetmsgCount(self, clubID):
        self.MessageCount = len(clubs.find_one({'clubID': clubID})['chat'])
    def Addmsg(self, clubID, event, tick, Low_id, name, role, msg):
        data = clubs.find_one({'clubID': clubID})
        tick = len(data['chat']) + 1
        data['chat'][str(tick)] = {
            "Event": event,
            "Tick": tick,
            "PlayerID": Low_id,
            "PlayerName": name,
            "PlayerRole": role,
            "Message": msg,
        }
        clubs.replace_one({'clubID': clubID}, data)