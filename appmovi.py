import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Validador de Stock")

# 1. Tu nuevo Token confirmado
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Ahora buscaremos por nombre de producto directamente
producto_buscar = st.text_input("Ingresa el nombre del producto (ej: Guantes)")

if producto_buscar:
    st.info(f"Buscando '{producto_buscar}' en el inventario actual...")
    
    # RUTA DE PRODUCTOS (Es la que menos permisos pide)
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/products"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            lista_productos = response.json()
            # Buscamos coincidencia en el nombre
            encontrados = [p for p in lista_productos if producto_buscar.lower() in p.get('name', '').lower()]
            
            if encontrados:
                st.success(f"✅ Se encontraron {len(encontrados)} coincidencias:")
                for p in encontrados:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"*{p.get('name')}*")
                        st.caption(f"Código: {p.get('barcode')}")
                    with col2:
                        st.metric("Stock", p.get('quantity', 0))
            else:
                st.warning(f"No hay productos llamados '{producto_buscar}' en el inventario.")
        else:
            st.error(f"Error {response.status_code}. El token sigue sin permisos suficientes.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
