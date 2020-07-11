# The Discord Bot token (https://discord.com/developers/applications)
token = ""
# The AMQP connection URI
amqp_uri = "amqp://broker:secret@127.0.0.1/"
# AMQP queue name and routing key
queue_name = "discord"
# The AMQP exchange
amqp_exchange = "budabot"
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
