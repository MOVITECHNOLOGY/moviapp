import streamlit as st
import requests

# 1. Configuración inicial
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Control de Devoluciones")

# 2. Tu llave Maestra de BoxHero
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 3. Interfaz de Folio
foto_factura = st.camera_input("Escanea el Folio con tu cámara")
nro_factura = st.text_input("O ingresa el Folio manualmente")

if foto_factura or nro_factura:
    st.success("¡Folio detectado!")

# 4. Escaneo del Producto y Búsqueda Real
scanned_code = st.text_input("2. Escanee el Código de Barras del producto")

if scanned_code:
    st.info(f"Buscando '{scanned_code}' en BoxHero...")
    
    # Esta es la dirección para buscar el producto
    url = f"https://api.boxhero.io/v1/items?barcode={scanned_code}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            productos = response.json()
            if productos:
                p = productos[0] # Tomamos el primer resultado
                st.balloons() # ¡Festejo!
                st.write(f"### ✅ Producto: {p.get('name')}")
                st.write(f"*Stock actual:* {p.get('quantity')}")
                st.write(f"*Precio:* ${p.get('price')}")
            else:
                st.error("❌ No encontré ese código en BoxHero.")
        else:
            st.error("Error de conexión con la API.")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")





