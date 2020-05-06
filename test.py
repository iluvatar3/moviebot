# Weinermans Magical Movie Spin Wheel

# do some importing
import discord
import pymysql
import configparser

# maybe some from imports
from discord.ext import commands
from datetime import datetime

# load config
config = configparser.ConfigParser()
config.read('../moviebot.ini')

# set db values
dbhost = config['db']['host']
dbuser = config['db']['user']
dbpass = config['db']['pass']
dbname = config['db']['name']

# setup some config
date = datetime.today().strftime('%Y-%m-%d')
time = datetime.today().strftime('%H:%M:%S')

# setup the bot
description = 'Weinerman\'s Magical Movie Spin Wheel'
bot = commands.Bot(command_prefix='-', description=description)


# remove the default bot command
bot.remove_command('help')

# on ready message will just print out to cli
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# submit commmand
@bot.command()
async def submit(ctx, movie: str):
    # submits the movie into the system
    userid = ctx.message.author.id
    username = ctx.message.author.name
    displayname = ctx.message.author.display_name

    # movie is stored as a string
    try:
        # do the connection
        connection = pymysql.connect(dbhost, dbuser, dbpass, dbname)

    except pymysql.ProgrammingError:
        # some sort of programming error
        await ctx.send("Failed to connect to database [ProgrammingError")
        raise RuntimeError("Create a group of connection parameters under the heading [ProgrammingError]")

    except pymysql.Error:
        # cant connect to db
        await ctx.send("Failed to connect to database [Error]")
        raise RuntimeError("Failed to connect to database [Error]")


    # add the submission
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO movie_suggestions SET username = %s, displayname = %s, user_id = %s, movie = %s, submit_date = %s, submit_time = %s"
            cursor.execute(sql, (username, displayname, userid, movie, date, time))

        # save changes
        connection.commit()

        # send back success
        await ctx.send(displayname+' successfully submitted "'+movie+'"')

    except pymysql.ProgrammingError as e:
        # some sort of programming error
        await ctx.send("Failed to submit movie, try again later [ProgrammingError: "+format(e)+"]")
        raise RuntimeError("Failed to submit movie, try again later [ProgrammingError: "+format(e)+"]")

    except pymysql.Error as e:
        # failed to insert
        await ctx.send("Failed to submit movie, try again later [Error: "+format(e)+"]")
        raise RuntimeError("Failed to submit movie, try again later [Error: "+format(e)+"]")

    except Exception as e:
       # generic error
       await ctx.send("Failed to submit movie, try again later [Exception: "+format(e)+"]")
       raise RuntimeError("Failed to submit movie, try again later [Exception: "+format(e)+"]")

    finally:
        # connection done
        connection.close()


# list command
@bot.command()
async def list(ctx):
    # gets the list of current movies
    movielist = ''

    # connect to db
    try:
        # do the connection
        connection = pymysql.connect(dbhost, dbuser, dbpass, dbname)

    except pymysql.ProgrammingError:
        # some sort of programming error
        await ctx.send("Failed to connect to database [ProgrammingError")
        raise RuntimeError("Create a group of connection parameters under the heading [ProgrammingError]")

    except pymysql.Error:
        # cant connect to db
        await ctx.send("Failed to connect to database [Error]")
        raise RuntimeError("Failed to connect to database [Error]")

    # get the current week
    startdate = ''
    enddate = ''

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM week_list WHERE start_date <= %s AND end_date >= %s LIMIT 1"
            cursor.execute(sql, (date, date))
            result = cursor.fetchone()

            if result is not None:
                startdate = result['start_date']
                enddate = result['end_date']

    except pymysql.ProgrammingError as e:
        # some sort of programming error
        await ctx.send("Failed to retrieve current submissions, try again later [ProgrammingError: "+format(e)+"]")
        raise RuntimeError("Failed to retrieve current submissions, try again later [ProgrammingError: "+format(e)+"]")

    except pymysql.Error as e:
        # failed to insert
        await ctx.send("Failed to retrieve current submissions, try again later [Error: "+format(e)+"]")
        raise RuntimeError("Failed to retrieve current submissions, try again later [Error: "+format(e)+"]")

    except Exception as e:
       # generic error
       await ctx.send("Failed to retrieve current submissions, try again later [Exception: "+format(e)+"]")
       raise RuntimeError("Failed to retrieve current submissions, try again later [Exception: "+format(e)+"]")


    # connection done
    connection.close()

    await ctx.send("Searching for submissions between "+startdate+" and "+enddate)




# help command
@bot.command()
async def help(ctx):
    # just display this string to show the commands
    result = '__Sorry you\'re having a hard time with this simple bot, here are the commands__\n' \
             +'**-submit "Movie Name"** To add a movie to the currently weekly submissions, only your most recent submission is used\n' \
             +'**-list** Simply prints out all the current movie suggestions\n' \
             +'**-winner** Shows the current winner, updates after 1pm on Tuesdays'
    await ctx.send(result)


# run the bot
bot.run('NzA3MjYxODkzNDEyMTI2ODEx.XrHPyg.vjHS6VhOnRY9X-9CYwsFWVJqgQY')