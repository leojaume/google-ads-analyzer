import streamlit as st
from google.ads.googleads.client import GoogleAdsClient
import pandas as pd

st.title("Analizador de Campañas de Google Ads")
client_id = st.text_input("Ingresa el ID de cliente (formato 123-456-7890):")
fetch_button = st.button("Obtener datos de campañas")

def get_campaign_data(client_id):
    try:
        client = GoogleAdsClient.load_from_env()
        service = client.get_service("GoogleAdsService")
        query = """
        SELECT
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.average_cpc
        FROM campaign
        WHERE campaign.status IN ('ENABLED', 'PAUSED')
        DURING LAST_30_DAYS"""
        response = service.search(customer_id=client_id.replace("-", ""), query=query)
        data = []
        for row in response:
            data.append({
                "Campaña": row.campaign.name,
                "Impresiones": row.metrics.impressions,
                "Clics": row.metrics.clicks,
                "CTR (%)": row.metrics.ctr * 100,
                "CPC Promedio": row.metrics.average_cpc / 1000000
            })
        df = pd.DataFrame(data)
        return df if not df.empty else None
    except Exception as e:
        st.error(f"Error al obtener datos: {str(e)}")
        return None

if fetch_button and client_id:
    with st.spinner("Obteniendo datos..."):
        df = get_campaign_data(client_id)
        if df is not None:
            st.subheader("Resultados de las campañas")
            st.dataframe(df)
        else:
            st.warning("No se encontraron campañas activas o pausadas en los últimos 30 días.")
st.write("Análisis de mejoras se implementará en la próxima versión.")
