
# DiscorBotYT

DiscorBotYT es un bot de Discord diseñado para reproducir música directamente desde YouTube en tu servidor de Discord. Es capaz de administrar una cola de canciones y proporcionar controles básicos de reproducción como pausa, resumir, detener, y saltar canciones.

## Características

- Reproduce música desde YouTube.
- Administra una cola de reproducción.
- Controles de reproducción: pausa, resumir, detener, y saltar a la siguiente canción.

## Requisitos

- Python
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/DiscorBotYT.git
    cd DiscorBotYT
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno:
    - Crea un archivo `.env` en el directorio raíz.
    - Añade tu token de Discord en el archivo `.env` con la siguiente estructura:
    ```env
    discord_token=TU_DISCORD_TOKEN
    ```

## Uso

Para ejecutar el bot, simplemente corre el siguiente comando:

```bash
python main.py
```

El bot se conectará a tu servidor de Discord y estará listo para reproducir música.

## Comandos

- `!play <URL o búsqueda>`: Reproduce una canción desde YouTube o añade la canción a la cola si ya hay una en reproducción.
- `!pause`: Pausa la reproducción actual.
- `!resume`: Reanuda la reproducción si está pausada.
- `!stop`: Detiene la reproducción y desconecta el bot del canal de voz.
- `!next`: Salta a la siguiente canción en la cola.
- `!queue`: Muestra la lista de canciones en la cola.

## Contribuciones

Las contribuciones son bienvenidas. Puedes abrir un issue o enviar un pull request.

