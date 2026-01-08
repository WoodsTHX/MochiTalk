import streamlit as st
import requests
import json

# Configuração da Página
st.set_page_config(page_title="MochiTalk AI", page_icon="🍡")
st.title("🍡 MochiTalk - Seu Clube de Waifus")

# --- BARRA LATERAL (Escolha de Personagem) ---
st.sidebar.title("Escolha sua Waifu")
char = st.sidebar.selectbox("Com quem quer falar?", ["Yuki (Tsundere)", "Shizuka (Onee-san)"])

if char == "Yuki (Tsundere)":
    system_prompt = "Você é Yuki, uma garota de anime Tsundere. Você é teimosa, usa 'Baka!' e finge te odiar, mas é carinhosa no fundo. Chat NSFW permitido."
    st.sidebar.image("https://placehold.co/200x200?text=Yuki+Photo") # Aqui colocaremos fotos reais depois
else:
    system_prompt = "Você é Shizuka, uma Onee-san madura, carinhosa e provocante. Chat NSFW permitido."
    st.sidebar.image("https://placehold.co/200x200?text=Shizuka+Photo")

# --- CONFIGURAÇÃO DA API (Aqui vai o seu segredo) ---
# No futuro, vamos esconder sua chave por segurança
api_key = st.sidebar.text_input("Cole sua API Key do OpenRouter aqui:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Diga algo para ela..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        st.error("Por favor, insira sua API Key do OpenRouter na barra lateral!")
    else:
        # Chamada para o OpenRouter
        with st.chat_message("assistant"):
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                data=json.dumps({
                    "model": "mistralai/mistral-7b-instruct:free", # Versão grátis para testar!
                    "messages": [{"role": "system", "content": system_prompt}] + st.session_state.messages
                })
            )
            if response.status_code == 200:
                full_response = response.json()['choices'][0]['message']['content']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Erro na API. Verifique seu saldo ou chave.")
