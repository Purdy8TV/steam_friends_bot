import time
import requests
import telepot


class SteamFriendBot():

    def __init__(self, bot_api, steam_api, steam_ids, game_db, chat_id):
        self.bot_api = bot_api
        self.steam_api = steam_api
        self.steam_ids = steam_ids
        self.game_db = game_db
        self.chat_id = chat_id

        # Variables
        self.returned_game = None

        # Dictionaries for last game
        self.steam_lastgame = {}
        for i in range(0, len(steam_ids)):
            self.steam_lastgame[steam_ids[i]] = ''

    # Initialise Bot
    def init_bot(self):
        myBot = telepot.Bot(self.bot_api)
        return myBot

    def string_request(self, friends_link):
        requested_string = ('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s'
                            % (self.steam_api, self.steam_ids[friends_link]))
        return requested_string

    def game_check(self, friends_link):
        if self.returned_game != self.steam_lastgame[self.steam_ids[
                                friends_link]]:
            return True

    def update_game(self, friends_link):
        self.steam_lastgame[self.steam_ids[friends_link]] = self.returned_game

    def reset_game(self, friends_link):
        self.steam_lastgame[self.steam_ids[friends_link]] = ''

    def execute(self):
        myBot = self.init_bot()
        while True:
            for friends in range(0, len(self.steam_ids)):
                request_string = self.string_request(friends)
                try:
                    # Request username and appid from user profile
                    req = requests.get(request_string)
                    j = req.json()
                    returned_name = j['response']['players'][0]['personaname']
                    returned_id = j['response']['players'][0]['gameid']
                    # Look up game name via app id in steam db
                    req_name_from_id = requests.get(self.game_db)
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
                        message_to_send = ('%s is now playing %s' %
                                           (returned_name, returned_game))
                        print(message_to_send)
                        try:
                            myBot.sendMessage(self.chat_id, message_to_send)

                        # Revisit this. No time to capture error term,
                        # should've done on initial testing.

                        except:
                            print('Issue with myBot send message')
                            print('Wanted to send - %s' % message_to_send)
                            time.sleep(5)
                            myBot.sendMessage(self.chat_id, message_to_send)

                    # Revisit this. No time to capture error term,
                    # should've done on initial testing.
                    # This reset_game isn't being used, figure out why it
                    # works above and how this isn't required.

                except:
                    self.reset_game(friends)
                    print('%s is not playing anything' % (returned_name))

                time.sleep(5)
