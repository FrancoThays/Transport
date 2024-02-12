'''
objeto para processamento de geração de viagens
Thays Franco
2022-04-08
'''
#==========================================================
#IMPORTS
import pathlib as pl
import pandas as pd
import time
from entidades.CalculadorEstatistico import CalculadorEstatistico
from entidades.GeradorRelatorio import GeradorRelatorio
import locale
import matplotlib.pyplot as plt
import numpy as np
from docx2pdf import convert
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#==========================================================
#DADOS
arquivo_dados_atuais = pl.Path("../Dados/dados_atuais.xlsx")
arquivo_dados_futuros = pl.Path("../Dados/dados_futuros.xlsx")
arquivo_relatorio = pl.Path("../RESULTADOS/relatorio.docx")
arquivo_grafico = pl.Path("../RESULTADOS/grafico.png")
arquivo_pdf = pl.Path("../RESULTADOS/relatorio.pdf")

#==========================================================
#CLASSE Geracao

class Geracao:

    def __init__(self):

        start_time = time.time()
        print("Iniciando procedimento.")

        relatorio = GeradorRelatorio()

        #Lendo arquivo de dados de entrada
        df_atuais = pd.read_excel(arquivo_dados_atuais)
        #print(df_atuais)
        df_futuros = pd.read_excel(arquivo_dados_futuros)
        #print(df_futuros)

        #Executando as regressões
        modelo_producao = CalculadorEstatistico("producao ~ vol_prod + emprego", df_atuais)
        modelo_atracao = CalculadorEstatistico("atracao ~ populacao + emprego", df_atuais)

        print("parâmetros produção")
        parametros_prod = modelo_producao.pega_resultados()
        print("parâmetros atração")
        parametros_atra = modelo_atracao.pega_resultados()

        #Jogando os dados de entrada no relatório
        relatorio.insere_secao("Dados de entrada",1)
        relatorio.insere_secao("Dados atuais", 2)
        relatorio.insere_tabela(df_atuais)
        relatorio.insere_secao("Dados futuros", 1)
        relatorio.insere_tabela(df_atuais)

        #parâmetros do modelo
        relatorio.insere_secao("Parâmetros do modelo", 1)
        relatorio.insere_secao("Produção",2)
        relatorio.insere_paragrafo(locale.format_string("producao = %0.3f + %0.3f * vol_prod + %0.3f * emprego", (parametros_prod[0], parametros_prod[1], parametros_prod[2])))
        relatorio.insere_paragrafo(locale.format_string("r^2 = %0.2f", parametros_prod[3]))
        relatorio.insere_paragrafo(self.imprime_p_values(parametros_prod[4]))

        relatorio.insere_secao("Atração", 2)
        relatorio.insere_paragrafo(locale.format_string("atracao = %0.3f + %0.3f * populacao + %0.3f * emprego",(parametros_atra[0], parametros_atra[1], parametros_atra[2])))
        relatorio.insere_paragrafo(locale.format_string("r^2 = %0.2f", parametros_atra[3]))
        relatorio.insere_paragrafo(self.imprime_p_values(parametros_atra[4]))

        #Predição dos dados futuros
        projecao_producao = modelo_producao.prediz(df_futuros)
        projecao_atracao = modelo_atracao.prediz(df_futuros)

        resultados = pd.DataFrame()
        resultados['zona'] = df_atuais['zona']
        resultados['prod_fut'] = projecao_producao
        resultados['atra_fut'] = projecao_atracao
        print(resultados)

        #relatorio.insere_quebra_de_pagina()

        #calculando o fator de ajuste
        f_aj = resultados['prod_fut'].sum() / resultados['atra_fut'].sum()
        print("fator de ajuste = %f" % f_aj)
        resultados['atra_fut_aj'] = resultados['atra_fut'] * f_aj
        resultados = resultados.round().astype('int')

        # jogando as tabelas futuras para o relatório
        relatorio.insere_secao("Resultados da projeção", 1)
        relatorio.insere_paragrafo(locale.format_string("Fator de ajuste = %0.3f", f_aj))
        relatorio.insere_tabela(resultados)

        #transformando colunas em listas
        af_aj = resultados['atra_fut_aj'].tolist()
        pf = resultados['prod_fut'].tolist()
        zonas = resultados['zona'].tolist()

        #criando o gráfico
        x = np.arange(len(zonas))
        width = 0.35

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, pf, width, label = 'Produção')
        rects2 = ax.bar(x + width/2, af_aj, width, label = 'Atração ajustada')

        #costumização
        ax.set_ylabel('Número de viagens')
        ax.set_xlabel('Zonas de tráfego')
        ax.set_title('Viagens futuras por atração e produção')
        ax.set_xticks(x, zonas)
        ax.legend()

        ax.bar_label(rects1, padding = 3, fontsize = 6)
        ax.bar_label(rects2, padding = 3, fontsize = 6)


        fig.tight_layout()

        #exportando o gráfico
        plt.savefig(arquivo_grafico)

        #adicionando ao relatório
        relatorio.insere_secao("Representação gráfica", 1)
        relatorio.insere_imagem(arquivo_grafico)


        relatorio.conclui_documento(arquivo_relatorio)

        #convertendo o arquivo docx para pdf
        input_file = arquivo_relatorio
        output_file = arquivo_pdf
        file = open(output_file, "w")
        file.close()

        convert(input_file, output_file)
        

        print("Tempo de execução = %f segundos." %(time.time() - start_time))

    def imprime_p_values(self, p_values):

        p_values_string = ""

        for i, p_value in enumerate(p_values):
            if p_value < 0.05:
                p_values_string += locale.format_string("p-value[%d] = %0.4f : OK!!\n", (i, p_value))
            else:
                p_values_string += locale.format_string("p-value[%d] = %0.4f\n", (i, p_value))

        return p_values_string.rstrip()


if __name__ == "__main__":
    geracao = Geracao()
