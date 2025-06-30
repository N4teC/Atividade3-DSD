#!/bin/bash

echo "🚀 Configurando ambiente de desenvolvimento..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt-get update -y

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install grpcio grpcio-tools protobuf
fi

# Instalar dependências Ruby
echo "💎 Instalando dependências Ruby..."
if [ -f "Gemfile" ]; then
    gem install bundler
    bundle install
else
    gem install grpc grpc-tools
fi

# Instalar outras dependências úteis
echo "🔧 Instalando ferramentas adicionais..."
sudo apt-get install -y tree htop curl wget git

# Verificar instalações
echo "✅ Verificando instalações..."
python3 --version
ruby --version
pip show grpcio
gem list grpc

echo "🎉 Ambiente configurado com sucesso!"
echo "📝 Pronto para desenvolver o jogo distribuído!"