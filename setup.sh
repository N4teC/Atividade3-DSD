#!/bin/bash

echo "🚀 Configurando ambiente para o Jogo da Velha gRPC..."

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# Instalar dependências Ruby
echo "💎 Instalando dependências Ruby..."
bundle install

# Compilar arquivos .proto
echo "🔨 Compilando arquivos .proto..."
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tictactoe.proto
grpc_tools_ruby_protoc -I. --ruby_out=. --grpc_out=. tictactoe.proto

echo "✅ Ambiente configurado com sucesso!"
echo "📋 Para jogar:"
echo "   1. Execute: python server.py"
echo "   2. Em outro terminal: python client.py (ou ruby client.rb)"
echo "   3. Em outro terminal: python client.py (ou ruby client.rb)"
