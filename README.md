# AzureDatabricksf1p

Implementa uma solução de Engenharia de dados para análises da Fórmula 1. O projeto utiliza exclusivamente a Azure, com o Databricks como principal componente. Os dados são fornecidos pela Ergast Developer API, serviço que gere dados históricos do esporte. <p>As transformações, conversões e incrementos são feitos em notebooks Databricks e o Data Factory é responsável pela orquestração, automatização e monitoramento dos pipelines.<p>
A estrutura captura dados automática e semanalmente, os insere no data lake ativando o pipeline para atualização do estudo e relatório.
Arquivos utilizados na API no formato CSV: CIRCUITS, CONSTRUCTORS, DRIVERS, LAP TIMES, PIT STOPS, QUALIFYING, RACES e RESULTS.

## Arquitetura
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/arquitetura.png"/>
</p>

## Recursos utilizados no Azure:
* Data Lake Gen2 para armazenar dados brutos, processados e de apresentação.
* Databricks e Spark para ingestão, transformação, conversão e exibição de dashboards. 
* Delta lake para utilizar funções exclusivas do formato.
* Key Vault para gerenciamento na segurança de acesso.
* Data Factory para automatização e orquestração.
* Power BI para exibição de relatórios.

## Preparo preliminar do ambiente
* Criar uma conta Azure, uma subscription e um resource group usado como um contêiner do projeto.
* Criar conta de armazenamento.
* Criar um Databricks
* Criar um Data Factory.
* Criar um dashboard com os recursos do projeto.

## Diagrama de entidade e relacionamento da API
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/ergast_db.png"/>
</p>

## Workspace do Databricks
O projeto foi construído com a seguinte estrutura de pastas:
* set-up - Que faz a montagem de armazenamento da estrutura: "raw" para dados brutos, "processed" para os transformados e "presentation" para os prontos. 
* raw - Que cria as tabelas a serem alimentadas pelos dados do data lake.
* includes - Para os arquivos de configuração e funções comuns aos notebooks. 
* utils - Que prepara o ambiente para incrementação.
* ingestion - Para realizar as transformações dos arquivos.
* trans - Para hospedar as transformações dos arquivos.
* analysis - Para os arquivos prontos e dashboards.

Os arquivos do workspace de extensão .sql e .py gerados no projeto se encontram no link abaixo:
https://github.com/LeandroRFausto/AzureDatabricksf1p/tree/main/f1p/databricks


## Extração e ingestão
Após criação dos recursos necessários, monta-se a estrutura e criam-se tabelas a serem utilizadas. A primeira extração e carregamento ocorre manualmente.  
De forma resumida, os notebooks da parte de ingestão verificam os esquemas; selecionam, renomeiam, criam ou excluem colunas; adicionam dados ao dataframe e escrevem simultaneamente na database e data lake. Este último ultilizando o formato Delta.
Como são oito arquivos, um arquivo de ingestão geral também foi criado para rodar os scripts simultaneamente. 
	
## Transformação
Nesta fase os arquivos se juntam dando vida a novas fontes de consulta, mais uma vez ocorrem transformações para não haver conflitos nos joins que são realizados. 
Basicamente os arquivos "race_results, driver_standlings e constructor_standings dão origem a o calculed_race_results, que usa Delta lake para criar tabelas e views com base em merge. E, por fim, o arquivo create_presentation_database, que cria a database de apresentação e estrutura as análises.

## Análises
Aqui são criadas as análises em geral, neste notebook são exibidos os maiores pilotos da história da fórmula 1, suas quantidades de corridas, pontos e médias. Os mesmos campos também são exibidos num recorte dos últimos 20 anos. As mesmas consultas também são feitas para as equipes.
Um Dashboard construído em um notebook dedicado a visualização também é feito.
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/dash_pilotos.png"/>
</p>

<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/dash_equipes.png"/>
</p>

## Carregamento incremental
Para atualização do estudo, utiliza-se carregamento incremental. Como os arquivos são pequenos, o carregamento total (full load) poderia ser adotado, porém o objetivo do estudo é simular o ambiente de produção.
widgets para inserção das datas são inseridos nos campos dos arquivos de ingestão. Assim apenas os dados novos são carregados.

## Ingestão de novos arquivos, automatização e orquestração
Os seguintes pipelines são criados:
* de extração, que semanalmente baixa os dados da API. 
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/pl1.png"/>
</p>
* de ingestão, que roda o notebook all_ingest do Databricks.
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/pl2.png"/>
</p>
* de transformação, como há uma dependência ao arquivo "race results" os arquivos não são processados simultaneamente.
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/pl3.png"/>
</p>
* de processo, um pipeline pai que executa os de ingestão e transformação.
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/pl_master.png"/>
</p>
A orquestração se dá com triggers com os mesmos padrões dos pipelines:
* de extração, do tipo "Schedule", agendado para repetir semanalmente.  
* de ingestão, do tipo "Storage events", que roda assim que um novo arquivo chega ao "raw" do data lake.
* de transformação, do tipo "Storage events", que roda assim que o novo arquivo, ingerido no pipeline do "raw", chega ao "processed" do datalake.
<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/triggers.png"/>
</p>


## Relatório (preliminar)
O Power BI foi usado para gerar um relatório dos arquivos tratados. A escolha foi retratar a trajetória do ídolo Ayrton Senna.  

<p align="center">
<img src="https://github.com/LeandroRFausto/AzureDatabricksf1p/blob/main/f1p/imagens/pbi.png"/>
</p>
