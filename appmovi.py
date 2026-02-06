import streamlit as st
import requests

# 1. Configuración de la página
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Folios")

# 2. Credenciales (Token confirmado en tu foto)
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 3. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio de la salida (ej: municipio)")

if nro_folio:
    st.info(f"Buscando productos del folio: {nro_folio}...")
    
    # URL OFICIAL de BoxHero para historial
    url = "https://api.boxhero.io/v1/history"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json()
            
            # Buscamos 'municipio' en las notas o referencias
            encontrado = None
            for m in movimientos:
                # Combinamos nota y referencia para buscar
                info_transaccion = (str(m.get('note', '')) + str(m.get('reference', ''))).lower()
                if nro_folio.lower() in info_transaccion:
                    encontrado = m
                    break
            
            if encontrado:
                st.success(f"✅ Folio Localizado")
                st.write(f"*Fecha:* {encontrado.get('created_at')[:10]}")
                st.write("### Productos a validar:")
                
                # Mostramos los productos de esa salida específica
                for item in encontrado.get('items', []):
                    st.write(f"⬜ *{item.get('name')}* | Cantidad: {item.get('quantity')}")
                
                st.divider()
                st.subheader("Paso 2: Escaneo de verificación")
                st.text_input("Escanea el producto para marcar")
            else:
                st.warning(f"⚠️ No encontré el folio '{nro_folio}' en las salidas recientes.")
        else:
            st.error(f"Error {response.status_code}: La dirección de BoxHero falló. Probaremos otra ruta si esto sigue.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
