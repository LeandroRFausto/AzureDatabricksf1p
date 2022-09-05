# Databricks notebook source
# MAGIC %md
# MAGIC ## Esquemas drivers.csv

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

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DateType

# COMMAND ----------

drivers_schema = StructType(fields=[StructField("driverId", IntegerType(), False),
                                     StructField("driverRef", StringType(), True),
                                     StructField("number", IntegerType(), True),
                                     StructField("code", StringType(), True),
                                     StructField("forename", StringType(), True),
                                     StructField("surname", StringType(), True),
                                     StructField("dob", DateType(), True),
                                     StructField("nationality", StringType(), True),
                                     StructField("url", StringType(), True)
])

# COMMAND ----------

drivers_df = spark.read \
.option("header", True) \
.schema(drivers_schema) \
.csv(f"{raw_folder_path}/{v_file_date}/drivers.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Renomeando, adicionando e excluindo colunas

# COMMAND ----------

from pyspark.sql.functions import concat, col, lit

# COMMAND ----------

drivers_renamed_df = drivers_df.withColumnRenamed("driverId", "driver_id") \
                                    .withColumnRenamed("driverRef", "driver_ref") \
                                    .withColumn("name", concat(col('forename'), lit(' '), col('surname'))) \
                                    .withColumn("data_source", lit(v_data_source)) \
                                    .withColumn("file_date", lit(v_file_date))

# COMMAND ----------

drivers_add_df = add_ingestion_date(drivers_renamed_df)
                                    

# COMMAND ----------

drivers_final_df = drivers_add_df.drop(col("forename")) \
                                          .drop(col("surname")) \
                                          .drop(col("url"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Alterando a ordem das colunas

# COMMAND ----------

drivers_final_df = drivers_final_df [['driver_id', 'driver_ref', 'number', 'code', 'name', 'dob', 'nationality', 'ingestion_date']]

# COMMAND ----------

# MAGIC %md
# MAGIC ## Escrevendo parquet no datalake

# COMMAND ----------

drivers_final_df.write.mode("overwrite").format("delta").saveAsTable("f1_processed.drivers")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM f1_processed.drivers

# COMMAND ----------

dbutils.notebook.exit("Success")