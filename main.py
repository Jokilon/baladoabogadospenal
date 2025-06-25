import streamlit as st
from datetime import datetime, timedelta
import locale

# Intentar usar el calendario en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
except:
    pass

st.set_page_config(page_title="Calculadora de beneficios penitenciarios")

st.title('Calculadora de Beneficios Penitenciarios')

modo = st.radio("¿Cómo querés calcular?", ["Conozco la fecha de detención", "No conozco la fecha exacta (solo el tiempo detenido)"])

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
    tiempo_detencion = (años_det * 12 + meses_det) * 30.4375  # más preciso

col1, col2 = st.columns(2)
with col1:
    anios = st.number_input('Años de condena', min_value=0, max_value=50, value=0)
with col2:
    meses = st.number_input('Meses de condena', min_value=0, max_value=11, value=0)

# Cálculo de días totales de condena
meses_totales = anios * 12 + meses
dias_totales = meses_totales * 30.4375  # promedio mensual

# Porcentajes y beneficios
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

if dias_totales == 0:
    st.warnin
