"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile
import pandas as pd
import glob

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    df = pd.DataFrame()

    files = glob.glob("files/input/*")
    for file in files:
        with zipfile.ZipFile(file) as z:
            with z.open(z.namelist()[0]) as f:
                df_file = pd.read_csv(f)
                df = pd.concat(
                    objs=[
                        df,
                        df_file
                    ],
                    axis=0,
                    join='outer',
                    ignore_index=False,
                    sort=False
                )
    
    df_client = df[['client_id', 'age', 'job', 
                'marital', 'education', 
                'credit_default', 'mortgage']].copy()
    
    df_client.job = df_client.job.str.replace(".", "")
    df_client.job = df_client.job.str.replace("-", "_")
    
    df_client.education = df_client.education.str.replace(".", "_")
    df_client.education = df_client.education.map(lambda x: x if x != 'unknown' else pd.NA)
    
    df_client.credit_default = df_client.credit_default.map(lambda x: 1 if x == 'yes' else 0)
    df_client.mortgage = df_client.mortgage.map(lambda x: 1 if x == 'yes' else 0)

    df_campaign = df[['client_id', 'number_contacts', 
                      'contact_duration', 'previous_campaign_contacts', 
                      'previous_outcome', 'campaign_outcome']].copy()
    
    
    df_campaign['last_contact_date'] = "2022" + "-" + df['month'].astype(str)+ "-" + df['day'].astype(str)
    
    print(df_campaign.head())

    df_campaign.last_contact_date = pd.to_datetime(
        df_campaign.last_contact_date,
        format="%Y-%b-%d"
    )

    df_campaign.previous_outcome = df_campaign.previous_outcome.map(lambda x: 1 if x == 'success' else 0)
    df_campaign.campaign_outcome = df_campaign.campaign_outcome.map(lambda x: 1 if x == 'yes' else 0)


    df_economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    

    if os.path.exists("files/output"):
        for file in glob.glob("files/output/*"):
            os.remove(file)
    else:
        os.makedirs("files/output")

    df_client.to_csv("files/output/client.csv", index=False)
    df_campaign.to_csv("files/output/campaign.csv", index=False)
    df_economics.to_csv("files/output/economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()
