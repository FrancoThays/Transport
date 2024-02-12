'''
objeto para processamento de regressão linear multivariada
Thays Franco
2022-04-08
'''

#================================================
#IMPORTS
import statsmodels.formula.api as smf

#================================================
#CLASSE CalculadorEstatistico

class CalculadorEstatistico:

    def __init__(self, funcao, df_dados):
        model = smf.ols(funcao, df_dados)
        self.result = model.fit()

    def pega_sumario(self):
        return self.result.summary()

    def prediz(self, dados_futuros):
        return self.result.predict(dados_futuros)

    def pega_resultados(self):
        a0 = self.result.params[0]
        a1 = self.result.params[1]
        a2 = self.result.params[2]
        r_quadrado = self.result.rsquared
        p_valules = self.result.pvalues



        return a0, a1, a2, r_quadrado, p_valules
