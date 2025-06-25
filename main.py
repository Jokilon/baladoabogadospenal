import streamlit as st
from datetime import datetime, timedelta
import locale

# Idioma español para fechas
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
except:
    pass

st.set_page_config(page_title="Calculadora de beneficios penitenciarios")

st.title('Calculadora de Beneficios Penitenciarios')

modo = st.radio("¿Cómo querés calcular?", ["Conozco la fecha de detención", "No conozco la fecha exacta (solo el tiempo detenido)"])

# Ingreso de datos
if modo == "Conozco la fecha de detención":
    fecha_detencion = st.date_input('Fecha de detención', format='DD/MM/YYYY')
    tiempo_detencion = None
else:
    fecha_detencion = None
    col1, col2 = st.columns(2)
    with col1:
        años_det = st.number_input("Años detenido", min_value=0, max_value=50, value=0)
    with col2:
        meses_det = st.number_input("Meses detenido", min_value=0, max_value=11, value=0)
    tiempo_detencion = (años_det * 12 + meses_det) * 30.4375

# Condena total
col1, col2 = st.columns(2)
with col1:
    anios = st.number_input('Años de condena', min_value=0, max_value=50, value=0)
with col2:
    meses = st.number_input('Meses de condena', min_value=0, max_value=11, value=0)

# Cálculo de días de condena
meses_totales = anios * 12 + meses
dias_totales = meses_totales * 30.4375

# Beneficios
beneficios = {
    "Salidas transitorias": dias_totales * 0.5,
    "Libertad condicional": dias_totales * (2 / 3),
    "Libertad asistida (Nacional)": dias_totales - 180,
    "Libertad asistida (PBA - 6 meses antes de los 2/3)": (dias_totales * (2 / 3)) - 180
}

def format_fecha(f):
    return f.strftime('%d/%m/%Y')

def calcular_mensaje(nombre_beneficio, dias_necesarios):
    hoy = datetime.now().date()
    if fecha_detencion:
        fecha_estim = fecha_detencion + timedelta(days=dias_necesarios)
        if fecha_estim <= hoy:
            return f'Ya podrías tener {nombre_beneficio}. (Fecha estimada: {format_fecha(fecha_estim)})', 'success'
        else:
            delta = fecha_estim - hoy
    elif tiempo_detencion is not None:
        dias_faltan = dias_necesarios - tiempo_detencion
        if dias_faltan <= 0:
            return f'Ya podrías tener {nombre_beneficio}.', 'success'
        else:
            delta = timedelta(days=dias_faltan)
    else:
        return None, None
    years, rem = divmod(delta.days, 365)
    months, rem = divmod(rem, 30)
    days = rem
    return f'Faltan {years} años, {months} meses y {days} días para {nombre_beneficio}.', 'error'

# Mostrar resultados
if dias_totales == 0:
    st.warning("Ingresá los años y meses de condena.")
else:
    st.subheader("Resultados:")
    for nombre, dias in beneficios.items():
        mensaje, tipo = calcular_mensaje(nombre, dias)
        st.markdown(f'**{nombre}:**')
        if mensaje:
            if tipo == 'success':
                st.success(mensaje)
            elif tipo == 'error':
                st.error(mensaje)
            else:
                st.info(mensaje)
        else:
            st.warning("Faltan datos para calcular este beneficio.")

    # 🟡 Nota aclaratoria
    st.markdown("---")
    st.info("**S.E.U.O:** Los resultados son estimativos y podrían aplicar otros beneficios según el caso particular. No deje de asesorarse con su abogado especialista en derecho penal de su confianza.")

    # 🟢 Botón de WhatsApp
    numero = "5493364249566"  # Reemplazá con tu número si es otro
    mensaje = "Hola, quiero recibir asesoramiento legal sobre beneficios penitenciarios."
    url = f"https://api.whatsapp.com/send?phone={numero}&text={mensaje}"
    st.markdown(f"""
        <a href="{url}" target="_blank">
            <button style="background-color:#25D366;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                📲 Recibir asesoramiento legal por WhatsApp
            </button>
        </a>
        """, unsafe_allow_html=True)

    # 🖨️ Botón para imprimir
    st.markdown("""
        <br>
        <button onclick="window.print()" style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
            🖨️ Imprimir resultados
        </button>
        """, unsafe_allow_html=True)

    # 🔗 Compartir en redes
    st.markdown("""
        <br><b>Compartir:</b><br>
        <a href="https://www.facebook.com/sharer/sharer.php?u=https://baladoabogadospenal.streamlit.app" target="_blank">📘 Facebook</a> |
        <a href="https://twitter.com/intent/tweet?url=https://baladoabogadospenal.streamlit.app" target="_blank">🐦 Twitter</a> |
        <a href="https://api.whatsapp.com/send?text=https://baladoabogadospenal.streamlit.app" target="_blank">📲 WhatsApp</a>
        """, unsafe_allow_html=True)
