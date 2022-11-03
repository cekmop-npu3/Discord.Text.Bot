import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

token = 'token'

cert = {
    'cert'
}
cred = credentials.Certificate(cert)
url_link = 'link'
url2 = {'databaseURL': url_link}
firebase_admin.initialize_app(cred, url2)
ref = db.reference(f"/discord")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    def get_id(member: discord.Member):
        return member.id

    if str(get_id(message.author)) in dict(ref.get()).keys():
        ref.update({
            get_id(message.author): dict(ref.get()).get(str(get_id(message.author))) + 1
        })
    else:
        ref.update({
            get_id(message.author): 1
        })


client.run(token)
