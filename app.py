import streamlit as st

st.set_page_config(page_title="Interpretador de Hemograma - Vet", page_icon="🐾", layout="centered")

st.title("🐾 Doggy Center - Interpretador de Hemograma")
st.write("Herramienta interactiva de apoyo diagnóstico para la práctica clínica veterinaria.")

# 1. Datos Generales del Paciente
st.sidebar.header("Datos del Paciente")
especie = st.sidebar.selectbox("Especie", ["Canino", "Felino"])
paciente_nombre = st.sidebar.text_input("Nombre del Paciente", "Ej. Rocky")

st.markdown("---")

# 2. Formulario de Ingreso de Parámetros
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Eritrograma")
    hct = st.number_input("Hematocrito (HCT %)", value=35.0, step=0.1)
    vcm = st.number_input("VCM (fL)", value=71.6, step=0.1)
    retic = st.number_input("Reticulocitos (%)", value=0.1, step=0.01)

with col2:
    st.subheader("Leucograma")
    wbc = st.number_input("Leucocitos Totales (x10³/µL)", value=17.8, step=0.1)
    neutro = st.number_input("Neutrófilos Abs. (x10³/µL)", value=11.2, step=0.1)
    bandas = st.number_input("Bandas Abs. (x10³/µL)", value=0.5, step=0.1)

with col3:
    st.subheader("Trombograma")
    plt = st.number_input("Plaquetas (x10³/µL)", value=153.0, step=1.0)
    proteinas = st.number_input("Proteínas Totales (g/dL)", value=7.2, step=0.1)

st.markdown("---")

# 3. Lógica de Interpretación Automatizada
if st.button("🚀 Interpretar Hemograma"):
    st.subheader(f"📋 Reporte Diagnóstico Preliminar para: {paciente_nombre} ({especie})")
    
    hallazgos = []
    
    # Definición de umbrales según especie
    if especie == "Canino":
        hct_min, hct_max = 37.0, 55.0
        wbc_min, wbc_max = 6.0, 17.0
        neutro_max = 10.0
        plt_min, plt_max = 200.0, 500.0
        retic_limite = 1.5
    else: # Felino
        hct_min, hct_max = 24.0, 45.0
        wbc_min, wbc_max = 5.5, 19.5
        neutro_max = 12.5
        plt_min, plt_max = 300.0, 800.0
        retic_limite = 1.0

    # Evaluación del Eritrograma
    if hct < hct_min:
        if retic > retic_limite:
            hallazgos.append(f"🔴 **Anemia Regenerativa** (Reticulocitos: {retic}%): Sugiere pérdida sanguínea aguda o procesos hemolíticos.")
        else:
            hallazgos.append(f"🔴 **Anemia No Regenerativa** (Reticulocitos: {retic}%): Sugiere enfermedad renal crónica, inflamación crónica o falla medular.")
        
        if vcm < 60:
            hallazgos.append("   ↳ *Índice VCM:* Microcítica (sospechar deficiencia de hierro o pérdida crónica).")
        elif vcm > 77:
            hallazgos.append("   ↳ *Índice VCM:* Macrocítica (típicamente asociada a regeneración).")
        else:
            hallazgos.append("   ↳ *Índice VCM:* Normocítica.")
            
    elif hct > hct_max:
        if proteinas > 7.5:
            hallazgos.append("🔵 **Eritrocitosis con hiperproteinemia:** Altamente compatible con hemoconcentración por deshidratación.")
        else:
            hallazgos.append("🔵 **Eritrocitosis / Policitemia:** Evaluar causas primarias o secundarias.")
    else:
        hallazgos.append("🟢 **Eritrograma:** Valores dentro de los rangos de referencia.")

    # Evaluación del Leucograma
    if wbc > wbc_max:
        hallazgos.append(f"⚪ **Leucocitosis total** ({wbc} x10³/µL): Compatible con inflamación, infección bacteriana o estrés.")
    elif wbc < wbc_min:
        hallazgos.append(f"⚪ **Leucopenia** ({wbc} x10³/µL): Sugiere infección viral severa, sepsis o consumo medular.")
    else:
        hallazgos.append("🟢 **Leucograma total:** Dentro de rangos normales.")

    if neutro > neutro_max:
        hallazgos.append(f"   ↳ **Neutrofilia absoluta** ({neutro} x10³/µL): Inflamación aguda, necrosis o respuesta a corticoides.")
        
    if bandas > 0.3:
        hallazgos.append(f"⚠️ **Desviación a la izquierda** (Bandas: {bandas} x10³/µL): Alerta de consumo tisular acelerado e inflamación severa.")

    # Evaluación del Trombograma
    if plt < plt_min:
        hallazgos.append(f"⚠️ **Trombocitopenia** ({plt} x10³/µL): **¡Atención!** Es obligatorio revisar el extendido de sangre periférica para descartar agregados plaquetarios antes de confirmar patología.")
    elif plt > plt_max:
        hallazgos.append(f"🟡 **Trombocitosis** ({plt} x10³/µL): Reactiva/inflamatoria o secundaria a deficiencia de hierro.")
    else:
        hallazgos.append("🟢 **Trombograma:** Recuento plaquetario normal.")

    # Mostrar resultados en pantalla
    for h in hallazgos:
        st.markdown(f"- {h}")
        
    st.info("💡 **Nota clínica:** Recuerda que el hemograma es una pieza clave pero debe correlacionarse siempre con la exploración física y la anamnesis del paciente en consulta.")
