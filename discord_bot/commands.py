import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import time
import math


token = 'MTAyODYwOTYzNzU4MDI3OTgzOA.GKeNrb.ZbIATbErMXLm9vv7UZNM7bSWVdUc4HjQ8RKegs'

cert = {
    "type": "service_account",
    "project_id": "discord-af6ab",
    "private_key_id": "893aead184363c40735540ffb2bf40441a0998e2",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDAQn94FKC8tYkU\nne6KBnNezIM6Czvi6SOE3NsKV5AwX/S9IoYzuxpspTVSMv4jrwIpFLxMpra20JI1\n3KLIUgGt+JyRJ3yiL90zyNtAy53HkUgOmPvTIlcFlEQ+ZcmcOl1d0AgDHn6d0Cnj\n/KhU6Uz+7iYD39gTGOwKx9HG2hzJicMYEv8N8dgPHhOkeWnRdwY4PP1ULe6APen6\nSb8USvWLXZZA871p6DOsw5QpAOtaZT/fXmmKQKlhiw5NMj+//MQzY25qE4VrEMI6\nDvTxQW1wk0Q+ve6dd9ko7Ex6x7BOLofjowYXtJ3NIyRu0OuqaOr2XGXo/BD8fp7j\nX/BD2iZZAgMBAAECggEAKrG5r9dY2H8xuUfXFISZMyiUTZv4CQw/zH3lEHdgeDWe\n2i9kAPHgTNclL6NOR2tSPgAyTo1JDvDjPx3Hclevssv+LMfJiBS7+Qd2FP4ChDJR\nf5hed8Ts8Tq7KuYcrtpRKIeNd+/aKz5yRwQw92Y1qHkHLR4U1CzZIg28mn2OHfzc\nsKZpvXcEum+QTjMLAAsBN7nX4g5h0CNkJ53X+SXoO5PRL4ZYpZs6yCkY/a+a+8AS\nEGST+03XcMLOJnEH/yZJT3v8RaAauHX78aRYUOpHL2U7X+n0qxSce6El+xaW4D/7\nE5SnS0yTfW0iB67hOSeKnbjNwyoBjk/8I/xS4B9tGQKBgQDhCT8C4yjNokiIm3It\n+G3q/PqsTZCtlzkoVJZG1a8GELfR/JsGBTYNoL4UGS+22d9/l3NTlSJ4MwFNehz4\nnWic76pbdONHhnTHQDKKBQmAszC43ajW2rs0jtja0ixSQEsBu1jRU0TUi3EuVm9f\nFif+eR94yplMyaLVdQpUDy2hBQKBgQDatrmyw9wvMInSULGVT3ZEWn1P9qD8KIZP\n+pL6mO/wnSrk3VHcqL77kYHjHcy+M4LlXKMbzK5XD4WqQHuMfYY0epcw0LeaAxky\nyaiY868SGTUl47yzRE+JyAB4jwMHCbsvDt4tfFzhXTIE7VSYdfMgRTSh+T9+eVnQ\nKyhllsLARQKBgQCqs2nR1eCQw8ZDoa6mAmnWs9mutBPIKgsYdbmct+DROANITVaG\n5ZMQGVu2QTi5emGYFplL0LfZ987IJ5YsXLMLQJ24TF1PV0XkEuWDXrjLoKGXycSW\nXktdXfJPYtht+AktoiCIgKKYm8HaBYTr2xGxbc2awgwxfE6BnwubofvZxQKBgEe+\njOfBK+cm6u7cnYQ3DrqZXGXwpxpQSM7PiYs+w+aQB9QPbZ0Olad8MblIuzLhPtzy\nKGckG0RfyR7yDBUnz/BDDnlq3e9deNSaJf4WYaV0M2T8cZf0noq52r2xW/LhFE/5\ndpRBKU6b/Z50I73nYxuA2CUR1+wq7nVE0vmQHM5pAoGBAJFl807Q4sibE+HgpRuE\n/aaws3Lqi7KCVpjkdLz1TeXdoiNq+PEAOy2f43o7QAwQQiBm77fdMyS6/sCeY2PY\nHEHvgxhKSvmLRA5GvGGsbgKpWWSOYezsE8Tut+3qI+vA6CtZ85qbhUtrraLf/1PZ\n/W19Elgn+5Tp0iOQe3deJRRn\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-djn2n@discord-af6ab.iam.gserviceaccount.com",
    "client_id": "116530960922195711850",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-djn2n%40discord-af6ab.iam.gserviceaccount.com"
}
cred = credentials.Certificate(cert)
url_link = 'https://discord-af6ab-default-rtdb.europe-west1.firebasedatabase.app'
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
