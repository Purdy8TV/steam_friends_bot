import bot.steamfriends_discordbot as thebot
import your_details.lists_and_apis as details

steamTeleBot = thebot.steamFriendbotapi(details.botapi, details.steamapi, 
                                        details.steam_friends, details.gamedb, 
                                        details.chatid)

steamTeleBot.execute()
