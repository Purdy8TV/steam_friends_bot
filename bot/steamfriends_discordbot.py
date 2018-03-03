import time
import requests
import telepot

class steamFriendbotapi():


    def __init__(self, botapi, steamapi, steamids, gamedb, chatid):
        self.botapi = botapi
        self.steamapi = steamapi
        self.steamids = steamids
        self.gamedb = gamedb
        self.chatid = chatid

        # Variables
        self.returned_game = None

        # Dictionaries for last game
        self.steam_lastgame = {}
        for i in range(0, len(steamids)):
            self.steam_lastgame[steamids[i]]=''

    # Initialise Bot
    def init_bot(self):
        mybot = telepot.Bot(self.botapi)
        return mybot
    
    def string_request(self, friendslink):
        requested_string = ('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s'
                            % (self.steamapi, self.steamids[friendslink]))
        return requested_string

    def game_check(self, friendslink):
        if self.returned_game != self.steam_lastgame[self.steamids[friendslink]]:
            return True
    
    def update_game(self, friendslink):
        self.steam_lastgame[self.steamids[friendslink]] = self.returned_game

    def reset_game(self, friendslink):
        self.steam_lastgame[self.steamids[friendslink]] = ''

    def execute(self):
        mybot = self.init_bot()
        while True:
            for friends in range(0, len(self.steamids)):
                request_string = self.string_request(friends)
                try:
                    # Request username and appid from user profile
                    req = requests.get(request_string)
                    j = req.json()
                    returned_name = j['response']['players'][0]['personaname']
                    returned_id = j['response']['players'][0]['gameid']
                    # Look up game name via app id in steam db
                    req_name_from_id = requests.get(self.gamedb)
                    j_2 = req_name_from_id.json()
                    for app in j_2['applist']['apps']:
                        if app['appid'] == int(returned_id):
                            returned_game = app['name']
                            break
                    print(returned_game)

                except:
                    if req.raise_for_status() is not None:
                        print(req.raise_for_status())
                    self.reset_game(friends)
                    continue
                
                

                try:
                    if self.game_check(friends) is True:
                        self.update_game(friends)
                        message_to_send = ('%s is now playing %s' % (returned_name,
                                                                    returned_game))
                        print(message_to_send)
                        try:
                            mybot.sendMessage(self.chatid, message_to_send)

                        # Revisit this. No time to capture error term, should've done on initial testing.

                        except:
                            print('Issue with mybot send message')
                            print('Wanted to send - %s' % message_to_send)
                            time.sleep(5)
                            mybot.sendMessage(self.chatid, message_to_send)

                    # Revisit this. No time to capture error term, should've done on initial testing.
                    # This reset_game isn't being used, figure out why it works above and how this isn't required.

                except:
                    self.reset_game(friends)
                    print('%s is not playing anything' % (returned_name))
                
                time.sleep(5)

