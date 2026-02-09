import streamlit as st
import requests

st.title("📦 MOVI: Validador de Emergencia")

# Tu token actual que ya sabemos que existe
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Vamos a buscar directamente el producto, sin pasar por 'ventas'
barcode = st.text_input("Escribe el Código de Barras (ej: 2002746640555)")

if barcode:
    st.info(f"Buscando producto {barcode}...")
    
    # Esta ruta suele estar abierta para todos los tokens
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/products"
    
    try:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            productos = r.json()
            # Buscamos el código en la lista que nos mande
            encontrado = next((p for p in productos if str(p.get('barcode')) == barcode), None)
            
            if encontrado:
                st.success(f"✅ ¡ENCONTRADO!")
                st.subheader(encontrado.get('name'))
                st.metric("Stock en Almacén", encontrado.get('quantity'))
            else:
                st.warning("Ese código no está en tu inventario actual.")
        else:
            st.error(f"Error {r.status_code}: BoxHero no suelta la información.")
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
