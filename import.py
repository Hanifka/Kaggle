import requests
from google.cloud import bigquery
import pandas as pd



import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/user/Downloads/quiet-platform-366707-35d83cedf5ba.json"


#===========================================================================
client = bigquery.Client()
# Make a request to the API
response = requests.get("http://universities.hipolabs.com/search?country=Indonesia")


# Retrieve the data from the response
data = response.json()

df = pd.json_normalize(data)
df.rename(columns = {'state-province':'stateprovince'}, inplace = True)


df['web_pages'] = df['web_pages'].str[0]
df['domains'] = df['domains'].str[0]



#=============================================================================
table_id = 'quiet-platform-366707.dataset3.tugas3'



job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    schema=[
        # Specify the type of columns whose type cannot be auto-detected. For
        # example the "title" column uses pandas dtype "object", so its
        # data type is ambiguous.
        bigquery.SchemaField("alpha_two_code", bigquery.enums.SqlTypeNames.STRING),
        # Indexes are written if included in the schema by name.
        bigquery.SchemaField("name", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("domains", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("stateprovince", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("country", bigquery.enums.SqlTypeNames.STRING),
       
      

    ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    # write_disposition="WRITE_TRUNCATE",
)

job = client.load_table_from_dataframe(
    df, table_id, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)

