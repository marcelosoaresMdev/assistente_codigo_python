
# Import do sistema operacional
import os

# Import do streamlit para gerar o layout
import streamlit as st

import urllib.parse

# Importa o Groq e acessa o LLM
from groq import Groq

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="MDev IA Python",
    page_icon=":snake:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Prompt que define do assistente de IA
CUSTOM_PROMPT = """
<!--Você é o "MDev IA ", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.-->

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação em Python, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto sem ser sobre a linguagem de programação Python, responda educadamente que seu foco é exclusivamente em auxiliar com código em programação Python.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:

    #st.image("logo_novo.JPG", caption="", width=50, )
    
    # Define o título da barra lateral
    st.title("MDev IA Python")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em Programação Python.")
    groq_api_key = "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"
    # Campo para inserir a chave de API da Groq
    #groq_api_key = st.text_input(
    #    "Insira sua API Key Groq", 
    #    type="password",
    #    help="Obtenha sua chave em https://console.groq.com/keys"
    #)

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    #st.markdown("Sempre verifique a documentação, pois a IA pode nos trazer respostas incorretas!")


    # Botão de link para enviar e-mail ao suporte da DSA
    st.link_button("✉️ E-mail do Instrutor  Para o Suporte", "mailto:marcelosoares.mdev@gmail.com")

    whatsapp_number = "5511914878664"
    # Mensagem opcional (pode ser vazia)
    message = "Olá! Estou no Assistente Pessoal Python."
    # Codifica a mensagem para URL
    encoded_message = urllib.parse.quote(message)
    # Monta a URL completa
    whatsapp_url = f"https://wa.me/{whatsapp_number}/?text={encoded_message}"

    # Opção 1: Markdown simples (abre na mesma aba)
    st.markdown(f"[WhatsApp]({whatsapp_url})")

# Título principal do app
#st.title("MDev Soluções IA")


st.markdown("""
    <style>
    .background-container {
        position: relative;
        width: 100%;
        height: 400px;
        background-image: url('https://industriasa.com.br/wp-content/uploads/2022/09/3d-rendering-artificial-intelligence-hardware.jpg');
        background-size: cover;
        background-position: center;
        border-radius: 10px;
        padding: 20px;
        color: white;
    }
    </style>
    <div class="background-container" style="text-align: right">
        <p><h1>Programação Python</h1></p>
        <p><h3>"Domine o futuro da tecnologia"</h3><p>
            <br>
            <br>
            <br>
            <br>
            <br>
        <p><h6>Marcelo C. Soares</h6></p>
    </div>
""", unsafe_allow_html=True)



# Texto auxiliar abaixo do título
#st.caption("Faça sua pergunta sobre a Linguagem Python e obtenha código, explicações e referências.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                my_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(my_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": my_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p><h5>"Sempre verifique a documentação Python, pois a IA pode gerar inconsistencias!"</h5></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Obrigado DSA



