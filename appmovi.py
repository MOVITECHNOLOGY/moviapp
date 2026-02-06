import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Folios")

# 1. Llaves de acceso
TOKEN = "7af32261-1ee8-4d53-b1b5-77afb233d446"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 2. Entrada de Folio
nro_folio = st.text_input("Ingresa el Folio de la salida (ej: FOLIO-001)")

if nro_folio:
    st.info(f"Buscando productos asociados al folio: {nro_folio}...")
    
    # URL para buscar en el historial de transacciones
    url_transacciones = "https://api.boxhero.io/v1/transactions"
    
    try:
        # Buscamos transacciones que coincidan con el folio
        res = requests.get(url_transacciones, headers=HEADERS)
        if res.status_code == 200:
            movimientos = res.json()
            # Filtramos por el folio que escribiste en la nota o referencia
            transaccion = next((t for t in movimientos if nro_folio in str(t.get('note', '')) or nro_folio in str(t.get('reference', ''))), None)
            
            if transaccion:
                st.success(f"✅ Folio encontrado. Fecha: {transaccion.get('created_at')[:10]}")
                
                # Listamos los productos que salieron en ese movimiento
                st.write("### Productos que deben venir:")
                for item in transaccion.get('items', []):
                    st.write(f"* *{item.get('name')}* - Cantidad: {item.get('quantity')}")
                
                st.divider()
                st.subheader("Ahora escanea para validar:")
                scan = st.text_input("Escanea producto físico")
                if scan:
                    st.warning("Validando contra la lista...")
            else:
                st.error("❌ No encontramos ninguna salida con ese folio en BoxHero.")
        else:
            st.error("Error al conectar con el historial. Revisa el TOKEN.")
    except Exception as e:
        st.error(f"Error: {e}")

