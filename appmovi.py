import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Devoluciones Automáticas", page_icon="🚀")
st.title("🚀 MOVI: Registro Real en BoxHero")

# Datos de tu cuenta confirmados
TOKEN = "5f705115-b965-45a9-baa5-519af2667a7b" 
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

barcode = st.text_input("Escanea el Código para DEVOLUCIÓN")

if barcode:
    # 1. Primero intentamos identificar el producto para que veas qué es
    url_ver = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/products/{barcode}"
    res_ver = requests.get(url_ver, headers={"Authorization": f"Bearer {TOKEN}"})
    
    if res_ver.status_code == 200:
        p = res_ver.json()
        st.info(f"Producto: *{p.get('name')}* | Stock actual: {p.get('quantity')}")
        
        cantidad = st.number_input("Cantidad a devolver", min_value=1, value=1)
        
        if st.button("CONFIRMAR DEVOLUCIÓN EN BOXHERO"):
            # 2. RUTA DE GOOGLE: Registro de entrada (Stock-In)
            url_in = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/stock-in"
            
            # Datos que pide la API de BoxHero
            payload = {
                "items": [
                    {
                        "barcode": barcode,
                        "quantity": cantidad
                    }
                ],
                "note": "Devolución automática desde App MOVI"
            }
            
            response = requests.post(url_in, headers=HEADERS, json=payload)
            
            if response.status_code == 200 or response.status_code == 201:
                st.success(f"✅ ¡ÉXITO! Se sumaron {cantidad} unidad(es) a BoxHero.")
                st.balloons()
            else:
                st.error(f"Error {response.status_code}: No se pudo actualizar el stock.")
                st.write(response.json()) # Para ver qué permiso falta exactamente
    else:
        st.warning("No puedo leer el nombre, pero intenta la devolución directa:")
        if st.button("FORZAR DEVOLUCIÓN"):
            # Intento de envío directo sin lectura previa
            url_in = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/stock-in"
            payload = {"items": [{"barcode": barcode, "quantity": 1}], "note": "Devolución Forzada"}
            res_f = requests.post(url_in, headers=HEADERS, json=payload)
            if res_f.status_code == 200:
                st.success("✅ ¡Logrado! Stock actualizado en BoxHero.")
            else:
                st.error("Definitivamente el Token está bloqueado para escritura.")
