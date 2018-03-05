import bot.steamfriends_discordbot as thebot
import your_details.lists_and_apis as details

steamTeleBot = thebot.SteamFriendBot(details.bot_api, details.steam_api,
                                     details.steam_friends, details.game_db,
                                     details.chat_id)

steamTeleBot.execute()
