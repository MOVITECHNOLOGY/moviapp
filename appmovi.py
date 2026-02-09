import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Validador de Productos")

TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

barcode = st.text_input("Escanea o escribe el Código de Barras")

if barcode:
    with st.spinner("Buscando en el Almacén..."):
        # Intentamos la ruta de búsqueda general que es más permisiva
        url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/products"
        params = {"keyword": barcode} # Le pedimos que busque el código como palabra clave
        
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                productos = response.json()
                # Buscamos coincidencia exacta en el código de barras
                p = next((x for x in productos if str(x.get('barcode')) == barcode), None)
                
                if p:
                    st.success(f"✅ PRODUCTO LOCALIZADO")
                    st.subheader(f"🏷️ {p.get('name')}")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Stock Actual", p.get('quantity', 0))
                    c2.write(f"*SKU:* {p.get('sku', 'N/A')}")
                    
                    st.info(f"Área: {p.get('location_name', 'DISPENSARIO')}")
                else:
                    st.warning(f"⚠️ El código '{barcode}' no coincide con ningún producto activo.")
            else:
                st.error(f"Error {response.status_code}: Permisos insuficientes.")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Conectado a: Almacen Movi | Modo: Búsqueda Global")
