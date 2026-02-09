import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador Final")

# 1. Tu nuevo Token de la foto
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

nro_folio = st.text_input("Ingresa el Folio (ej: municipio)")

if nro_folio:
    st.info(f"Conectando con Almacen Movi...")
    
    # Esta ruta es la más básica para ver movimientos
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/stock-txs"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json().get('list', [])
            # Buscamos 'municipio' en las notas
            encontrado = next((m for m in movimientos if nro_folio.lower() in str(m.get('note', '')).lower()), None)
            
            if encontrado:
                st.success("✅ ¡Folio Localizado!")
                for p in encontrado.get('items', []):
                    st.write(f"⬜ *{p.get('name')}* | Cant: {p.get('quantity')}")
            else:
                st.warning(f"No encontré el folio '{nro_folio}' en movimientos de stock.")
        else:
            st.error(f"Error {response.status_code}: BoxHero sigue restringiendo este Token.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
