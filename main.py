import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Calculadora de beneficios penitenciarios")

st.title("Calculadora de beneficios penitenciarios")

st.write("Calculá salidas transitorias, libertad condicional y libertad asistida según la fecha de detención y duración de la condena.")

# Selección: ¿Conoce la fecha de detención?
conoce_fecha = st.radio("¿Conocés la fecha de detención?", ("Sí", "No"))

fecha_detencion = None
if conoce_fecha == "Sí":
    fecha_detencion = st.date_input("Fecha de detención", value=datetime.today())

# Años y meses de condena
col1, col2 = st.columns(2)
with col1:
    anios = st.number_input("Años de condena", min_value=0, max_value=100, step=1)
with col2:
    meses = st.number_input("Meses de condena", min_value=0, max_value=11, step=1)

# Total de condena en días (aprox. con promedio mensual)
total_dias = (anios * 12 + meses) * 30.4375

# Cálculos de beneficios
dias_salidas_transitorias = total_dias * (2/3)
dias_libertad_condicional = total_dias * (3/4)
dias_libertad_asistida = total_dias - 180  # 6 meses antes del final

def formatear_dias(dias):
    años = int(dias // 365)
    meses = int((dias % 365) // 30)
    dias_restantes = int((dias % 365) % 30)
    return f"{años} años, {meses} meses y {dias_restantes} días"

def sumar_dias(fecha, dias):
    return (fecha + timedelta(days=int(dias))).strftime('%d/%m/%Y')

# Mostrar resultados
st.subheader("Resultados:")

if total_dias == 0:
    st.warning("Ingresá la duración de la condena.")
else:
    if conoce_fecha == "Sí" and fecha_detencion:
        st.markdown("**Salidas transitorias:** faltan " +
                    formatear_dias(dias_salidas_transitorias) +
                    f" _(Fecha estimada: {sumar_dias(fecha_detencion, dias_salidas_transitorias)})_")

        st.markdown("**Libertad condicional:** faltan " +
                    formatear_dias(dias_libertad_condicional) +
                    f" _(Fecha estimada: {sumar_dias(fecha_detencion, dias_libertad_condicional)})_")

        st.markdown("**Libertad asistida:** faltan " +
                    formatear_dias(dias_libertad_asistida) +
                    f" _(Fecha estimada: {sumar_dias(fecha_detencion, dias_libertad_asistida)})_")
    else:
        st.markdown(f"**Salidas transitorias:** luego de {formatear_dias(dias_salidas_transitorias)}")
        st.markdown(f"**Libertad condicional:** luego de {formatear_dias(dias_libertad_condicional)}")
        st.markdown(f"**Libertad asistida:** luego de {formatear_dias(dias_libertad_asistida)}")
