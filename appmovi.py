import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Folios")

# 2. Credenciales (Token confirmado)
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 3. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio de la salida (ej: municipio)")

if nro_folio:
    st.info(f"Buscando productos del folio: {nro_folio}...")
    
    # URL estándar de transacciones
    url = "https://api.boxhero.io/v1/transactions"
    
    try:
        # Pedimos los últimos movimientos
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json()
            
            # Buscamos 'municipio' en el historial
            encontrado = None
            for m in movimientos:
                # Revisamos Nota, Referencia o ID
                texto_busqueda = (str(m.get('note', '')) + str(m.get('reference', ''))).lower()
                if nro_folio.lower() in texto_busqueda:
                    encontrado = m
                    break
            
            if encontrado:
                st.success(f"✅ Folio Localizado")
                st.write("### Lista de productos cargados:")
                
                # Mostramos los productos de esa salida
                for item in encontrado.get('items', []):
                    nombre = item.get('name', 'Producto sin nombre')
                    cant = item.get('quantity', 0)
                    st.write(f"⬜ *{nombre}* | Cantidad: {cant}")
                
                st.divider()
                st.subheader("Paso 2: Validación física")
                st.text_input("Escanea el producto para marcar check")
            else:
                st.warning(f"⚠️ No encontré '{nro_folio}' en las salidas recientes. Verifica que esté escrito igual en BoxHero.")
        else:
            st.error(f"Error {response.status_code}: Revisa los permisos de tu API en BoxHero.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")

