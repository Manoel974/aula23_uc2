import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import os 
from sqlalchemy import create_engine

# Dados para ler SQL


host = "localhost"
user = "root"
password = "root"
database = "bd_roubos_coletivos"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# TRY 1: COLETANDO E PROCESSANDO DADOS
try:
    # leitura dos dados da tabela de produtos
    tb_base = pd.read_sql("basedp",engine)
    tb_roubo_coletivos = pd.read_sql("basedp_roubo_coletivo",engine)
    
    # Calculando e separando dados
    df_roubo_coletivos = pd.merge(tb_base, tb_roubo_coletivos, on="cod_ocorrencia")
    print(df_roubo_coletivos)

    # Separando, agrupando e filtrando dados
    df_roubo_coletivos = pd.merge(tb_base, tb_roubo_coletivos, on="cod_ocorrencia")
    df_roubo_coletivos = df_roubo_coletivos[(df_roubo_coletivos["ano"]>=2022) & (df_roubo_coletivos["ano"]<=2023)]
    df_roubo_coletivos = df_roubo_coletivos[["aisp","roubo_em_coletivo"]]
    df_roubo_coletivos = df_roubo_coletivos.groupby(["aisp"]).sum(["roubo_em_coletivo"]).reset_index()
    
    # df_roubo_coletivos_final

    print(df_roubo_coletivos)

except Exception as e:
    print(f"Erro {e}")

try:
    print('Obtendo Dados...')

    array_roubo_coletivos = np.array(df_roubo_coletivos['roubo_em_coletivo'])
    media_roubo_coletivos = np.mean(array_roubo_coletivos)
    mediana_roubo_coletivos = np.median(array_roubo_coletivos)
    distancia_media_mediana = abs((media_roubo_coletivos - mediana_roubo_coletivos) / mediana_roubo_coletivos)

    maximo = np.max(array_roubo_coletivos)
    minimo = np.min(array_roubo_coletivos)
    amplitude = maximo - minimo

    q1 = np.quantile(array_roubo_coletivos, 0.25, method='weibull')
    q2 = np.quantile(array_roubo_coletivos, 0.50, method='weibull')
    q3 = np.quantile(array_roubo_coletivos, 0.75, method='weibull')

    iqr = q3 - q1
   
    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    df_roubo_coletivos_outliers_inferiores = df_roubo_coletivos[tb_roubo_coletivos['roubo_em_coletivo'] < limite_inferior]
    df_roubo_coletivos_outliers_superiores = df_roubo_coletivos[tb_roubo_coletivos['roubo_em_coletivo'] > limite_superior]


    variancia_roubo = np.var(array_roubo_coletivos)
    desvio_padrao = np.std(array_roubo_coletivos)
    dist_var_med = variancia_roubo / (media_roubo_coletivos ** 2)
    coeficiente_variacao = (desvio_padrao / media_roubo_coletivos) *100

    assimetria = df_roubo_coletivos['roubo_em_coletivo'].skew()
    curtose = df_roubo_coletivos['roubo_em_coletivo'].kurtosis()

    print(media_roubo_coletivos)
    print(mediana_roubo_coletivos)
    print(distancia_media_mediana)

    print('\nMEDIDAS DE DISPERSÃO:')
    print(30*'-')
    print('\nMÍNIMO: ', minimo)
    print(f'Limite Inferior: {limite_inferior:.2f}')
    print('Q1 (25%): ', q1)
    print('Q2 (50%): ', q2)
    print('Q3 (75%): ', q3)
    print(f'IQR: {iqr:.2f}')
    print(f'\n Limite Superior: {limite_superior:.2f}')
    print('\nMÁXIMO: ', maximo)
    print('\nMunicípios com outliers inferiores:')
    print(30*'-')
    if len(df_roubo_coletivos_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_coletivos_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nMunicípios com outliers superiores:')
    print(30*'-')
    if len(df_roubo_coletivos_outliers_superiores) == 0:
        print('Não existem outliers superiores!')
    else:
        print(df_roubo_coletivos_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
    
   
except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()    


try:
    plt.subplots(2,2, figsize=(16,7))
    plt.suptitle("Análise de Roubo em Coletivos no RJ", fontsize=20)

    plt.subplot(2,2,1)
    plt.boxplot(array_roubo_coletivos, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # Histograma
    plt.subplot(2, 2, 2)
    plt.hist(array_roubo_coletivos, bins=50, edgecolor="black")
    plt.axvline(media_roubo_coletivos, color="g", linewidth=1)
    plt.axvline(mediana_roubo_coletivos, color="y", linewidth=1)
    plt.title("Histograma:")

    # Terceira posição
    plt.subplot(2, 2, 3)
    plt.text(0.1, 0.9, f'Média: {media_roubo_coletivos}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_coletivos}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.title("Medidas Observadas:")
    plt.axis("off")

    # Quarta posição
    plt.subplot(2, 2, 4)
    plt.text(0.1, 0.9, f'Assimetria: {assimetria}', fontsize=12)
    plt.text(0.1, 0.8, f'Curtose: {curtose}', fontsize=12)
    plt.text(0.1, 0.7, f'Variância: {variancia_roubo}', fontsize=12)
    plt.text(0.1, 0.6, f'Desvio Padrão: {desvio_padrao}', fontsize=12)
    plt.text(0.1, 0.5, f'Distância entre Variância e Média: {dist_var_med}', fontsize=12)
    plt.text(0.1, 0.4, f'Coeficiente de Variação: {coeficiente_variacao}', fontsize=12)
    plt.title("Demais Medidas:")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
  
    # plt.subplots(2, 2, figsize=(16, 7))
    # plt.suptitle('Análise de roubos coletivos no RJ')

    # plt.subplot(1, 2, 1)
    # plt.boxplot(array_roubo_coletivos, vert=False, showmeans=True)
    # plt.title('Bolxplot dos Dados')
    #     # Segunda subplot: Exibição de informações estatísticas
    # plt.subplot(1, 2, 2)  # Configurar o segundo gráfico no lado direito
    # plt.text(0.1, 0.9, f'Média: {media_roubo_coletivos}', fontsize=12)
    # plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_coletivos}', fontsize=12)
    # plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana}', fontsize=12)
    # plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    # plt.text(0.1, 0.5, f'Limite inferior: {limite_inferior}', fontsize=12)
    # plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    # plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    # plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=12)
    # plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    # plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)
    # plt.title('Medidas Observadas')

    # plt.subplot(2, 2, 2,)
    # plt.hist(array_roubo_coletivos, bins=50, edgecolor="black")
    # plt.axvline(media_roubo_coletivos, color="g", linewidth=1)
    # plt.axvline(mediana_roubo_coletivos, color="y", linewidth=1)

    # plt.boxplot(array_roubo_coletivos)
    
    # plt.boxplot(array_roubo_coletivos, vert=False, showmeans=True, showfliers=False)

    #  # Quarta posição
    # plt.subplot(2, 2, 4)
    # plt.text(0.1, 0.9, f'Assimetria: {assimetria}', fontsize=12)
    # plt.text(0.1, 0.8, f'Curtose: {curtose}', fontsize=12)
    # plt.title("Assimetria e Curtose")

    # plt.axis("off")


    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()




except ImportError as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()





os.system('cls')