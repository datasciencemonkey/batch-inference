#%%
import random
from locust import HttpUser, task, stats
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
stats.PERCENTILES_TO_CHART = [0.95,0.75,0.5]
input_file = "./data/sample_data_pd.csv"
system_prompt = """Could you summarize the content with an appropriate question or title? 
Brainstormed content: """
request_params = {"max_tokens": 1000, "temperature": 0}  # Changed this line
#%%
# with open(input_file, "r") as file:
#     lines = file.readlines()
# model_inputs = [line.strip() for line in lines if line.strip()]
df  = pd.read_csv("data/sample_data_pd.csv") 
choice_list = df.response.to_list()
#%%
class LoadTestUser(HttpUser):
    host = os.getenv("HOSTNAME")
    token = os.getenv("TOKEN")
    endpoint_name = "llamatest-benchmark"

    @task
    def query_single_model(self):
        headers = {"Authorization": f"Bearer {self.token}"}
       
        text_input = random.choice(choice_list)
        messages = [{"role": "user", "content": system_prompt + str(text_input)}]
        print(messages)
        json_input = {"messages": messages,**request_params}

        response = self.client.post(f"/serving-endpoints/{self.endpoint_name}/invocations",
                         headers=headers,
                         json=json_input)
        print(f"Response:{response.json()}")
