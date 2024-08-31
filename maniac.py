# Importar librerías necesarias
import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
import urllib.parse, urllib.request, re

# Función para ejecutar el bot
def run_bot():
    # Cargar variables de entorno
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    
    # Configurar intenciones del bot
    intents = discord.Intents.default()
    intents.message_content = True
    
    # Crear cliente del bot
    client = commands.Bot(command_prefix=".", intents=intents)

    # Inicializar colas y clientes de voz
    queues = {}
    voice_clients = {}
    
    # Configurar URLs de YouTube
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    
    # Configurar opciones de yt_dlp
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    # Configurar opciones de FFmpeg
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    
    # Evento cuando el bot está listo
    @client.event
    async def on_ready():
        print(f'{client.user} es el DJ ahora')

    # Función para reproducir la siguiente canción en la cola
    async def play_next(ctx):
        if queues[ctx.guild.id]:
            link = queues[ctx.guild.id][0]
            await play(ctx, link=link)
    
    # Comando para reproducir una canción
    @client.command(name="play")
    async def play(ctx, *, link):
        try:
            # Conectarse al canal de voz del usuario
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            # Si la URL no es de YouTube, buscar la canción en YouTube
            if youtube_base_url not in link:
                query_string = urllib.parse.urlencode({
                    'search_query': link
                })

                content = urllib.request.urlopen(
                    youtube_results_url + query_string
                )

                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

                link = youtube_watch_url + search_results[0]

            # Extraer información de la canción con yt_dlp
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            # Reproducir la canción y agregar la función para reproducir la siguiente canción
            voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))
            queues[ctx.guild.id].pop(0)
        except Exception as e:
            print(e)

    # Comando para limpiar la cola
    @client.command(name="limpiar_cola")
    async def clear_queue(ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()
            await ctx.send("¡Cola vaciada!")
        else:
            await ctx.send("No hay cola para vaciar")

    # Comando para pausar la reproducción
    @client.command(name="pausa")
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    # Comando para reanudar la reproducción
    @client.command(name="reanudar")
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    # Comando para detener la reproducción y desconectar del canal de voz
    @client.command(name="stop")
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    # Comando para saltar a la siguiente canción
    @client.command(name="next")
    async def next(ctx):
        try:
            if ctx.guild.id in voice_clients and voice_clients[ctx.guild.id].is_playing():
                if queues[ctx.guild.id]:
                    voice_clients[ctx.guild.id].stop()
                    await play_next(ctx)
                    await ctx.send("Saltando a la siguiente canción.")
                else:
                    await ctx.send("No hay canciones en la cola para saltar.")
            else:
                await ctx.send("No hay una canción reproduciéndose.")
        except Exception as e:
            print(e)

    # Comando para mostrar la cola de reproducción
    @client.command(name="cola")
    async def queue(ctx, *, url=None):
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        
        if url:
            queues[ctx.guild.id].append(url)
            await ctx.send("¡Agregado a la cola!")

        if queues[ctx.guild.id]:
            queue_list = "\n".join([f"{index + 1}. {song}" for index, song in enumerate(queues[ctx.guild.id])])
            await ctx.send(f"Canciones en cola:\n{queue_list}")
        else:
            await ctx.send("La cola está vacía.")

    # Ejecutar el bot con el token de Discord
    client.run(TOKEN)