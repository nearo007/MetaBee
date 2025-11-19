import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import aiohttp
from discord.errors import LoginFailure

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("DISCORD_TOKEN não encontrado no .env")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    GUILD_ID = 1235268950418260179
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync()
    print(f"{bot.user.name} is online!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "metabee" in message.content.lower():
        await message.channel.send(f"{message.author.mention} fala cupinxa")

    await bot.process_commands(message) # continuar a verificar os eventos padrões

@bot.command()
async def ajuda(context):
    comandos = ["!help", "!impressora_status_id + ID_DA_IMPRESSORA", "impressora_status_name + NOME_DA_IMPRESSORA"]
    
    response_string = ""
    
    for i in range(0, len(comandos)):
        response_string += f"\n\n{i+1} - {comandos[i]}"
        
    await context.send(f"Precisa de ajuda? {context.author.mention}!{response_string}")

@bot.command()
async def soma(context, n1: float, n2: float):
    soma = n1 + n2
    await context.send(f"{context.author.mention} {n1:g} + {n2:g} = {soma:g}")

@bot.tree.command(name="help", description="list commands")
async def hello(interaction: discord.Interaction):
    comandos = ["!help", "!impressora_status_id + ID_DA_IMPRESSORA", "impressora_status_name + NOME_DA_IMPRESSORA"]
    
    response_string = ""
    
    for i in range(0, len(comandos)):
        response_string += f"\n\n{i+1} - {comandos[i]}"
    await interaction.response.send_message(f"Precisa de ajuda? {interaction.user.mention}!{response_string}")

@bot.command()
async def impressora_status_id(context, device_id):
    url = f"http://127.0.0.1:8000/api/get_printer_status_id/{device_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()  # se a API retornar JSON
                # exemplo: pegar um campo específico
                nome = data.get("name", "Campo não encontrado")
                state = data.get("state", "Campo não encontrado")
                await context.send(f"{context.author.mention}\nNome: {nome}\nEstado: {state}")
            else:
                await context.send(f"{context.author.mention} Erro ao acessar a API: {response.status}")

@bot.command()
async def impressora_status_name(context, printer_name):
    url = f"http://127.0.0.1:8000/api/get_printer_status_name/{printer_name}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()  # se a API retornar JSON
                # exemplo: pegar um campo específico
                nome = data.get("name", "Campo não encontrado")
                state = data.get("state", "Campo não encontrado")
                await context.send(f"{context.author.mention}\nNome: {nome}\nEstado: {state}")
            else:
                await context.send(f"{context.author.mention} Erro ao acessar a API: {response.status}")

@bot.command()
async def todas_impressoras(context):
    url = f"http://127.0.0.1:8000/api/all_printer_status"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()  # se a API retornar JSON
                printers = data.get("printer_id")

                full_string = f"{context.author.mention}"
                
                for printer in printers:
                    full_string += f"\nNome: {printer.name}\nEstado: {printer.state}"

                await context.send(full_string)
            else:
                await context.send(f"{context.author.mention} Erro ao acessar a API: {response.status}")     

if __name__ == '__main__':
    try:
        bot.run(token, log_handler=handler, log_level=logging.DEBUG)
    
    except LoginFailure:
        print('Erro: Credenciais Incorretas, verifique o token.')