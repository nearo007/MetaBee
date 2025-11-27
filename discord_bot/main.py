import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import aiohttp
import urllib.parse  # ADICIONADO: Para tratar espaços na URL
from discord.errors import LoginFailure

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("DISCORD_TOKEN não encontrado no .env")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ============================
# BOT ONLINE
# ============================
@bot.event
async def on_ready():
    # Nota: O sync global pode demorar para aparecer, em produção prefira syncar por Guild se for urgente
    await bot.tree.sync()
    print(f"{bot.user.name} is online!")

# ============================
# EVENTO DE MENSAGEM
# ============================
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "metabee" in message.content.lower():
        await message.channel.send(f"{message.author.mention} fala cupinxa")

    await bot.process_commands(message)

# ============================
# HELP
# ============================
@bot.command(name="help", help="Mostra todos os comandos disponíveis.")
async def help_command(context):
    help_lines = []

    for command in bot.commands:
        if command.hidden:
            continue
        
        name = f"!{command.name}"
        desc = command.help or "Sem descrição."
        help_lines.append(f"**{name}** — {desc}")

    final_msg = f"Comandos disponíveis {context.author.mention}:\n\n"
    final_msg += "\n".join(help_lines)

    await context.send(final_msg)

# ============================
# STATUS POR ID
# ============================
@bot.command(help="Mostra o status de uma impressora pelo ID.")
async def impressora_status_id(context, device_id):
    # IDs geralmente não tem espaço, mas se tiverem, trate com urllib também
    safe_id = urllib.parse.quote(str(device_id))
    url = f"http://127.0.0.1:8000/api/get_printer_status_id/{safe_id}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                nome = data.get("name", "Campo não encontrado")
                state = data.get("state", "Campo não encontrado")
                await context.send(f"{context.author.mention}\nNome: {nome}\nEstado: {state}")
            else:
                await context.send(f"{context.author.mention} Erro ao acessar a API: {response.status}")


# ============================
# STATUS POR NOME (ATUALIZADO)
# ============================
@bot.command(help="Mostra o status de uma impressora pelo nome (Aceita espaços).")
async def impressora_status_name(context, *, printer_name): # O asterisco permite espaços
    
    # Transforma "HP Laserjet" em "HP%20Laserjet" para a URL não quebrar
    safe_name = urllib.parse.quote(printer_name)
    
    url = f"http://127.0.0.1:8000/api/get_printer_status_name/{safe_name}"
    
    async with aiohttp.ClientSession() as session:
        # Bloco try/except adicionado para capturar erros de conexão (ex: API desligada)
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    nome = data.get("name", "Campo não encontrado")
                    state = data.get("state", "Campo não encontrado")
                    await context.send(f"{context.author.mention}\nNome: {nome}\nEstado: {state}")
                elif response.status == 404:
                     await context.send(f"{context.author.mention} Impressora '{printer_name}' não encontrada.")
                else:
                    await context.send(f"{context.author.mention} Erro na API: {response.status}")
        except Exception as e:
            await context.send(f"{context.author.mention} Erro de conexão: {str(e)}")


# ============================
# TODAS IMPRESSORAS
# ============================
@bot.command(help="Lista o status de todas as impressoras.")
async def todas_impressoras(context):
    url = f"http://127.0.0.1:8000/api/all_printer_status"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    printers = data.get("printer_id", []) # Adicionado valor padrão [] se a chave não existir

                    if not printers:
                         await context.send(f"{context.author.mention} Nenhuma impressora encontrada.")
                         return

                    full_string = f"{context.author.mention}\n"
                    
                    state = printer.get('state', 'N/A')
                    if state == 0:
                        state = 'Desligado'
                    elif state == 1:
                        state = 'Ligado'
                    elif state == 2:
                        state = 'Operando'
                
                    for printer in printers:
                        full_string += f"**Nome:** {printer.get('name', 'N/A')} | **Estado:** {state}\n"

                    # O Discord tem limite de 2000 caracteres por mensagem. 
                    # Se tiver muitas impressoras, pode cortar.
                    if len(full_string) > 2000:
                        full_string = full_string[:1900] + "\n... (lista muito longa)"

                    await context.send(full_string)
                else:
                    await context.send(f"{context.author.mention} Erro ao acessar a API: {response.status}")
        except Exception as e:
            await context.send(f"{context.author.mention} Erro de conexão: {str(e)}")

# ============================
# RUN
# ============================
if __name__ == '__main__':
    try:
        bot.run(token, log_handler=handler, log_level=logging.DEBUG)
    
    except LoginFailure:
        print('Erro: Credenciais Incorretas, verifique o token.')