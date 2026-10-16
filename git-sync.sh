#!/bin/bash

# Exibe o status atual do repositório
echo "=== Verificando status do Git ==="
git status

# Pergunta se deseja continuar
read -p "Deseja continuar com o commit e push? (s/n): " resposta
if [[ "$resposta" != "s" && "$resposta" != "S" ]]; then
    echo "Operação cancelada."
    exit 0
fi

# Solicita a mensagem do commit ao usuário
echo -n "Digite a mensagem do commit: "
read mensagem_commit

# Se a mensagem estiver vazia, define uma padrão
if [ -z "$mensagem_commit" ]; then
    mensagem_commit="chore: atualizando laboratorios hlg"
fi

# Executa os comandos do Git
echo "=== Adicionando arquivos ==="
git add .

echo "=== Realizando commit ==="
git commit -m "$mensagem_commit"

echo "=== Enviando para o GitHub ==="
git push origin main

echo "=== Sincronização concluída com sucesso! ==="
