# Análise Interativa de Preços de Alimentos

Este aplicativo permite explorar dados históricos de preços de alimentos coletados pelo Programa Mundial de Alimentos (WFP).

## Funcionalidades

- Visualização interativa dos dados filtrados.
- Gráficos de linha mostrando a variação de preços ao longo do tempo.
- Comparação de preços entre diferentes commodities.
- Mapa interativo dos mercados.
- Análise de tendências com médias móveis.


### **Ajustes Específicos de Atributos**

#### **Entendendo os Atributos do Dataset**

O conjunto de dados possui os seguintes atributos:

- **date:** Data em que o preço foi coletado.
- **admin1:** Região administrativa de nível 1 (pode ser o país ou um estado/província).
- **admin2:** Região administrativa de nível 2 (por exemplo, distrito, município).
- **market:** Nome do mercado onde o preço foi coletado.
- **latitude & longitude:** Coordenadas geográficas do mercado.
- **category:** Categoria do produto (por exemplo, grãos, vegetais).
- **commodity:** Nome específico da commodity (por exemplo, arroz, milho).
- **unit:** Unidade de medida (por exemplo, kg, litro).
- **priceflag:** Indicadores sobre a qualidade ou confiabilidade do preço.
- **pricetype:** Tipo de preço (por exemplo, varejo, atacado).
- **currency:** Moeda em que o preço está denotado.
- **price:** Preço na moeda local.
- **usdprice:** Preço em dólares americanos.


## Como Executar

1. Clone este repositório ou copie os arquivos para o seu ambiente local.
2. Instale as dependências necessárias:

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly
````
3. Execute o aplicativo:

```bash
streamlit run app.py
```