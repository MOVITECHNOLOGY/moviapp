import streamlit as st
import requests

st.set_page_config(page_title="MOVI - Validador", page_icon="📦")
st.title("📦 MOVI: Verificador Total")

# 1. Credenciales Confirmadas
TOKEN = "872810ff-7e4b-44f3-a3a9-d437c59e7ddc"
TEAM_ID = "314955"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 2. Entrada del Folio
nro_folio = st.text_input("Ingresa el Folio (ej: municipio)")

if nro_folio:
    st.info(f"Buscando '{nro_folio}' en el historial...")
    
    # RUTA ALTERNATIVA: Historial de eventos (suele estar abierto por defecto)
    url = f"https://api.boxhero.io/v1/teams/{TEAM_ID}/history-events"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            datos = response.json()
            # BoxHero a veces devuelve una lista o un dict con una llave 'list'
            movimientos = datos.get('list', []) if isinstance(datos, dict) else datos
            
            # Buscamos 'municipio' en el campo 'note' o 'description'
            encontrado = None
            for m in movimientos:
                # Revisamos nota, referencia o descripción
                texto_mov = (str(m.get('note', '')) + str(m.get('description', ''))).lower()
                if nro_folio.lower() in texto_mov:
                    encontrado = m
                    break
            
            if encontrado:
                st.success("✅ ¡Folio localizado!")
                st.write(f"*Fecha del movimiento:* {encontrado.get('created_at')[:10]}")
                
                # Intentamos sacar los productos
                st.write("### Productos que salieron:")
                items = encontrado.get('items', [])
                
                if items:
                    for p in items:
                        st.write(f"⬜ *{p.get('name')}* | Cantidad: {p.get('quantity')}")
                else:
                    st.warning("El folio existe, pero no pude leer los productos. Revisa si la salida está 'Confirmada'.")
                
                st.divider()
                st.subheader("Validación física")
                st.text_input("Escanea código para verificar")
            else:
                st.warning(f"No encontré el folio '{nro_folio}' en los movimientos recientes.")
        else:
            st.error(f"Error {response.status_code}. El Token sigue restringido.")
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
