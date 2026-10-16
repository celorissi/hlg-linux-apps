# Portal Web FastAPI & yt-dlp no Raspberry Pi

Documentação técnica do projeto de automação para download, divisão e gestão de ficheiros de áudio do YouTube (playlists e álbuns por capítulos) num ambiente Raspberry Pi.

---

## 1. Visão Geral da Arquitetura
O sistema consiste numa aplicação web leve desenvolvida em **FastAPI** que corre de forma autónoma num **Raspberry Pi**, gerindo o motor de extração **`yt-dlp`** e **FFmpeg**. Os ficheiros são organizados numa pasta centralizada e partilhados na rede local via **Samba**, permitindo o acesso e gestão direta tanto via browser como por partilha de rede.

* **Ambiente de Execução:** Raspberry Pi OS / Python 3 (`venv`)
* **Framework Web:** FastAPI + Uvicorn
* **Motor de Extração:** `yt-dlp` & FFmpeg
* **Diretório Raiz Centralizado:** `/home/marcelo/laboratorios/yt-dlp/downloads-youtube`
* **Subdiretórios:**
  * `musicas-ylp/` (Playlists e músicas individuais)
  * `albuns-separados/` (Álbuns completos divididos por capítulos)

---

## 2. Decisões Técnicas e Desafios Superados
1. **Numeração Sequencial e Limpa:** 
   * Utilização de templates de saída com `% (autonumber)02d. %(title)s.%(ext)s` para garantir nomes legíveis, seguros e ordenados (`01. Nome.mp3`, `02. Nome.mp3`).
   * Eliminação completa de erros de metadados (`NA`) garantindo consistência no formato de saída.
2. **Gestão de Pastas Planas:**
   * Manutenção de todos os ficheiros MP3 diretamente na raiz das respetivas pastas principais (`musicas-ylp` e `albuns-separados`), sem subpastas individuais por álbum, facilitando drasticamente a visualização em tabelas HTML e a limpeza de ficheiros.
3. **Interface Web Intuitiva:**
   * Tabelas com índices enumerados (`1.`, `2.`, ...), indicação de tamanho em MB, botões individuais de exclusão (`[Apagar]`) e botões de limpeza em massa por diretório.

---

## 3. Código Completo da Aplicação (`app.py`)

