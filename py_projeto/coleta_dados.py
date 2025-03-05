import serial
import csv
import os
import time

# Configuração da porta serial
ser = serial.Serial('COM12', 115200)  # Substitua 'COM12' pela porta correta
ser.flushInput()

# Função para coletar dados e salvar em um arquivo CSV
def coletar_dados(nome_arquivo):
    # Caminho completo para o arquivo CSV
    caminho_completo = os.path.join("py_projeto", nome_arquivo + ".csv")

    # Abre o arquivo CSV para escrita
    with open(caminho_completo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Magnitude"])  # Cabeçalho do CSV

        print(f"Coleta de dados iniciada. Os dados serão salvos em: {caminho_completo}")
        print("A coleta começará em 5 segundos...")

        # Contagem regressiva de 5 segundos
        for i in range(5, 0, -1):
            print(f"Iniciando em {i}...")
            time.sleep(1)

        print("Coleta iniciada!")

        try:
            contador = 0
            while contador < 5000:  # Limite de 5000 medições
                # Lê uma linha da porta serial
                line = ser.readline().decode('utf-8').strip()
                
                # Verifica se a linha contém um valor numérico
                if line.replace(".", "").isdigit():  # Verifica se é um número válido
                    try:
                        magnitude = float(line)  # Converte para float
                        
                        # Escreve a magnitude no arquivo CSV
                        writer.writerow([magnitude])
                        file.flush()  # Força a gravação dos dados no arquivo
                        
                        contador += 1
                        print(f"Medição {contador}/5000: Magnitude = {magnitude}")
                    except ValueError:
                        print(f"Erro ao converter valor: {line}")
                else:
                    print(f"Formato inesperado: {line}")

            print("Coleta concluída! 5000 medições realizadas.")

        except KeyboardInterrupt:
            print("Coleta de dados interrompida pelo usuário.")
        finally:
            print(f"Dados salvos em: {caminho_completo}")

# Loop principal para coletar dados em diferentes configurações
try:
    while True:
        # Pergunta o nome do arquivo
        nome_arquivo = input("Digite o nome do arquivo para salvar os dados (ou 'sair' para encerrar): ").strip()
        
        # Verifica se o usuário quer sair
        if nome_arquivo.lower() == "sair":
            print("Encerrando o programa.")
            break

        # Coleta os dados e salva no arquivo
        coletar_dados(nome_arquivo)

except Exception as e:
    print(f"Erro durante a execução: {e}")
finally:
    ser.close()