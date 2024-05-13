import os
import shutil
import argparse

def copiar(origem, destino, arquivo):
    """
    Copia o arquivo para o destino.

    Parâmetros:
        origem (str): O caminho para a pasta de origem.
        destino (str): O caminho para a pasta de destino.
        arquivo: arquivo a ser copiado.
    
    Retorna:
        None
    """

    # Cria o caminho completo para o arquivo de origem
    origem_arquivo = os.path.join(origem, arquivo)
    # Cria o caminho completo para o arquivo de destino
    destino_arquivo = os.path.join(destino, arquivo)
    # Copia o arquivo para o destino
    shutil.copy2(origem_arquivo, destino_arquivo)

def copiar_arquivos(origem, destino):
    """
    Copia todos os arquivos de uma pasta de origem para uma pasta de destino.

    Parâmetros:
        origem (str): O caminho para a pasta de origem.
        destino (str): O caminho para a pasta de destino.
    """

    # Criando os caminhos da origem:
    train = origem + "/train"
    valid = origem + "/valid"
    test = origem + "/test"

    # Criando uma lista de caminhos:
    caminhos = [train, valid, test]

    # Criando os caminhos dos diretórios:
    anotacoes = destino+"/root/Annotations"
    imagens = destino+"/root/JPEGImages"

    # Criando os caminhos dos txts:
    trainval_nomes = destino+'/root/ImageSets/Main/trainval.txt'
    teste_nomes = destino+'/root/ImageSets/Main/test.txt'

    for caminho in caminhos:
        # Itera sobre os arquivos na pasta de origem
        for arquivo in os.listdir(caminho):
            # Verifica o tipo de arquivo:
            if arquivo.endswith(".jpg"):
                nome_arquivo = os.path.splitext(arquivo)[0]
                if (caminho == caminhos[0] or caminho == caminhos[1]):
                    escrever_em_txt(trainval_nomes, nome_arquivo)
                else:
                    escrever_em_txt(teste_nomes, nome_arquivo)
                copiar(caminho, imagens, arquivo)
            elif arquivo.endswith(".xml"):
                copiar(caminho, anotacoes, arquivo)

def criar_pastas(nomes_pastas, dir_base='.'):
    """
    Cria pastas no diretório especificado.

    Parâmetros:
        nomes_pastas (list): Lista de nomes das pastas a serem criadas.
        dir_base (str, opcional): Diretório base onde as pastas serão criadas. O padrão é o diretório atual.
    
    Retorna:
        None
    """
    for nome_pasta in nomes_pastas:
        caminho_pasta = os.path.join(dir_base, nome_pasta)
        try:
            os.makedirs(caminho_pasta)
            print(f"Pasta '{nome_pasta}' criada em '{caminho_pasta}'")
        except FileExistsError:
            print(f"A pasta '{nome_pasta}' já existe em '{caminho_pasta}'")
        except Exception as e:
            print(f"Falha ao criar a pasta '{nome_pasta}' em '{caminho_pasta}': {e}")

def escrever_em_txt(caminho_arquivo, informacao):
    """
    Escreve uma informação em um arquivo de texto e pula linha.

    Parâmetros:
        caminho_arquivo (str): O caminho para o arquivo de texto.
        informacao (str): A informação a ser escrita no arquivo.
    """

    # Tenta abrir o arquivo no modo de escrita
    with open(caminho_arquivo, 'a') as arquivo:
        arquivo.write(informacao + '\n')

def main():
    parser = argparse.ArgumentParser(description='Conversão de pascal voc -> ssd_mobilenet-jetson.')
    parser.add_argument('--origem', type=str, help='O caminho da pasta de origem com os diretórios')
    parser.add_argument('--destino', type=str, help='O caminho para salvar a pasta destino (root)')
    parser.add_argument('--labels', type=str, help='Uma lista ordenada com os rótulos -> "rótulo1,rótulo2,rótulo3" ')
    args = parser.parse_args()

    origem, destino = args.origem, args.destino

    # Verifica se a pasta de destino existe, se não existir, cria
    if not os.path.exists(destino):
        print(f"A pasta de destino '{destino}' não existe. Criando...")
        os.makedirs(destino)

    if args.labels:
        labels = args.labels.split(',')  # Divide a string de rótulos em uma lista de palavras
        print("Rótulos das classes:", labels)

    # Cria as pastas principais
    criar_pastas(['Annotations', 'ImageSets', 'JPEGImages'], destino+'/root')

    # Cria a Main dentro de ImageSets
    criar_pastas(['Main'], destino+"/root/ImageSets")

    # Copia os arquivos .xml e .jpg para as pastas destino:
    copiar_arquivos(origem, destino)
    
    # Escreve as labels:
    for label in labels:
        escrever_em_txt(destino+'/root/labels.txt', label)

    print("Operação finalizada!")

if __name__ == "__main__":
    main()
