import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Ventas")

# 1. Datos Maestros (Sacados de tu foto)
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
TEAM_ID = "314955" 
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 2. Entrada del Folio
nro_folio = st.text_input("Ingresa el nombre del Folio (ej: MUNICIPIO)")

if nro_folio:
    st.info(f"Buscando Orden de Venta: {nro_folio}...")
    
    # URL específica para Órdenes de Venta
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/orders"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            ventas = response.json()
            # Buscamos la orden que coincida con el nombre o nota
            orden = next((o for o in ventas if nro_folio.upper() in str(o.get('name', '')).upper() or nro_folio.lower() in str(o.get('note', '')).lower()), None)
            
            if orden:
                st.success(f"✅ Orden Encontrada: {orden.get('name')}")
                st.write(f"*Estado:* {orden.get('status_text')}")
                st.write("### Productos en esta orden:")
                
                # Para ver los productos de una orden, a veces hay que consultar el detalle
                order_id = orden.get('id')
                url_det = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/orders/{order_id}"
                res_det = requests.get(url_det, headers=HEADERS)
                
                if res_det.status_code == 200:
                    detalles = res_det.json()
                    for item in detalles.get('items', []):
                        st.write(f"⬜ *{item.get('name')}* | Cantidad: {item.get('quantity')}")
                        st.caption(f"Código: {item.get('barcode')}")
                
                st.divider()
                st.subheader("Paso 2: Escanea para validar")
                st.text_input("Escanea el producto físico")
            else:
                st.warning(f"⚠️ No encontré la orden '{nro_folio}'. Revisa que esté en 'Ventas'.")
        else:
            st.error(f"Error {response.status_code}. Verifica los permisos de Ventas en tu API.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
