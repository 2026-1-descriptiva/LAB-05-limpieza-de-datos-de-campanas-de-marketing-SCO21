import os
import glob
import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.
    ...
    """
    # 1. Configurar y validar rutas de entrada y salida
    input_dir = "files/input/"
    output_dir = "files/output/"
    
    if not os.path.exists(input_dir):
        input_dir = os.path.join(os.path.dirname(__file__), "../files/input/")
        output_dir = os.path.join(os.path.dirname(__file__), "../files/output/")
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Encontrar y cargar todos los archivos zip en un único dataframe
    zip_files = glob.glob(os.path.join(input_dir, "*.csv.zip"))
    df_list = [pd.read_csv(file) for file in zip_files]
    df = pd.concat(df_list, ignore_index=True)

    # ==========================================
    # PROCESAMIENTO Y LIMPIEZA: client.csv
    # ==========================================
    client_df = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    
    # Limpieza de 'job': quitar '.' y cambiar '-' por '_'
    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    
    # Limpieza de 'education': cambiar '.' por '_' y 'unknown' por pd.NA
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False)
    client_df["education"] = client_df["education"].replace("unknown", pd.NA)
    
    # Conversión binaria de 'credit_default' y 'mortgage' ("yes" -> 1, cualquier otro -> 0)
    client_df["credit_default"] = client_df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    # Guardar client.csv
    client_df.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    # ==========================================
    # PROCESAMIENTO Y LIMPIEZA: campaign.csv
    # ==========================================
    campaign_df = df[[
        "client_id", "number_contacts", "contact_duration", 
        "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "day", "month"
    ]].copy()
    
    # Conversión binaria para outcomes
    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    
    # Mapeo de meses en texto a número con dos dígitos para construir la fecha
    months_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    # Formatear el día a dos dígitos, mapear el mes y construir "YYYY-MM-DD" para el año 2022
    campaign_df["day_str"] = campaign_df["day"].astype(str).str.zfill(2)
    campaign_df["month_str"] = campaign_df["month"].str.lower().map(months_map)
    
    # CORRECCIÓN: El nombre final de la columna debe ser obligatoriamente 'last_contact_date'
    campaign_df["last_contact_date"] = "2022-" + campaign_df["month_str"] + "-" + campaign_df["day_str"]
    
    # Eliminar las columnas temporales e intermedias que no van en el archivo final
    campaign_df = campaign_df.drop(columns=["day", "month", "day_str", "month_str"])
    
    # Guardar campaign.csv
    campaign_df.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    # ==========================================
    # PROCESAMIENTO Y LIMPIEZA: economics.csv
    # ==========================================
    economics_df = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    
    # Guardar economics.csv
    economics_df.to_csv(os.path.join(output_dir, "economics.csv"), index=False)


if __name__ == "__main__":
    clean_campaign_data()