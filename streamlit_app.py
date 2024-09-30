import streamlit as st
import requests
import json

# Mostrar título y descripción.
st.title("💬 Chatbot Grupo Revoredo")
st.write(
    "This is a simple chatbot that uses AWS cloud computing model to generate responses. "
    "To use this app, you need to provide a key"
)

lambda_url = "https://9h14dzfc80.execute-api.us-east-1.amazonaws.com/dev/query"
token =  st.text_input("Token", type="password")


if not token:
    st.info("Por favor, ingresa el token de respuesta para continuar.", icon="🗝️")
else:
    # Crear una variable de estado de sesión para almacenar los mensajes.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes existentes.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Crear el campo de entrada para permitir al usuario escribir un mensaje.
    prompt = st.chat_input("Escribe tu mensaje:")

    if prompt:
        # Almacenar y mostrar el mensaje del usuario.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Enviar la solicitud a la Lambda Function URL.
        try:
            response = requests.post(lambda_url, json={
                "prompt": prompt,
                "token": token
                })
            response.raise_for_status()  # Verificar si la solicitud fue exitosa
            response_data = response.json()['body']
            response_data = json.loads(response_data)
            print(response_data)
            # Verificar si la respuesta tiene el campo 'response'
            lambda_response = response_data.get("generation", "No se recibió una respuesta válida de Lambda.")

            # Mostrar la respuesta de la Lambda en el chat.
            with st.chat_message("assistant"):
                st.markdown(lambda_response)
            st.session_state.messages.append({"role": "assistant", "content": lambda_response})

        except requests.exceptions.RequestException as e:
            st.error(f"Error al llamar a la Lambda: {e}")
