# EL ARCHIVO SE CORRE CON python -m streamlit run main.py
import streamlit as st 
from groq import Groq

st.set_page_config(page_title="Chat con IA", page_icon="👺")

st.title("Chatbot con Groq")
nombre = st.text_input("¿Cuál es tu nombre?") 

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Gracias por usar esta aplicación")

def configuracionPagina():
    st.sidebar.title("Configuración de la IA")
    modelos=['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
    seleccionarModelo=st.sidebar.selectbox(
        "Elegí un Modelo", options=modelos, index=0
        )
    return seleccionarModelo

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
      model=modelo,
      messages=[{"role": "user", "content": mensajeDeEntrada}],
      stream=True
)

def crearusuariogroq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar" : avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : 
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat : mostrar_historial()

def generar_respuestas(chat_completo):
    respuesta_completa = "" 
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa 

if nombre!="":
    st.title(f"¡Bienvenido  {nombre}!")
else:
    st.title("¡Bienvenido!")

def main(): 
    modelo=configuracionPagina()
    clienteUsuario = crearusuariogroq()
    inicializar_estado() 
    area_chat() 
    mensaje = st.chat_input("Escribí tu mensaje...")
    if mensaje:
        actualizar_historial("user", mensaje, "👩‍🏫")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant") :
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
            st.rerun()
                
if __name__ == "__main__":
    main()