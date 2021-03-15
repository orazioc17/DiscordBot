#Discord library, is asynchronous
import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.members = True

#This is the connection to discord
client = discord.Client(intents=intents)

sad_words = ["sad","unhappy","depressed","depressing","miserable"]

starter_encouragements = [
	"Cheer up!",
	"Hang in there",
	"You are a great person!"
]

commands = [
	"$new: Nueva frase inspiradora en la base de datos",
	"$inspire: Frase inspiradora de un autor",
	"$responding: con on y off puedes activar y desactivar los mensajes inspiradores auto-enviados",
	"$help: Mensaje de ayuda para usar el bot",
	"$del: Borra un mensaje inspirador de la base de datos",
	"$list: Muestra una lista de las frases inspiradoras en la base de datos"
]

new_user_message = """
Hi, welcome to this beautiful server
You can type $help to know how to use this bot
"""

if "responding" not in db.keys():
	db["responding"] = True

if db["encouragements"] not in db.keys():
	db["encouragements"] = starter_encouragements


def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote


def update_encouragements(encouraging_message):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(encouraging_message)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = encouraging_message


def delete_encouragement(index):
	encouragements = db["encouragements"]
	if len(encouragements) > index:
		del encouragements[index]
		db["encouragements"] = encouragements


#This is how i register an event, using decorators
@client.event
async def on_ready():
	#This is taking the client, the zero is replaced with the client, getting the username
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	msg = message.content

	#Doing this, this is like a command the bot will read and do something
	if message.content.startswith("$hello"):
		#So, everytime someone writes "$hello", the bot will answer "Hello!"
		await message.channel.send("Hello!")

	if msg.startswith("$help"):
		await message.channel.send("Hi, I am botXinxero, if you want to new the commands to use me, type $commands")

	if msg.startswith("$commands"):
		for command in commands:
			await message.channel.send(command)

	if message.content.startswith('$inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	if db["responding"]:	
		options = db["encouragements"]

		if any(word in msg for word in sad_words):
			await message.channel.send(random.choice(options))

	if msg.startswith("$new"):
		encouraging_message = msg.split("$new ", 1)[1]
		update_encouragements(encouraging_message)
		await message.channel.send("New encouraging message added")

	if msg.startswith("$del"):
		encouragements = []
		if "encouragements" in db.keys():
			index = int(msg.split("$del", 1)[1])
			delete_encouragement(index)
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)

	if msg.startswith("$list"):
		encouragements = []
		if "encouragements" in db.keys():
			encouragements = db["encouragements"]
			await message.channel.send(encouragements)

	if msg.startswith("$responding"):
		value = msg.split("$responding ", 1)[1]

		if value.lower() == "true":
			db["responding"] = True
			await message.channel.send("Responding is on.")
		else:
			db["responding"] = False
			await message.channel.send("Responding is off.")

@client.event
async def on_member_join(member):
	try:
		await client.send_message(member, new_user_message)
	except:
		embed = discord.Embed(
			title = 'Welcome ' + member.name+'!',
			description="We're so glad you're here!\nType $help to get more information about me",
      color=discord.Color.green()
		)
		await member.send(embed=embed)


keep_alive()
client.run(os.getenv('TOKEN'))