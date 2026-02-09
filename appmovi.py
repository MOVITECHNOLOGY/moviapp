import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Validador de Productos")

# Datos confirmados de tus fotos
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Entrada del código de barras
barcode = st.text_input("Escanea o escribe el Código de Barras")

if barcode:
    # BARRA AZUL DE CARGA
    with st.spinner(f"Consultando producto {barcode}..."):
        # RUTA INDIVIDUAL (Esta es la llave maestra)
        url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/products/{barcode}"
        
        try:
            response = requests.get(url, headers=HEADERS)
            
            if response.status_code == 200:
                p = response.json()
                # BARRA VERDE DE ÉXITO
                st.success(f"✅ PRODUCTO LOCALIZADO")
                
                st.subheader(f"🏷️ {p.get('name', 'Sin nombre')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Stock Actual", p.get('quantity', 0))
                with col2:
                    st.write(f"*Precio:* ${p.get('price', 0)}")
                
                st.info(f"Ubicación: {p.get('location_name', 'No asignada')}")
                
            elif response.status_code == 404:
                st.warning(f"⚠️ El código '{barcode}' no se encontró en tu inventario.")
            else:
                st.error(f"❌ Error {response.status_code}: Problema de conexión con BoxHero.")
                
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {e}")

st.divider()
st.caption("Validando conexión con Almacen Movi.")
