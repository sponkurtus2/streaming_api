from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

app.config['VIMEO_CLIENT_ID'] = '3d938927cba6e7b871d8c318c27f996b40c77564'
app.config[
    'VIMEO_CLIENT_SECRET'] = '0kD4yQovAn2xrf20sYZNkrjclTAFeLOdUJrEDO7pGIS6uL32fRepay3SB4Iv7+RrYNTdJL9WmdnqupM3qanRcqD+B3nh4xunNNrws4X4eEAYNr83me+H2VzeHL/CDjnG'


@app.route('/')
def reproducir_video():
    video_id = '871122886'
    access_token = '05abe224de75c8a4252292059a37b93c'

    # Realiza una solicitud GET para obtener información del video
    url = f'https://api.vimeo.com/videos/{video_id}'
    # headers -> almacena datos de la solicitud, que seran utilizados para la informacion
    headers = {
        # Authorization verifica que la api y su token sean validos
        'Authorization': f'Bearer {access_token}',
        # Se indica el tipo de dato que se espera aceptar
        'Accept': 'application/vnd.vimeo.*+json;version=3.4',
    }

    # Todos los datos anteriores, se almacenan en una respuesta
    response = requests.get(url, headers=headers)

    # Y verificamos si el resultado de la respuesta es valido, o no.
    if response.status_code == 200:
        # La variable de video_info es la que almacena el json que recibimos de la respuesta anterior
        video_info = response.json()

        # Todos los valores de abajo, son obtenidos del JSON
        titulo = video_info['name']
        likes = video_info['metadata']['connections']['likes']['total']
        duracion = video_info['duration']
        propietario = video_info['user']['name']
        descripcion = video_info['description']

        # En caso de que la descripcion sea muy grande, la recortamos.
        if len(descripcion) > 100:
            descripcion = descripcion[:100] + '...'

        # Indicamos que la pagina se cargara en index.hml, y pasamos como parametros los datos que usaremos del video, titulo, etc.
        return render_template('index.html', titulo=titulo, likes=likes, duracion=duracion,
                               propietario=propietario, descripcion=descripcion, video_id=video_id)
    else:
        return 'Error al obtener información del video de Vimeo'


if __name__ == '__main__':
    app.run(debug=True)