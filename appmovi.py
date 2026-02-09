import streamlit as st
import requests

# Configuración visual de la App
st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador de Inventario")

# 1. Credenciales Actualizadas (Basadas en tu última foto)
TOKEN = "872810ff-7e4b-44f3-a3a9-d437c59e7ddc"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 2. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio (ej: municipio)")

if nro_folio:
    st.info(f"Buscando '{nro_folio}' en movimientos de inventario...")
    
    # RUTA OFICIAL RECOMENDADA POR SOPORTE: /location_txs
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/location_txs"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            transacciones = response.json()
            # Buscamos 'municipio' en el campo de nota de las transacciones
            encontrado = next((t for t in transacciones if nro_folio.lower() in str(t.get('note', '')).lower()), None)
            
            if encontrado:
                st.success("✅ Movimiento Localizado")
                st.write(f"*Fecha:* {encontrado.get('created_at')[:10]}")
                
                # Listamos los productos que salieron (ej: Guantes)
                st.write("### Productos en esta salida:")
                items = encontrado.get('items', [])
                if items:
                    for p in items:
                        st.write(f"⬜ *{p.get('name')}* | Cantidad: {p.get('quantity')}")
                        st.caption(f"Código: {p.get('barcode')}")
                else:
                    st.warning("No se encontraron productos dentro de este folio.")
                
                st.divider()
                st.subheader("Paso 2: Validación Física")
                st.text_input("Escanea el producto para confirmar")
            else:
                st.warning(f"No encontré el folio '{nro_folio}' en las transacciones recientes.")
        elif response.status_code == 404:
            st.error("Error 404: La dirección /location_txs no fue encontrada. Revisa con soporte si tu plan incluye esta API.")
        else:
            st.error(f"Error {response.status_code}: El token nuevo no tiene permiso de acceso.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
