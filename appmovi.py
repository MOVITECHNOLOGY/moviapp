import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Folios")

# 2. Credenciales
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 3. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio de la salida (ej: municipio)")

if nro_folio:
    st.info(f"Buscando productos del folio: {nro_folio}...")
    
    # URL para ver todos los movimientos de inventario
    url = "https://api.boxhero.io/v1/transactions"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json()
            
            # Buscamos la transacción que tenga tu folio en la nota o referencia
            encontrado = None
            for m in movimientos:
                nota = str(m.get('note', '')).lower()
                ref = str(m.get('reference', '')).lower()
                if nro_folio.lower() in nota or nro_folio.lower() in ref:
                    encontrado = m
                    break
            
            if encontrado:
                st.success(f"✅ Folio Localizado")
                st.write("### Lista de productos a validar:")
                
                # Mostramos los productos que guardaste en esa salida
                for p in encontrado.get('items', []):
                    # Creamos un formato de lista con check
                    st.write(f"⬜ *{p.get('name')}* | Cantidad: {p.get('quantity')}")
                
                st.divider()
                st.subheader("Paso 2: Escanea para confirmar")
                confirmar = st.text_input("Escanea el código de barras del producto físico")
                if confirmar:
                    st.warning("Verificando producto...")
            else:
                st.error("❌ No existe ninguna salida con ese folio en BoxHero.")
        else:
            st.error(f"Error de conexión (Código {response.status_code}). Revisa tu TOKEN.")
            
    except Exception as e:
        st.error(f"Error inesperado: {e}")
