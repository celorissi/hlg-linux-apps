# 🧪 HLG Linux Apps & Labs

Este repositório contém scripts, automações, testes e laboratórios focados em aplicações e serviços executados em ambientes Linux / Docker (Raspberry Pi e servidores local/homologação).

O objetivo principal é manter um ambiente flexível e versionado para testes rápidos de automação, manipulação de mídias, APIs e infraestrutura de suporte.

---

## 🛠️ Estrutura do Repositório

```text
hlg-linux-apps/
├── terminaltube-docker/       # Aplicação em Docker para gestão/reprodução de mídias
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── app.py
├── yt-dlp/                    # Automações e scripts Python utilizando yt-dlp
│   ├── app.py
│   ├── requirements.txt
│   └── yt-dlp-python/         # Scripts para download e organização de álbuns/músicas
├── .gitignore                 # Filtros para ignorar venv, logs e arquivos temporários
├── git-sync.sh                # Script de automação para commit/push rápido
└── README.md                  # Documentação do repositório

🚀 Como Utilizar os Laboratórios
1. Pré-requisitos
Certifique-se de ter os seguintes componentes instalados no ambiente:

Git

Python 3.x e pip

Docker e Docker Compose

2. Clonando o Repositório
Bash
git clone [https://github.com/celorissi/hlg-linux-apps.git](https://github.com/celorissi/hlg-linux-apps.git)
cd hlg-linux-apps
3. Configurando Ambientes Python (venv)
Para executar os scripts da pasta yt-dlp sem poluir o sistema operacional:

Bash
cd yt-dlp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🔄 Automação do Git (git-sync.sh)
Para agilizar o fluxo de testes e garantir que as alterações sejam enviadas para o GitHub ao finalizar uma sessão de trabalho, utilize o script git-sync.sh:

Garanta permissão de execução (apenas na primeira vez):

Bash
chmod +x git-sync.sh
Execute o script de sincronização:

Bash
./git-sync.sh
O script fará a checagem do status, solicitará a mensagem de commit e enviará as atualizações automaticamente para o GitHub, respeitando as exclusões do .gitignore.

⚠️ Regras e Boas Práticas (Git)
Não suba ambientes virtuais (venv) ou dependências locais.

Mantenha chaves de API, senhas ou tokens fora dos arquivos do repositório.

Atualize o requirements.txt sempre que adicionar bibliotecas novas ao projeto.


---

### Como salvar no seu repositório:

Execute os comandos a seguir no terminal do seu Raspberry Pi para criar o arquivo e enviar ao GitHub usando o script que criamos:

```bash
cd ~/laboratorios/hlg-linux-apps
cat << 'EOF' > README.md
# 🧪 HLG Linux Apps & Labs

Este repositório contém scripts, automações, testes e laboratórios focados em aplicações e serviços executados em ambientes Linux / Docker (Raspberry Pi e servidores local/homologação).

O objetivo principal é manter um ambiente flexível e versionado para testes rápidos de automação, manipulação de mídias, APIs e infraestrutura de suporte.

---

## 🛠️ Estrutura do Repositório

```text
hlg-linux-apps/
├── terminaltube-docker/       # Aplicação em Docker para gestão/reprodução de mídias
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── app.py
├── yt-dlp/                    # Automações e scripts Python utilizando yt-dlp
│   ├── app.py
│   ├── requirements.txt
│   └── yt-dlp-python/         # Scripts para download e organização de álbuns/músicas
├── .gitignore                 # Filtros para ignorar venv, logs e arquivos temporários
├── git-sync.sh                # Script de automação para commit/push rápido
└── README.md                  # Documentação do repositório
🚀 Como Utilizar os Laboratórios
1. Pré-requisitos
Certifique-se de ter os seguintes componentes instalados no ambiente:

Git

Python 3.x e pip

Docker e Docker Compose

2. Clonando o Repositório
Bash
git clone [https://github.com/celorissi/hlg-linux-apps.git](https://github.com/celorissi/hlg-linux-apps.git)
cd hlg-linux-apps
3. Configurando Ambientes Python (venv)
Para executar os scripts da pasta yt-dlp sem poluir o sistema operacional:

Bash
cd yt-dlp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🔄 Automação do Git (git-sync.sh)
Para agilizar o fluxo de testes e garantir que as alterações sejam enviadas para o GitHub ao finalizar uma sessão de trabalho, utilize o script git-sync.sh:

Garanta permissão de execução (apenas na primeira vez):

Bash
chmod +x git-sync.sh
Execute o script de sincronização:

Bash
./git-sync.sh
O script fará a checagem do status, solicitará a mensagem de commit e enviará as atualizações automaticamente para o GitHub, respeitando as exclusões do .gitignore.

⚠️ Regras e Boas Práticas (Git)
Não suba ambientes virtuais (venv) ou dependências locais.

Mantenha chaves de API, senhas ou tokens fora dos arquivos do repositório.

Atualize o requirements.txt sempre que adicionar bibliotecas novas ao projeto.
EOF

Enviar a documentação usando o script recém-criado
./git-sync.sh