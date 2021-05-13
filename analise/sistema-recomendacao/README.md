# Sistema de Recomendação de Produtos de um 'Market Place'

- [No notebook Pré Processamento](pre_processamento.ipynb) Está detalhado o passo a passo desde a obtenção dos dados da Olist e o processamento dos dados brutos até o resultado final [dataset processado](olist_processado.csv).

- [Recomendação por Filtro Colaborativo](recomendacao-filtro_colaborativo.ipynb) - Sistema de recomendação item-item computando similaridade usando técnicas de vizinho mais próximo - KNN, utilizando notas de *Review's* dos clientes.

- [Recomendação Baseado no Conteúdo](recomendacao-baseado_conteudo.ipynb). A filtragem colaborativa falha em incorporar novos usuários que ainda não classificaram e novos itens que não possuem classificações ou comentários. Foi usado a Similaridade do Cosseno para construir o sistema de recomendação Baseada em Contéudo para contornar esse problema.


### Para mais esclarecimentos sobre as técnicas e ferramentas utilizadas, consultar o notebook da análise.


## Recomendações para o uso:

iniciar > CMD > enter

pip install -r requirements.txt

jupyter notebook

Veja os notebooks no diretório que acabou de baixar, tem a extensão ipynb


- Caso escolha Docker

iniciar > CMD > enter

```
make start

```
