import streamlit as st
import requests
st.title("📦 MOVI: Control de Devoluciones")

# 1. LA CÁMARA (Ahora arriba para que cargue rápido)
foto_factura = st.camera_input("Escanea el Folio con tu cámara")

# 2. EL TEXTO (Abajo por si la cámara no enfoca)
nro_factura = st.text_input("O ingresa el Folio manualmente")

# Lógica para usar cualquiera de los dos
if foto_factura or nro_factura:
    # Si tomó foto, podrías mostrar un mensaje
    if foto_factura:
        st.success("¡Imagen recibida!")
    
    st.info(f"Buscando datos en BoxHero...")

# Configuración de MOVI
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Control de Devoluciones")

# --- ESTA ES LA PARTE IMPORTANTE ---
# Borra TU_TOKEN_AQUI (pero deja las comillas) y pega tu Token de BoxHero
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446" 
# ----------------------------------

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE_URL = "https://api.boxhero.io/v1"


    scanned_code = st.text_input("2. Escanee el Código de Barras del producto")
    
    if scanned_code:
        # Aquí es donde el programa hace la magia de comparar cantidades
        st.warning(f"Validando {scanned_code}... Espere un momento.")
        # El resto del código de validación lo agregaremos cuando veas que este abre bien.








