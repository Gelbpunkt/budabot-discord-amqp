# The Discord Bot token (https://discord.com/developers/applications)
token = ""
# The AMQP connection URI
amqp_uri = "amqp://broker:secret@127.0.0.1/"
# AMQP queue name and routing key
queue_name = "discord"
# AMQP exchange name
exchange_name = "budabot"
# The Discord channel ID to send to and read from
discord_channel_id = 1234567890
# Logfile path, set to None to have stdout
logfile = None
# The bot prefix
# used e.g. for !confirm code
prefix = "!"
# format for sending discord messages to AMQP
# valid format words:
# server: the name of the discord server
# channel: the name of the discord server
# nick: nickname of the message sender
# username: username of the message sender
# discrim: the 4-number discriminator of the  user
# content: message content
chat_format = "[#{server}/{channel}] {nick}: {content}"
# List of emojis to add with !createemojis
# Beware that Discord limits you to 50 total non-animated emojis
emojis = {
    "GFX_GUI_ICON_PROFESSION_1.png": "soldier",
    "GFX_GUI_ICON_PROFESSION_LARGE_1.png": "soldier_large",
    "GFX_GUI_ICON_PROFESSION_2.png": "ma",
    "GFX_GUI_ICON_PROFESSION_LARGE_2.png": "ma_large",
    "GFX_GUI_ICON_PROFESSION_3.png": "engi",
    "GFX_GUI_ICON_PROFESSION_LARGE_3.png": "engi_large",
    "GFX_GUI_ICON_PROFESSION_4.png": "fixer",
    "GFX_GUI_ICON_PROFESSION_LARGE_4.png": "fixer_large",
    "GFX_GUI_ICON_PROFESSION_5.png": "agent",
    "GFX_GUI_ICON_PROFESSION_LARGE_5.png": "agent_large",
    "GFX_GUI_ICON_PROFESSION_6.png": "advy",
    "GFX_GUI_ICON_PROFESSION_LARGE_6.png": "advy_large",
    "GFX_GUI_ICON_PROFESSION_7.png": "trader",
    "GFX_GUI_ICON_PROFESSION_LARGE_7.png": "trader_large",
    "GFX_GUI_ICON_PROFESSION_8.png": "crat",
    "GFX_GUI_ICON_PROFESSION_LARGE_8.png": "crat_large",
    "GFX_GUI_ICON_PROFESSION_9.png": "enfo",
    "GFX_GUI_ICON_PROFESSION_LARGE_9.png": "enfo_large",
    "GFX_GUI_ICON_PROFESSION_10.png": "doc",
    "GFX_GUI_ICON_PROFESSION_LARGE_10.png": "doc_large",
    "GFX_GUI_ICON_PROFESSION_11.png": "nt",
    "GFX_GUI_ICON_PROFESSION_LARGE_11.png": "nt_large",
    "GFX_GUI_ICON_PROFESSION_12.png": "mp",
    "GFX_GUI_ICON_PROFESSION_LARGE_12.png": "mp_large",
    "GFX_GUI_ICON_PROFESSION_14.png": "keeper",
    "GFX_GUI_ICON_PROFESSION_LARGE_14.png": "keeper_large",
    "GFX_GUI_ICON_PROFESSION_15.png": "shade",
    "GFX_GUI_ICON_PROFESSION_LARGE_15.png": "shade_large",
}
