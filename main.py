import sys
import discord
from discord import Client
import asyncio
from itertools import cycle
from datetime import datetime, date


client: Client = discord.Client()
emoji = '\N{THUMBS UP SIGN}'
helpfile = open('system/help.txt', 'r').read()
owner = open('system/owner.txt', 'r').read().split('\n')
admincommands = open('system/adminCommands.txt', 'r').read().split('\n')
ownercommands = open('system/ownerCommands.txt', 'r').read().split('\n')
alb = open('system/audit_log_base.html', 'r').read()
selectedserver = 0
selectedserver2 = 0
annoy = False


try:
	token = open('system/token.txt', 'r').read()
except:
	token = ''
selectedserver = [0, 0]

if token == '' or token == 'Token here':
    print('No token given')
    print('Read README.md')
    while True:
        pass


async def save_audit_logs(guild):
    result = ''
    f = open(f'audit_logs_{guild.name}.html', 'w+')
    # f.write('{0.user} did {0.action} to {0.target}\n'.format(entry))
    result += '<tr style=""><td>{0.user}</td><td>{0.action}</td><td>{0.target}</td></tr>'.format(entry)
    result = alb.format(content=result)
    print(result)
    f.write(result)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='$help'))
    client.user.verified = True
    print(time() + f"Connected as {client.user}")


@client.event
async def on_message(message):
    con: str = message.content
    channel = message.channel
    author = message.author
    args = con.split(' ')
    arg = args[0].lower()
    send = channel.send
    global selectedserver
    global selectedserver2
    global annoy

    #await message.add_reaction('<:turret:787923805917675530>')

    if arg.startswith('$'):
        print(time() + f'Message: {str(author)}, {message.guild.name}, {channel}, {con}')

    if arg in admincommands and not hasadmin(message):
        if not str(author) in owner:
            await send('`No permission....`')
            return

    if arg in ownercommands and not str(author) in owner:
        await send('`No permission....`')
        return

    if con.startswith('$') and str(author) in open('system/mute.txt', 'r').read().split('\n'):
        await send('You\'re bot-muted')
        return

    if channel.id == selectedserver2 and str(author) != 'Antosser-Bot#4884' and arg.startswith('$owdo'):
        channel2 = channel
        channel = client.get_channel(selectedserver)
        send = channel.send
        try:
            if args[1] == 'a':
                await eval(' '.join(args[2:]))
            else:
                eval(' '.join(args[1:]))
        except Exception as ex:
            await channel2.send(ex)
        return

    if annoy and str(author) != 'Antosser-Bot#4884':
        await send(con)

    if channel.id == selectedserver and str(author) != 'Antosser-Bot#4884':
        await client.get_channel(selectedserver2).send(str(author) + ':\n' + con + '\n-')

    if channel.id == selectedserver2 and str(author) != 'Antosser-Bot#4884':
        await client.get_channel(selectedserver).send(con)
        return

    if arg == '$userattributes':
        result = "```"
        for att in dir(message.author):
            result += f'{att}\n'
        result += '```'
        await send(result)

    if arg == '$help':
        await send(helpfile)

    if arg == "$logoutbot":
        await send('Logging out...')
        await sys.exit()

    if arg == '$say':
        await send(con[4:])

    if arg == '$repeat' and len(args) >= 3:
        for i in range(int(args[1])):
            new_msg = await send(' '.join(args[2:]))
        await new_msg.add_reaction(emoji)

    if arg == '$getfile' and len(args) == 2:
        if '/' not in con and '\\' not in con:
            send("No permission...")
        else:
            try:
                await send(file=discord.File(con.split(' ')[1]))
            except Exception as i:
                print(i)

    if arg == '$owner':
        await send(f'{owner}')

    if arg == '$admin':
        admin = False
        result = '```Your roles:'
        for roleIndex in range(len(author.roles) - 1):
            result += f'\nRole {author.roles[roleIndex]} has administrator: {author.roles[roleIndex].permissions.administrator}'
            if author.roles[roleIndex].permissions.administrator:
                admin = True
        result += '\n---------------'
        result += f'\nYou have admin: {admin}```'
        await send(result)

    if arg == '$testbot':
        await send('I\'m working')

    if arg == '$user' and len(args) == 3:
        if args[1] == 'me':
            args[1] == author.id
        try:
            await eval(f"send(client.get_user(int(args[1])).{args[2]})")
        except Exception as ex:
            await send(ex)

    if arg == '$owdo':
        try:
            if args[1] == 'a':
                await eval(' '.join(args[2:]))
            else:
                eval(' '.join(args[1:]))
        except Exception as ex:
            await send(ex)

    if arg == '$ca':
        await channel.purge(limit=1000)

    if arg == '$cl' and len(args) == 2:
        await channel.purge(limit=int(args[1]) + 1)

    if con == '$get':
        await send(channel.purge(limit=1)[0].content)

    if arg == 'calc':
        try:
            await send(eval(' '.join(args[1:])))
        except Exception as ex:
            await send(ex)

    if arg == '$audit':
        await save_audit_logs(message.channel.guild)
        try:
            await send(file=discord.File(f'audit_logs_{channel.guild.name}.html'))
        except:
            await send('File does not exist')

    if arg == '$yeet':
        await send('Yeet')

    if arg == '$botmute' and len(args) == 3:
        with open('system/mute.txt', 'r').read().split('\n') as mute:
            if args[1] == 'add':
                if str(author) in mute:
                    await send('User is already bot-muted')
                else:
                    pass
            elif args[1] == 'rem':
                pass
            else:
                await send('Invalid parameter')

    if arg == '$react':
        await message.add_reaction(emoji)

    if arg == '$here':
        selectedserver = channel.id
        print('ss1 ' + str(selectedserver))
        await message.delete()

    if arg == '$serverid':
        await send(message.guild)

    if arg == '$ownercommand':
        pass

    if arg == '$ss' and len(args) > 1:
        await client.get_channel(selectedserver).send(' '.join(args[1:]))

    if arg == '$here2':
        selectedserver2 = channel.id
        print('ss2 ' + str(selectedserver2))

    if arg == '$annoy':
        if annoy:
            annoy = False
        else:
            annoy = True

    if arg == '?c100':
        await send('https://cdn.discordapp.com/attachments/773199816564932628/791430300823584768/9k.png')

    if arg == '?mem':
        await send('https://cdn.discordapp.com/attachments/773167713568030761/791217190228852756/1NPWT5vcLqA2.jpg')

'''async def inputmethod():
    while True:
        command = await input('Hi: ')
        cmdargs = command.split(' ')
        cmdarg = cmdargs[0]

        print(command, cmdargs, cmdarg)
        if cmdarg == 'send':
            await selectedserver[3].send(cmdargs[1])'''


def hasadmin(message):
    admin = False
    for roleIndex in range(len(message.author.roles) - 1):
        if message.author.roles[roleIndex].permissions.administrator:
            admin = True
    return admin


def time():
    return str(datetime.now()) + '   '


try:
    client.run(token)
except:
    print('Incorrect token or connection error')
    while True:
        pass
