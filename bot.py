# This code for a bot that runs on the popular chatting application Discord
# This is the second iteration of the bot as it originally was done in JavaScript
# This file has code for the bot to login and what to do when a message is received.
# Author: George Cepeda
# Created: 1/15/2020
# For more information on the bot email me at CepedaGeorgeA@gmail.com

#imports
import discord
import sqlite3
from sqlite3 import Error
#import botfunctions as bf

#Other Section
TOKEN = 'Your token here'
client = discord.Client()
#End of Other Section

#Custom Functions
#added in v2.1
#parses the message given and checks for a command. 
async def order(message):
    msg = message.content.split(); #Split gives a list of words.
    cmd = msg[0]                   # 0 should be the first element which should be the actually command for the bot to use.
    #Python has no Switch statements so later on try to implement a dictionary for each function call
    
    if cmd == '!intro':
        await introduction(message)
    
    if cmd == '!latest':
        await newest_messages(message)

#added in v2.1
#sends a simple introduction message with a link to it's github repo
async def introduction(message):
    hiIam = "Hello, I am Beth 2.1, a bot created for fun on discord. This iteration has new features and improved operation. For more info on me checkout my Github repo at <https://github.com/GeorgeCepeda/CustomDiscordBot.git>".format(message)
    await message.channel.send(hiIam)

#added in v2.1
#Adds a message to the database
async def addToDB(conn, message):
    #create the object to be added
    addThis = (message.id, message.author.name, message.content, 0) #id, author, message itself, rating default to 0
    
    #create the sql command
    sql = ''' INSERT INTO messages(MessageId,Author,Message,Rating)
              VALUES(?,?,?,?)'''

    #Actually adding to DB
    cur = conn.cursor()
    cur.execute(sql,addThis)
    conn.commit() #This should save the newly added row.
    #print(cur.lastrowid) #Shows us the rowid of our newly added row. Mainly for testing purposes

#added in v2.1
#Gets the 3 newest messages saved in the db
async def newest_messages(message):
    conn = create_connection(r"discordlog.db")
    if conn is not None:
        query = "SELECT * FROM messages ORDER BY id DESC LIMIT 3"
        
        curr = conn.cursor()
        curr.execute(query)
        rows = curr.fetchall()

        msg = "Last 3 messages sent in this server\n"
        for row in rows:
            mId = row[1]
            writer = row[2]
            content = row[3]
            rowMsg = "Message Id: " + str(mId) + ", Author: " + writer + ", Message: " + content + "\n"
            msg += rowMsg
        
        msg.format(message)
        await message.channel.send(msg)
    else:
        print("Could not connect for latest messages")
    
#End of Custom Functions

#SQLite functions
"""
These SQL functions are in reference to sqlitetutorial.net tutorials. 
"""
#added in v2.1
#Create tables based on sql_statement
def create_table(conn, sql_statement):
    #conn = connection object
    #sql_statement is a CREATE TABLE Statement
    try:
        c = conn.cursor()
        c.execute(sql_statement)
    except Error as e:
        print(e)

#added in v2.1
#creates a connection to a database specified in db_file
def create_connection(db_file):
    #Create db conncection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file) 
        #print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

#End of SQLite Functions

#Discord Functions 
@client.event
async def on_message(message):
    #this keeps it from replying to itself.
    if message.author == client.user:
        return

    #sends message to be parsed
    await order(message)
    
    conn = create_connection(r"discordlog.db")
    if conn is not None:
        await addToDB(conn,message)
    else:
        print("Could not add message to database")
    
    conn.close()

    

#Gives confirmation on commandline the bot has successfully booted.
@client.event
async def on_ready():
    #Bot info
    print('-------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('now running in python')
    print('-------------')
    
    #SQLite stuff
    conn = create_connection(r"discordlog.db")
    cTable = """CREATE TABLE IF NOT EXISTS messages (
        id integer PRIMARY KEY, MessageId integer, Author text, Message text, Rating integer
        );"""

    if conn is not None:
        create_table(conn,cTable)
    else:
        print("Error cannot connect to DB")
    
    conn.close()

#Actually starts the bot
client.run(TOKEN)
#End of Discord Functions

"""
Version History
v1.0 - Original JavaScript version of bot. released: 2018
v2.0 - Bot remade in python based from previous JavaScript version. released: December 2019
V2.1 - Added SQLite database features. released: January 15, 2020
"""

