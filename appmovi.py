import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Ventas")

# 1. Credenciales Confirmadas
TOKEN = "872810ff-7e4b-44f3-a3a9-d437c59e7ddc"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

nro_folio = st.text_input("Ingresa el Folio (ej: municipio)")

if nro_folio:
    st.info(f"Buscando '{nro_folio}' en Ventas...")
    
    # REGRESAMOS A LA RUTA DE VENTAS
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/orders"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            ventas = response.json().get('list', [])
            # Buscamos 'municipio' en el nombre o nota de la venta
            encontrado = next((v for v in ventas if nro_folio.lower() in str(v.get('note', '')).lower() or nro_folio.lower() in str(v.get('label', '')).lower()), None)
            
            if encontrado:
                st.success("✅ ¡Venta Localizada!")
                # Listamos productos
                st.write("### Productos a validar:")
                for p in encontrado.get('items', []):
                    st.write(f"⬜ *{p.get('name')}* | Cant: {p.get('quantity')}")
            else:
                st.warning(f"No encontré el folio '{nro_folio}' en las ventas recientes.")
        else:
            st.error(f"Error {response.status_code}. El Token necesita permiso de 'Ventas' (Order Read).")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
