from dis import disco
from http import client
from lib2to3.pgen2 import token
import os
from pydoc import cli
import discord
from discord.ext import commands
import sqlite3 as sl
from dotenv import load_dotenv
    
con = sl.connect('player.db')

client = commands.Bot(command_prefix="*")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')



def verify_tables():
    
    strQuery = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Players'"

    c = con.cursor()
			
    #get the count of tables with the name
    c.execute(strQuery)

    #if the count is 1, then table exists
    if c.fetchone()[0]==1 : {
        print('Table exists.')
    }
    else:
        create_table_players()
                
    #commit the changes to db			
    con.commit()

    strQuery = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Locations'"

    d = con.cursor()
			
    #get the count of tables with the name
    d.execute(strQuery)

    #if the count is 1, then table exists
    if d.fetchone()[0]==1 : {
        print('Table exists.')
    }
    else:
        create_table_locations()
                
    #commit the changes to db			
    con.commit()



def create_table_players():
    with con:
        con.execute("""
            CREATE TABLE Players (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                rating INTEGER
            );
        """)    
    

def create_table_locations():
    with con:
        con.execute("""
            CREATE TABLE Locations (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                warbandName TEXT,
                locationName TEXT
            );
        """)
    print('Table locations created.')


# VERIFY/CREATE WARBAND
@client.command(name = "verify", help = "Debug Program. No practical use")
async def verify(ctx):
    verify_tables()

# CREATE WARBAND
@client.command(name ='createWarband', help = 'input a warband name (no space) and a warband rating. Creates the warband in the database')
async def createWarband(ctx, playerName, playerRating):
    tup = [playerName, playerRating]
    sql = ''' INSERT INTO Players (name, rating)
              VALUES(?,?) '''
    cur = con.cursor()
    cur.execute(sql, tup)
    con.commit()

    await ctx.send('Warbands : ' + playerName + ' has been created with rating: ' + playerRating)


# LIST LOCATION
@client.command(name='listLocations', help = 'Lists the locations in alphabetical order of owning warbands')
async def listLocations(ctx):
    sql = ''' SELECT warbandName, locationName FROM Locations ORDER BY warbandName '''
    cur = con.cursor()
    cur.execute(sql)
    for locationName in cur.fetchall():
        await ctx.send(locationName)

# CHECKS LOCATION
@client.command(name='checkLocation', help = 'input a location name, and checks who currently owns that location')
async def checkLocation(ctx, locationName):
    tup = ['%' + locationName + '%']
    sql = ''' SELECT warbandName, locationName FROM Locations WHERE locationName like ? '''
    cur = con.cursor()
    cur.execute(sql, tup)
    for locationName in cur.fetchall():
        await ctx.send(locationName)

# UPDATES LOCATION
@client.command(name='updateLocation', help = 'input a location name (no space) and then a warband name. Updates the location to be owned by that warband')
async def updateLocation(ctx, locationName, warbandName):
    tup = [warbandName, locationName]
    sql = ''' UPDATE Locations SET warbandName = ? WHERE locationName = ? '''
    cur = con.cursor()
    cur.execute(sql, tup)
    for locationName in cur.fetchall():
        await ctx.send(locationName)

# UPDATES WARBAND RATING
@client.command(name='updateWarbandRating', help = 'input a warband name (no spaces) and a warband rating. Updates the warband to have that rating')
async def updateWarbandRating(ctx, playerName, playerRating):
    tup = [playerRating, playerName]
    sql = ''' UPDATE Players SET rating = ? WHERE name = ? '''
    cur = con.cursor()
    cur.execute(sql, tup)
    await ctx.send('Warbands : ' + playerName + ' has been updated to rating: ' + playerRating)   

# SELECT WARBANDS
@client.command(name='listWarbands', help= 'lists all warbands in order of descending rating')
async def listWarbands(ctx):
    sql = ''' SELECT name, rating FROM Players ORDER BY rating desc '''
    cur = con.cursor()
    cur.execute(sql)
    for name in cur.fetchall():
        await ctx.send(name)
    
# REMOVE WARBANDS
@client.command(name = 'removeWarband', help = 'input a warband name (no spaces). removes all warbands with that name')
async def removeWarband(ctx, playerName):
    tup = [playerName]
    sql = ''' DELETE FROM Players
              WHERE name = ? '''
    cur = con.cursor()
    cur.execute(sql, tup)
    con.commit()
    await ctx.send('Warbands : ' + playerName + ' has been removed')

client.run(TOKEN)