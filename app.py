import streamlit as st
from google.ads.googleads.client import GoogleAdsClient
import pandas as pd

# Configuración de la interfaz
st.title("Analizador de Campañas de Google Ads")
client_id = st.text_input("Ingresa el ID de cliente (formato 123-456-7890):")
fetch_button = st.button("Obtener datos de campañas")

# Función para obtener datos de la API
def get_campaign_data(client_id):
    try:
        # Carga las credenciales (sustituye con la ruta a tu archivo JSON de credenciales)
        client = GoogleAdsClient.load_from_file("google-ads.yaml")
        service = client.get_service("GoogleAdsService")
        
        # Consulta para obtener métricas de campañas
        query = """
        SELECT
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        DURING LAST_30_DAYS"""
        
        response = service.search(customer_id=client_id.replace("-", ""), query=query)
        
        # Procesar resultados
        data = []
        for row in response:
            data.append({
                "Campaña": row.campaign.name,
                "Impresiones": row.metrics.impressions,
                "Clics": row.metrics.clicks,
                "CTR (%)": row.metrics.ctr * 100,
                "CPC Promedio": row.metrics.average_cpc / 1000000  # Convertir de micros
            })
        
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error al obtener datos: {str(e)}")
        return None

# Acción del botón
if fetch_button and client_id:
    with st.spinner("Obteniendo datos..."):
        df = get_campaign_data(client_id)
        if df is not None and not df.empty:
            st.subheader("Resultados de las campañas")
            st.dataframe(df)
        else:
            st.warning("No se encontraron datos para el ID proporcionado.")

# Placeholder para análisis futuro
st.write("Análisis de mejoras se implementará en la próxima versión.")