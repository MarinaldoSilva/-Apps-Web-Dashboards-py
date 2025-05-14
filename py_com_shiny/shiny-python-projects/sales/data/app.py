import pandas as pd
from pathlib import Path as pl
from shiny import App, reactive, render, ui        
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Dashboard", fillable=True)

@reactive.calc

#base de dados que será usada nos exemplos
def arquivo():
    #caminho absoluto do arquivo
    arquivo = pl(__file__).parent / "sales.csv"
    return pd.read_csv(arquivo)
    #retorna um dataFrame que ser executado pelo shiny

#tudo dentro desse bloco 'with' é parte do layout de colunas
with ui.layout_columns():
    # Esse bloco renderiza o DataFrame para ser exibido na interface web
    # Ele converte os dados para uma tabela interativa, permitindo rolagem, filtros e ordenação


    @render_plotly
    #O decorador @render_plotly indica que essa função renderiza um gráfico interativo usando Plotly dentro do aplicativo Shiny para Python.Tudo que essa função retorna será exibido como um gráfico na interface.O Shiny automaticamente atualiza esse gráfico caso os dados sejam alterados. Complementação: Esse trecho é essencial para exibir visualizações dinâmicas dentro do dashboard.
    def grafico_top_vendas():
        #responsável por gerar o gráfico de barras.
        df = arquivo()
                     #groupby()agrupa por coluna somando os pedidos de cada produto
                     #sum() somo a quantidade vendida por cada produto
                     #nlargest(24) filtra os 24 produtos mais vendidos
                     #reset_index() com o filtro aplicado, ele reorganiza a posição dos itens para mostrar os tops vendidos
        top_vendas = df.groupby('product')['quantity_ordered'].sum().nlargest(24).reset_index()
        #px.bar 
        #return px.bar(top_vendas, x='product', y= 'quantity_ordered')
        fig = px.pie(df, names='product', values='quantity_ordered', title="Distribuição das Vendas por Produto")
        return fig

    #@render.data_frame
    #def dados_csv():
    #    return arquivo()

