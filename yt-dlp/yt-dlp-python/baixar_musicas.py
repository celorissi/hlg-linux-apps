import os
import yt_dlp

def baixar_playlist_para_pasta(url_playlist, pasta_destino):
    # Garante que o diretório de destino existe
    os.makedirs(pasta_destino, exist_ok=True)
    
    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
        'ignoreerrors': True, # Ignora vídeos removidos/privados para não parar os 800 downloads
    }
    
    print(f"Iniciando o download e conversão exclusiva para MP3 em: {pasta_destino}")
    print("Isso pode demorar bastante tempo devido ao tamanho da playlist. Pode deixar a correr.")
    
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url_playlist])
        
    print("Processo finalizado! Apenas os ficheiros MP3 foram guardados.")

if __name__ == '__main__':
    # O seu diretório escolhido no Raspberry Pi
    DIRETORIO_SAIDA = '/home/marcelo/laboratorios/yt-dlp/downloads-youtube/musicas-ylp'
    
    # Pede o link diretamente no terminal na hora de executar
    link_playlist = input("Insira o link da playlist do YouTube: ").strip()
    
    if link_playlist:
        baixar_playlist_para_pasta(link_playlist, DIRETORIO_SAIDA)
    else:
        print("Nenhum link foi inserido. O programa foi encerrado.")