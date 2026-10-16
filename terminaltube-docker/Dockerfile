FROM python:3.11-slim

# Instalar dependências do sistema (incluindo ffmpeg para processamento de media)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho dentro do contentor
WORKDIR /app

# Instalar bibliotecas Python necessárias (incluindo o suporte a formulários multipart)
RUN pip install --no-cache-dir fastapi uvicorn yt-dlp python-multipart

# Copiar o código da aplicação para o contentor
COPY app.py /app/app.py

# Criar a estrutura de pastas de media dentro do contentor
RUN mkdir -p /app/media/audio/musicas /app/media/audio/albuns /app/media/video/mp4

# Expor a porta padrão da aplicação
EXPOSE 8000

# Comando para iniciar o servidor FastAPI (corrigido para 'app:app')
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]