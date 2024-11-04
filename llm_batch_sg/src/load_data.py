#%%
from datasets import load_dataset  # Add this import
from databricks.connect import DatabricksSession
#%%
spark = (
    DatabricksSession.builder.profile("DEFAULT").remote(serverless=True).getOrCreate()
)

# %%
# Load the Databricks Dolly 15k dataset
dolly_dataset = load_dataset("databricks/databricks-dolly-15k", cache_dir=".datasets/")
# Print some information about the dataset
spdf = spark.createDataFrame(dolly_dataset["train"].to_pandas())
print("INFO: Data downloaded and written to a local dataframe")
# %%
spdf.write.format("delta").mode("overwrite").saveAsTable("sgfs.default.dolly_data")
# %%
print("INFO: Data downloaded and written to DBSQL Table")
print("INFO: Sample records from the table")
spark.sql("select * from sgfs.default.dolly_data limit 10").show()
# %%
