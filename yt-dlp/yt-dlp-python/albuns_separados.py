import os
import yt_dlp

def baixar_album_com_capitulos(url: str):
    # Diretório base onde os álbuns serão guardados
    diretorio_base = '/home/marcelo/laboratorios/yt-dlp/downloads-youtube/albuns-separados'

    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        'split_chapters': True,
        # Cria uma subpasta com o nome do vídeo/álbum e enumera as faixas lá dentro
        'outtmpl': os.path.join(diretorio_base, '%(title)s', '%(autonumber)02d. %(title)s.%(ext)s'),
        'ignoreerrors': True,
    }

    print(f"A descarregar e a dividir capítulos para: {url}")
    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print("Download, criação da pasta e adição das músicas concluídos com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro durante o processo: {e}")

if __name__ == "__main__":
    url_alvo = input("Cole o link do YouTube (álbum/vídeo com capítulos): ")
    baixar_album_com_capitulos(url_alvo)