import streamlit as st
import requests

# Configuración de MOVI
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Control de Devoluciones")

# --- ESTA ES LA PARTE IMPORTANTE ---
# Borra TU_TOKEN_AQUI (pero deja las comillas) y pega tu Token de BoxHero
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446" 
# ----------------------------------

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE_URL = "https://api.boxhero.io/v1"

# Interfaz del empleado
nro_factura = st.text_input("1. Ingrese o escanee el Folio de Factura")

# Esto activa la cámara en el celular
foto_factura = st.camera_input("O escanea el Folio con tu cámara")

# Si el empleado toma una foto, usamos ese dato
if foto_factura:
    st.write("¡Folio capturado!")

if nro_factura:
    st.info(f"Conectado a BoxHero. Buscando datos de: {nro_factura}")
    
    scanned_code = st.text_input("2. Escanee el Código de Barras del producto")
    
    if scanned_code:
        # Aquí es donde el programa hace la magia de comparar cantidades
        st.warning(f"Validando {scanned_code}... Espere un momento.")
        # El resto del código de validación lo agregaremos cuando veas que este abre bien.







