#### `llm_batch_sg` folder:
This folder contains code for batch processing using LLM (Large Language Model) on Databricks. Shows developing and running asset bundles that run serverless workflows which in turn run inference on Provisioned Throughput Endpoints using Databricks Connect.

#### `load_testing` folder:
Shows load testing code for the batch job in question using locust. Note: This will NOT be required in the future versions of batch inference. As of this writing (Nov 2024), this is needed to properly saturated the Provisioned Throughput Endpoint that serves the model.
