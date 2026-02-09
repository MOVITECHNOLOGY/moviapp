import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Ventas")

# 1. Tu Token Actual
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b" 
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

nro_folio = st.text_input("Ingresa el Folio (ej: municipio)")

if nro_folio:
    # Esta es la barra azul que recordabas
    st.info(f"Buscando '{nro_folio}' en Ventas...") 
    
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/orders"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            ventas = response.json().get('list', [])
            encontrado = next((v for v in ventas if nro_folio.lower() in str(v.get('note', '')).lower() or nro_folio.lower() in str(v.get('label', '')).lower()), None)
            
            if encontrado:
                # Esta es la barra verde
                st.success("✅ ¡Venta Localizada!") 
                st.write("### Productos a validar:")
                for p in encontrado.get('items', []):
                    st.write(f"⬜ *{p.get('name')}* | Cant: {p.get('quantity')}")
            else:
                st.warning(f"No encontré el folio '{nro_folio}' en las ventas.")
        else:
            st.error(f"Error {response.status_code}. El Token no tiene permiso de Ventas.")
            st.info("💡 RECOMENDACIÓN: Ve a BoxHero > Ajustes > Miembros y confirma que seas 'Administrador'.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
