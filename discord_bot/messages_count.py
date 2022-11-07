import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import datetime

token = 'token'

cert = {
    'cert'
}
cred = credentials.Certificate(cert)
url_link = 'link'
url2 = {'databaseURL': url_link}
firebase_admin.initialize_app(cred, url2)
ref = db.reference(f"/Discord/Users/")
ref_del = db.reference(f"/Discord/DeletedMessages/")
ref_edit = db.reference(f"/Discord/EditedMessages/")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message_delete(message):
    ref_del.update({
        str(int(time.time())): {
            'Message': message.content, 'Author': str(message.author).split("#")[0],
            'Time': str(datetime.datetime.now()), 'Channel': message.channel.name
        }
    })


@client.event
async def on_message_edit(before, after):
    ref_edit.update({
        str(int(time.time())): {
            'MessageBefore': before.content,
            'MessageAfter': after.content,
            'Author': str(after.author).split("#")[0],
            'Time': str(datetime.datetime.now()),
            'Channel': after.channel.name
        }
    })



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
