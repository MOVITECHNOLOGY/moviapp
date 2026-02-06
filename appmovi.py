import streamlit as st
import requests

# Configuración inicial
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Control de Devoluciones")

# 1. LA CÁMARA Y EL FOLIO
foto_factura = st.camera_input("Escanea el Folio con tu cámara")
nro_factura = st.text_input("O ingresa el Folio manualmente")

# Configuración de BoxHero (Tu Token ya está aquí)
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

if foto_factura or nro_factura:
    st.success("¡Folio detectado!")
    st.info("Buscando datos en BoxHero...")

# 2. ESCANEO DEL PRODUCTO (Sin espacios al inicio)
scanned_code = st.text_input("2. Escanee el Código de Barras del producto")

if scanned_code:
    st.warning(f"Validando producto: {scanned_code}...")
    # Aquí es donde el código conectará con tu inventario después
# ESTO ES LO QUE FALTA PARA BUSCAR EN EL INVENTARIO
    url_busqueda = f"https://api.boxhero.io/v1/items?barcode={scanned_code}"
    respuesta = requests.get(url_busqueda, headers=HEADERS)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        if datos:
            producto = datos[0] # Agarramos el primer resultado
            nombre = producto.get('name', 'Sin nombre')
            stock = producto.get('quantity', 0)
            
            st.success(f"✅ PRODUCTO: {nombre}")
            st.metric("Stock actual", stock)
        else:
            st.error("❌ Código no encontrado en BoxHero")
    else:
        st.error("Hubo un problema al conectar con BoxHero")





