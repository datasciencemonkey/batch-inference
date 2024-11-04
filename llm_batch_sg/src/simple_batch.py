# %pip install -r requirements.txt # ruff: noqa: E501
# dbutils.library.restartPython()

# COMMAND ----------
# %%
from databricks import sql
from dotenv import load_dotenv
import os
import pandas as pd
from databricks.sdk import WorkspaceClient
import warnings
import base64

# %%
warnings.filterwarnings("ignore")
mode = "bricks"

print(os.getenv("DATABRICKS_SERVER_HOSTNAME"))
if mode == "local":
    load_dotenv(dotenv_path="./.env")
    connection = sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN"),
    )
elif mode == "bricks":
    w = WorkspaceClient()
    try:
      sql_host = w.secrets.get_secret("sgscope", "sql_host").value
      http_path = w.secrets.get_secret("sgscope", "http_path").value
      access_token = w.secrets.get_secret("sgscope", "access_token").value
      connection = sql.connect(
          server_hostname=base64.b64decode(sql_host).decode(),
          http_path=base64.b64decode(http_path).decode(),
          access_token=base64.b64decode(access_token).decode(),
      )
    except Exception as e:
      print(e)

# %%
#configure this as needed
query = """
WITH data AS (
  SELECT response as text
  FROM sgfs.default.dolly_data
  WHERE category = 'brainstorming'
  LIMIT 100
)
  SELECT
    text,
    ai_query(
      'llamatest',
      CONCAT('summarize the content with an appropriate question or title? Brainstormed content:', text)
    ) AS label
  FROM data
"""
df = pd.read_sql(query, connection)
# %%
print(df.head())
# %%
