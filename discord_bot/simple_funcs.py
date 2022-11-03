import discord

token = 'MTAyODYwOTYzNzU4MDI3OTgzOA.GKeNrb.ZbIATbErMXLm9vv7UZNM7bSWVdUc4HjQ8RKegs'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    try:
        if str(message.content).lower().startswith('!clear'):
            def get_roles(member: discord.Member):
                return [str(i).lower() for i in member.roles if str(i) != '@everyone']
            if 'супер-админ' in get_roles(message.author) or 'админ' in get_roles(message.author):
                await message.channel.purge(limit=int(message.content.split(' ')[1]))
        if message.channel.name == 'системные-сообщения' and str(message.type) == 'MessageType.new_member':
            await message.add_reaction('✅')
            await message.reply(f'Hello, {str(message.author).split("#")[0]} :wave:')
        if str(message.channel.name) == 'nsfw' and str(message.content) != '':
            await message.channel.purge(limit=1)
        if str(message.channel.name) == 'музыка' and str(message.content) == '':
            await message.channel.purge(limit=1)
    except Exception:
        pass


client.run(token)
