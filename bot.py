import os

import discord

from dotenv import load_dotenv

from pysnmp import hlapi

from discord.ext import commands

import snmp

import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SHA_PASSWORD = os.getenv('SHA_PASSWORD')
AES_PASSWORD = os.getenv('AES_PASSWORD')
SNMP_USER = os.getenv('SNMP_USER')

bot = commands.Bot(command_prefix="$")
#client = discord.Client()

@bot.command()
async def snmpget(ctx, *args):
	order = args[0]
	if(order == 'sysName'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.2.1.1.5.0'],hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
	elif(order == 'sysLocation'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.2.1.1.6'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
	elif(order == 'sysDescr'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.2.1.1.1'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
	elif(order == 'cpuLoad'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.4.1.2021.10.1.3.3'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
	elif(order == 'ramFree'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.4.1.2021.4.11.0'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
	elif(order == 'freeDiskSpace'):
		await ctx.channel.send(snmp.get('127.0.0.1',['1.3.6.1.4.1.2021.9.1.7.1'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)))
    
@bot.command()
async def snmpGetBulk(ctx, *args):
	order = args[0]
	max_mibs = int(args[1])
	
	if(order == 'memory'):
		await ctx.channel.send(snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.4'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),max_mibs))
	elif(order == 'disk'):
		await ctx.channel.send(snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.9.1'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),max_mibs))
	elif(order == 'cpuTimes'):
		await ctx.channel.send(snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.11'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),max_mibs))
	elif(order == 'network'):
		await ctx.channel.send(snmp.getBulk('127.0.0.1', ['1.3.6.1.2.1.2.2'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),max_mibs))

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
@bot.command()
async def GR(ctx,*args):
    order = args [0]
    client = MongoClient('localhost',27017)
    db = client.grs
    find = db.metric.find()

    if order == "Memory":
        xList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        yList = []#Obtener los 15 valores de memoria
        print(find)
        for i in xList:
        	yList.append(find[i].mem)
			
        x = np.array(xList)
        y = np.array(yList)

        plt.plot(x,y)
        ##plt.title(f'{order}'s Graph')
        plt.savefig(fname='plot')
        await ctx.send(file = discord.File('plot.png'))
        os.remove('plot.png')
        plt.clf()

    elif order == "CPU":

        xList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        yList = []#Obtener los 15 valores de memoria
        for i in xList:
            yList.append(find[i].cpu)

        x = np.array(xList)
        y = np.array(yList)

        plt.plot(x,y)
        ##plt.title(f'{order}'s Graph')
        plt.savefig(fname='plot')

        await ctx.send(file = discord.File('plot.png'))
        os.remove('plot.png')
        plt.clf()

"""@client.event
async def on_message(message):
    if message.author == client.user:
        return
    response = ''
    if message.content == '!sysName':
    	response = snmp.get('127.0.0.1', ['1.3.6.1.2.1.1.5.0'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    elif message.content == '!sysLocation':
        response = snmp.get('127.0.0.1',['1.3.6.1.2.1.1.6'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    elif message.content == '!sysDescr':
        response = snmp.get('127.0.0.1',['1.3.6.1.2.1.1.1'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    elif message.content == '!diskStatistics':
    	response = snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.9.1'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),7)
    elif message.content == '!memoryStatistics':
        response = snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.4'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),8)
    elif message.content == '!cpuTimes':
        response = snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2021.11'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),7)
    
    await message.channel.send(response)"""


bot.run(TOKEN)
