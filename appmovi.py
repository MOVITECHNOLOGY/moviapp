import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Folios")

# 2. Credenciales (Tu Token confirmado)
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 3. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio de la salida (ej: municipio)")

if nro_folio:
    st.info(f"Buscando productos del folio: {nro_folio}...")
    
    # URL corregida para el historial de transacciones
    url = "https://api.boxhero.io/v1/tx-history"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json()
            
            # Buscamos el folio en Nota o Referencia
            encontrado = None
            for m in movimientos:
                nota = str(m.get('note', '')).lower()
                ref = str(m.get('reference', '')).lower()
                if nro_folio.lower() in nota or nro_folio.lower() in ref:
                    encontrado = m
                    break
            
            if encontrado:
                st.success(f"✅ Folio Localizado")
                st.write("### Productos a validar:")
                
                # Listamos los productos de esa salida específica
                for p in encontrado.get('items', []):
                    st.write(f"⬜ *{p.get('name')}* | Cantidad: {p.get('quantity')}")
                
                st.divider()
                st.subheader("Paso 2: Escanea para confirmar")
                confirmar = st.text_input("Escanea el código de barras del producto físico")
            else:
                st.error(f"❌ No encontré el folio '{nro_folio}' en las últimas salidas.")
        else:
            st.error(f"Error {response.status_code}: El servidor de BoxHero rechazó la conexión.")
            
    except Exception as e:
        st.error(f"Error inesperado: {e}")
