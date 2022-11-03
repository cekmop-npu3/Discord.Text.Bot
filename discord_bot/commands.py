import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
import math


token = ''

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

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


@bot.group(invoke_without_command=True)
async def server(ctx):
    embed = discord.Embed(
        title=str(ctx.guild.name),
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(url=str(ctx.guild.icon))
    embed.add_field(name='Server id', value=str(ctx.guild.id), inline=False)
    embed.add_field(name='Creation date',
                    value=datetime.datetime.fromtimestamp(time.mktime(ctx.guild.created_at.timetuple())), inline=False)
    user = await ctx.bot.fetch_user(int(ctx.guild.owner_id))
    embed.add_field(name='Creator', value=str(user).split('#')[0], inline=False)
    embed.add_field(name='Members count', value=str(ctx.guild.member_count), inline=False)
    await ctx.send(embed=embed)


@server.command()
async def info_of(ctx, member: discord.Member):
    try:
        embed = discord.Embed(
            title=member,
            color=discord.Color.brand_green()
        )
        embed.set_thumbnail(url=str(member.avatar))
        embed.add_field(name='Joined at',
                        value=str(datetime.datetime.fromtimestamp(time.mktime(member.joined_at.timetuple()))),
                        inline=False)
        roles = [str(i) for i in member.roles if str(i) != '@everyone']
        if roles != []: embed.add_field(name='Roles', value=', '.join(roles), inline=False)
        lst = sorted(list(zip(dict(ref.get()).keys(), dict(ref.get()).values())), key=lambda x: x[1], reverse=True)
        embed.add_field(name='Stats',
                        value=f'Top: {[lst.index(i) + 1 for i in lst if str(member.id) in i[0]][0]}\nMessages: {dict(ref.get()).get(str(member.id))}',
                        inline=False)
        await ctx.send(embed=embed)
    except discord.ext.commands.errors.MemberNotFound:
        return


@server.command()
async def stats(ctx):
    embed = discord.Embed(
        title=str(ctx.guild.name),
        description=f'{sum(dict(ref.get()).values())} messages',
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(url=str(ctx.guild.icon))
    for key, value in dict(sorted(list(zip(dict(ref.get()).keys(), dict(ref.get()).values())), key=lambda x: x[1],
                                  reverse=True)).items():
        user = await ctx.bot.fetch_user(int(key))
        embed.add_field(name=str(user).split('#')[0], value=f'{value} messages', inline=False)
    await ctx.send(embed=embed)


@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title='Help',
        description='Use !help <command> for extended information',
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(
        url='https://4.bp.blogspot.com/-8oy1fb-s-Js/UBZR4LbEt8I/AAAAAAAABls/OM1YpMl0XjY/s1600/vraagteken.jpg')
    embed.add_field(name='Text commands', value='!help text', inline=False)
    embed.add_field(name='Music commands', value='!help music', inline=False)
    embed.add_field(name='Math commands', value='!help math_cmd', inline=False)
    await ctx.send(embed=embed)


@help.command()
async def text(ctx):
    embed = discord.Embed(
        title='Text',
        description='Available text commands',
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(
        url='https://4.bp.blogspot.com/-8oy1fb-s-Js/UBZR4LbEt8I/AAAAAAAABls/OM1YpMl0XjY/s1600/vraagteken.jpg')
    embed.add_field(name='Commands', value='!server\n!server stats\n!server info_of <nickname>\n!clear <msg_amount>', inline=False)
    await ctx.send(embed=embed)


@help.command()
async def music(ctx):
    embed = discord.Embed(
        title='Music',
        description='Available music commands\nMusic commands can only be written in appropriate channel',
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(
        url='https://4.bp.blogspot.com/-8oy1fb-s-Js/UBZR4LbEt8I/AAAAAAAABls/OM1YpMl0XjY/s1600/vraagteken.jpg')
    embed.add_field(name='Commands', value='None', inline=False)
    await ctx.send(embed=embed)


@help.command()
async def math_cmd(ctx):
    embed = discord.Embed(
        title='Math',
        description=f'All math commands are from python math library\nAll funcs are available on: https://docs.python.org/3/library/math.html\nFuncs must be written without <math.> prefix',
        color=discord.Color.brand_green()
    )
    embed.set_thumbnail(
        url='https://4.bp.blogspot.com/-8oy1fb-s-Js/UBZR4LbEt8I/AAAAAAAABls/OM1YpMl0XjY/s1600/vraagteken.jpg'
    )
    embed.add_field(name='Commands', value='!calc <func_name> <args>\n!calc_eval <math_problem>', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def calc(ctx, *arg):
    try:
        await ctx.send(getattr(math, arg[0])(*[float(i) for i in list(arg)[1:]]))
    except Exception:
        try:
            await ctx.send(getattr(math, arg[0])(*[int(i) for i in list(arg)[1:]]))
        except Exception:
            try:
                await ctx.send(getattr(math, arg[0])([float(i) for i in list(arg)[1:]]))
            except Exception:
                await ctx.send(getattr(math, arg[0])(range(*[int(i) for i in list(arg)[1:]])))


@bot.command()
async def calc_eval(ctx, arg):
    await ctx.send(eval(str(arg)))


bot.run(token)
