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
    
    # URL UNIVERSAL para historial de movimientos en BoxHero
    url = "https://api.boxhero.io/v1/history"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            movimientos = response.json()
            
            # Buscamos 'municipio' en las notas o referencias
            encontrado = None
            for m in movimientos:
                # Revisamos nota y referencia
                contenido = (str(m.get('note', '')) + str(m.get('reference', ''))).lower()
                if nro_folio.lower() in contenido:
                    encontrado = m
                    break
            
            if encontrado:
                st.success(f"✅ Folio Localizado")
                st.write(f"*Fecha:* {encontrado.get('created_at')[:10]}")
                st.write("### Productos que deben venir:")
                
                # Listamos los productos de esa salida
                for item in encontrado.get('items', []):
                    # Buscamos el nombre del producto
                    nombre = item.get('name', 'Producto')
                    cantidad = item.get('quantity', 0)
                    st.write(f"⬜ *{nombre}* | Cantidad: {cantidad}")
                
                st.divider()
                st.subheader("Paso 2: Validación")
                st.text_input("Escanea el producto físico para marcarlo")
            else:
                st.warning(f"⚠️ No encontré '{nro_folio}' en las salidas recientes. Revisa que esté escrito igual en BoxHero.")
        
        # SI DA 404, INTENTAMOS LA RUTA ALTERNA AUTOMÁTICAMENTE
        elif response.status_code == 404:
            url_alt = "https://api.boxhero.io/v1/transactions"
            res_alt = requests.get(url_alt, headers=HEADERS)
            if res_alt.status_code == 200:
                st.write("Conectado por ruta alterna...")
                # (Repetir lógica de búsqueda aquí si es necesario)
            else:
                st.error("❌ Error 404: BoxHero no reconoce la dirección. Contacta a soporte de API.")
        else:
            st.error(f"Error {response.status_code}: Revisa los permisos de tu TOKEN.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