```python
from fastapi import FastAPI, BackgroundTasks, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import glob
import yt_dlp

app = FastAPI()

DIRETORIO_RAIZ_YOUTUBE = '/home/marcelo/laboratorios/yt-dlp/downloads-youtube'
DIRETORIO_PLAYLIST = os.path.join(DIRETORIO_RAIZ_YOUTUBE, 'musicas-ylp')
DIRETORIO_ALBUNS = os.path.join(DIRETORIO_RAIZ_YOUTUBE, 'albuns-separados')

def executar_download(url: str, modo: str):
    if modo == "album":
        pasta_destino = DIRETORIO_ALBUNS
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
            'outtmpl': os.path.join(pasta_destino, '%(autonumber)02d. %(title)s.%(ext)s'),
            'ignoreerrors': True,
        }
    else:
        pasta_destino = DIRETORIO_PLAYLIST
        opcoes = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(pasta_destino, '%(autonumber)02d. %(title)s.%(ext)s'),
            'ignoreerrors': True,
        }

    os.makedirs(pasta_destino, exist_ok=True)
    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print(f"Download concluído ([Modo: {modo}]) para: {url}")
    except Exception as e:
        print(f"Erro no download: {e}")

@app.get("/", response_class=HTMLResponse)
def home():
    os.makedirs(DIRETORIO_PLAYLIST, exist_ok=True)
    os.makedirs(DIRETORIO_ALBUNS, exist_ok=True)
    
    musicas_playlist = glob.glob(os.path.join(DIRETORIO_PLAYLIST, "*.mp3"))
    musicas_albuns = glob.glob(os.path.join(DIRETORIO_ALBUNS, "*.mp3"))

    def gerar_tabela(lista):
        if not lista:
            return "<tr><td colspan='4' style='text-align: center; color: #777;'>Pasta vazia.</td></tr>"
        
        html = ""
        for i, f in enumerate(sorted(lista), start=1):
            nome = os.path.basename(f)
            tamanho = os.path.getsize(f) / (1024 * 1024)
            html += f"""
                <tr>
                    <td style="width: 40px; color: #1db954; font-weight: bold;">{i}.</td>
                    <td>{nome}</td>
                    <td style="color: #888; text-align: right; width: 80px;">{tamanho:.1f} MB</td>
                    <td style="text-align: right; width: 70px;">
                        <a href="/apagar?caminho={f}" style="color: #ff5555; text-decoration: none; font-weight: bold;">[Apagar]</a>
                    </td>
                </tr>
            """
        return html

    tabela_playlist = gerar_tabela(musicas_playlist)
    tabela_albuns = gerar_tabela(musicas_albuns)

    return f"""
    <html>
        <head>
            <title>YT-DLP Raspberry Pi Portal</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; background: #121212; color: #fff; display: flex; justify-content: center; align-items: flex-start; min-height: 100vh; margin: 0; padding: 30px; box-sizing: border-box; }}
                .container {{ width: 800px; display: flex; flex-direction: column; gap: 20px; }}
                .card {{ background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.6); }}
                h2, h3 {{ margin-top: 0; color: #1db954; text-align: center; }}
                h3 {{ text-align: left; font-size: 16px; color: #fff; }}
                input[type="text"], select {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #444; background: #2b2b2b; color: #fff; border-radius: 6px; box-sizing: border-box; font-size: 14px; }}
                select {{ cursor: pointer; }}
                button {{ background: #1db954; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; font-size: 16px; transition: background 0.3s; margin-top: 10px; }}
                button:hover {{ background: #1aa34a; }}
                .danger-btn {{ background: #d9534f !important; margin: 0; }}
                .danger-btn:hover {{ background: #c9302c !important; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
                th, td {{ padding: 8px; border-bottom: 1px solid #333; text-align: left; }}
                .file-list {{ max-height: 200px; overflow-y: auto; display: block; }}
                table {{ display: table; width: 100%; }}
                .section-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h2>YouTube to MP3 Portal</h2>
                    <form action="/baixar" method="post">
                        <input type="text" name="url" placeholder="Cole o link do YouTube..." required autocomplete="off">
                        <select name="modo">
                            <option value="playlist">Playlist / Músicas Individuais (musicas-ylp)</option>
                            <option value="album">Álbum Completo com Capítulos (albuns-separados)</option>
                        </select>
                        <button type="submit">Iniciar Download</button>
                    </form>
                </div>

                <div class="card">
                    <div class="section-header">
                        <h3 style="margin:0;">Pasta: Playlists / Músicas ({len(musicas_playlist)})</h3>
                        {f'<form action="/limpar-pasta" method="post" style="margin:0;"><input type="hidden" name="pasta" value="playlist"><button type="submit" class="danger-btn" style="padding: 5px 10px; font-size: 12px; width: auto;">Limpar Esta Pasta</button></form>' if musicas_playlist else ''}
                    </div>
                    <div class="file-list">
                        <table>{tabela_playlist}</table>
                    </div>
                </div>

                <div class="card">
                    <div class="section-header">
                        <h3 style="margin:0;">Pasta: Álbuns Separados ({len(musicas_albuns)})</h3>
                        {f'<form action="/limpar-pasta" method="post" style="margin:0;"><input type="hidden" name="pasta" value="album"><button type="submit" class="danger-btn" style="padding: 5px 10px; font-size: 12px; width: auto;">Limpar Esta Pasta</button></form>' if musicas_albuns else ''}
                    </div>
                    <div class="file-list">
                        <table>{tabela_albuns}</table>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/baixar", response_class=HTMLResponse)
def iniciar_download(background_tasks: BackgroundTasks, url: str = Form(...), modo: str = Form(...)):
    background_tasks.add_task(executar_download, url, modo)
    return """
    <html>
        <head><meta charset="utf-8"><style>body{font-family:Arial;background:#121212;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;text-align:center;}.card{background:#1e1e1e;padding:40px;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.6);}h2{color:#1db954;}a{display:inline-block;margin-top:20px;background:#333;color:white;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;}</style></head>
        <body><div class="card"><h2>Download Iniciado!</h2><p>O Raspberry Pi está a processar o seu pedido.</p><a href="/">Voltar ao Portal</a></div></body>
    </html>
    """

@app.get("/apagar")
def apagar_ficheiro(caminho: str):
    if caminho.startswith(DIRETORIO_RAIZ_YOUTUBE):
        if os.path.exists(caminho) and caminho.endswith(".mp3"):
            os.remove(caminho)
    return RedirectResponse(url="/", status_code=303)

@app.post("/limpar-pasta")
def limpar_pasta(pasta: str = Form(...)):
    diretorio_alvo = DIRETORIO_PLAYLIST if pasta == "playlist" else DIRETORIO_ALBUNS
    for f in glob.glob(os.path.join(diretorio_alvo, "*.mp3")):
        os.remove(f)
    return RedirectResponse(url="/", status_code=303)
```

---

## 4. Configuração como Serviço de Sistema (Systemd)

Para garantir a execução contínua e automática no arranque do Raspberry Pi, criou-se o serviço em `/etc/systemd/system/yt-portal.service`:

```ini
[Unit]
Description=Portal FastAPI YouTube to MP3 (yt-dlp)
After=network.target

[Service]
User=marcelo
WorkingDirectory=/home/marcelo/laboratorios/yt-dlp
ExecStart=/home/marcelo/laboratorios/yt-dlp/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Comandos de gestão do serviço:**
```bash
sudo systemctl stop yt-portal.service
sudo systemctl daemon-reload
sudo systemctl enable yt-portal.service
sudo systemctl start yt-portal.service
sudo systemctl status yt-portal.service

sudo systemctl restart yt-portal.service
```

---

## 5. Partilha de Rede (Samba)

Configuração adicionada ao ficheiro `/etc/samba/smb.conf` para expor a pasta centralizada na rede local:

```ini
[Downloads-YouTube]
   comment = Portal de Downloads YouTube (Álbuns e Playlists)
   path = /home/marcelo/laboratorios/yt-dlp/downloads-youtube
   browseable = yes
   writeable = yes
   create mask = 0775
   directory mask = 0775
   public = no
```
*(Reiniciar serviço Samba com: `sudo systemctl restart smbd`)*


sudo systemctl stop yt-portal.service
sudo pkill -9 -f "uvicorn app:app"
sudo ss -lptn 'sport = :8000'