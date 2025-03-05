import serial
import numpy as np
import joblib

# 1. Carregar o modelo treinado e o label_encoder
modelo = joblib.load('random_forest_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# 2. Configuração da porta serial
ser = serial.Serial('COM12', 115200)  # Substitua 'COM12' pela porta correta
ser.flushInput()

# 3. Função para extrair características (igual ao código de treinamento)
def extrair_features(dados):
    return np.array([
        dados.mean(),  # Média
        dados.std(),   # Desvio padrão
        dados.max(),   # Valor máximo
        dados.min(),   # Valor mínimo
        np.percentile(dados, 25),  # Primeiro quartil
        np.percentile(dados, 75),  # Terceiro quartil
    ])

# 4. Função para prever o estado em tempo real e armazenar mudanças
def prever_estado_tempo_real():
    print("Iniciando previsão em tempo real...")
    print("Pressione Ctrl+C para parar.")

    # Variável para armazenar o último estado registrado
    ultimo_estado = None

    # Abrir arquivo para armazenar as mudanças de estado
    with open('mudancas_estado.txt', 'w') as arquivo:
        arquivo.write("Estado de Maquina:\n")  # Cabeçalho do arquivo

        try:
            # Buffer para armazenar as últimas 100 amostras
            buffer = []

            while True:
                # Lê uma linha da porta serial
                line = ser.readline().decode('utf-8').strip()

                # Verifica se a linha contém um valor numérico
                if line.replace(".", "").isdigit():  # Verifica se é um número válido
                    try:
                        magnitude = float(line)  # Converte para float

                        # Adiciona a magnitude ao buffer
                        buffer.append(magnitude)

                        # Quando o buffer tiver 100 amostras, faz a previsão
                        if len(buffer) == 200:
                            # Extrai as características das 100 amostras
                            features = extrair_features(np.array(buffer))

                            # Fazer a previsão
                            estado_previsto = modelo.predict([features])

                            # Mapear o estado previsto para o nome da condição
                            estado_nome = label_encoder.inverse_transform(estado_previsto)[0]

                            # Verifica se houve mudança de estado
                            if estado_nome != ultimo_estado:
                                # Atualiza o último estado registrado
                                ultimo_estado = estado_nome


                                # Exibe o resultado no terminal
                                print(f"Estado Previsto: {estado_nome}")
                                
                                # Armazena a mudança no arquivo
                                arquivo.write(f"Estado Previsto: {estado_nome}\n")
                                arquivo.flush()  # Força a gravação no arquivo

                            # Limpa o buffer para coletar novas amostras
                            buffer = []

                    except ValueError:
                        print(f"Erro ao converter valor: {line}")
                else:
                    print(f"Formato inesperado: {line}")

        except KeyboardInterrupt:
            print("Previsão em tempo real interrompida.")
        finally:
            ser.close()

# 5. Iniciar a previsão em tempo real
prever_estado_tempo_real()