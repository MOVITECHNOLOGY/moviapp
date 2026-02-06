import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Control de Devoluciones")

# 2. Llaves de acceso
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json"
}

# 3. Entrada de Folio
foto_factura = st.camera_input("Escanea el Folio con tu cámara")
nro_factura = st.text_input("O ingresa el Folio manualmente")

if foto_factura or nro_factura:
    st.success("¡Folio detectado!")

# 4. Búsqueda de Producto
scanned_code = st.text_input("Escriba o escanee el Código de Barras del producto")

if scanned_code:
    st.info(f"Buscando '{scanned_code}' en BoxHero...")
    
    # URL CORREGIDA: Usamos el filtro de barcode correctamente
    url = f"https://api.boxhero.io/v1/items?barcode={scanned_code}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            datos = response.json()
            # BoxHero devuelve una lista, revisamos si tiene algo
            if isinstance(datos, list) and len(datos) > 0:
                p = datos[0]
                st.balloons() # ¡Festejo!
                st.markdown(f"## ✅ {p.get('name')}")
                st.metric("Stock disponible", p.get('quantity'))
                if p.get('price'):
                    st.write(f"*Precio:* ${p.get('price')}")
            else:
                st.error("❌ Código no encontrado. Revisa si el producto existe en BoxHero.")
        else:
            st.error(f"❌ Error {response.status_code}: Revisa la configuración del TOKEN.")
            
    except Exception as e:
        st.error(f"Error inesperado: {e}")

