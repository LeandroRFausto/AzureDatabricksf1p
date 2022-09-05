# Databricks notebook source
# MAGIC %md
# MAGIC ## Esquemas constructors.csv

# COMMAND ----------

dbutils.widgets.text("p_data_source", "")
v_data_source = dbutils.widgets.get("p_data_source")

# COMMAND ----------

dbutils.widgets.text("p_file_date", "2022-07-31")
v_file_date = dbutils.widgets.get("p_file_date")

# COMMAND ----------

# MAGIC %run "../includes/configuration"

# COMMAND ----------

# MAGIC %run "../includes/common_functions"

# COMMAND ----------

constructors_schema = "constructorId INT, constructorRef STRING, name STRING, nationality STRING, url STRING"

# COMMAND ----------

constructors_df = spark.read \
.option("header", True) \
.schema(constructors_schema) \
.csv(f"{raw_folder_path}/{v_file_date}/constructors.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Removendo colunas indesejadas

# COMMAND ----------

from pyspark.sql.functions import col, lit

# COMMAND ----------

constructors_dropped_df = constructors_df.drop(col('url'))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renomeando colunas e ingerindo data

# COMMAND ----------

constructors_renamed_df = constructors_dropped_df.withColumnRenamed("constructorId", "constructor_id") \
                                                 .withColumnRenamed("constructorRef", "constructor_ref") \
                                                 .withColumn("data_source", lit(v_data_source)) \
                                                 .withColumn("file_date", lit(v_file_date))

# COMMAND ----------

constructors_final_df = add_ingestion_date(constructors_renamed_df) 

# COMMAND ----------

# MAGIC %md
# MAGIC ## Escrevendo parquet no datalake

# COMMAND ----------

constructors_final_df.write.mode("overwrite").format("delta").saveAsTable("f1_processed.constructors")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_processed.constructors;

# COMMAND ----------

dbutils.notebook.exit("Success")

# COMMAND ----------

