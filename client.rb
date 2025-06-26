require 'grpc'
require_relative 'tictactoe_pb'
require_relative 'tictactoe_services_pb'

def main
  # Conecta ao servidor gRPC
  stub = Tictactoe::TicTacToe::Stub.new('localhost:50051', :this_channel_is_insecure)

  # Fila para enviar requisições (jogadas) para o servidor
  requests = Enumerator.new do |yielder|
    # O primeiro envio é para se registrar. A posição -1 pode ser ignorada pelo servidor.
    puts "Conectando ao jogo..."
    yielder.yield Tictactoe::GameRequest.new(position: -1)

    loop do
      # Lê a entrada do usuário de forma não bloqueante
      move = $stdin.gets.chomp
      if move =~ /^\d+$/
        yielder.yield Tictactoe::GameRequest.new(position: move.to_i)
      end
    end
  end

  begin
    # Inicia o stream bidirecional
    responses = stub.game_stream(requests)
    player_id = -1
    symbol = ''

    # Thread para receber e processar mensagens do servidor
    responses.each do |res|
      # Determina o ID do jogador na primeira mensagem útil
      if player_id == -1 && res.board.include?('|')
        player_id = res.your_turn ? 0 : 1
        symbol = player_id == 0 ? 'X' : 'O'
        puts "Você é o jogador #{player_id} (#{symbol})."
      end

      # Limpa a tela e exibe o estado do jogo
      system('clear') || system('cls')
      puts "=== JOGO DA VELHA gRPC ==="
      puts res.board
      puts "\n"
      puts "Status: #{res.message}"

      if res.your_turn && !res.game_over
        print "Sua vez, digite a posição (0-8): "
      end

      if res.game_over
        puts "FIM DE JOGO!"
        break
      end
    end
  rescue GRPC::BadStatus => e
    puts "Erro de conexão: #{e.details}"
  end
  puts "Conexão encerrada."
end

main