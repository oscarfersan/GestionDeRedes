import os

import discord

from dotenv import load_dotenv

from pysnmp import hlapi

import snmp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SHA_PASSWORD = os.getenv('SHA_PASSWORD')
AES_PASSWORD = os.getenv('AES_PASSWORD')
SNMP_USER = os.getenv('SNMP_USER')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    response = ''
    if message.content == '!sysName':
    	response = snmp.get('127.0.0.1', ['1.3.6.1.2.1.1.5.0'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    
    if message.content == '!sensors':
    	response = snmp.getBulk('127.0.0.1', ['1.3.6.1.4.1.2620.1.6.7.8'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol),5)
    
    if message.content == '!diskUsed':
    	response = snmp.get('127.0.0.1', ['1.3.6.1.4.1.2021.9.1.9'], hlapi.UsmUserData(SNMP_USER, authKey=SHA_PASSWORD, privKey=AES_PASSWORD, authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol))
    await message.channel.send(response)
        


client.run(TOKEN)
