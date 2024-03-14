import os
import streamlit as st
from streamlit_float import *
from streamlit_feedback import streamlit_feedback
from streamlit_theme import st_theme
from streamlit_extras.stylable_container import stylable_container

import toml
#======================================================================================================================================
def create_index():
    chroma_client = chromadb.PersistentClient(path = db_path)
    
    collection = chroma_client.get_or_create_collection(name = colection_name)
    service_context = ServiceContext.from_defaults(embed_model = embed_model,
                                                   llm = llm,
                                                   chunk_size = 128, chunk_overlap = 50)
    
    vector_store = ChromaVectorStore(chroma_collection = collection )
    storage_context = StorageContext.from_defaults(vector_store = vector_store)
    
    index = VectorStoreIndex.from_vector_store( vector_store = vector_store,
                                                storage_context = storage_context,
                                                service_context = service_context
                                              )

    return index
#======================================================================================================================================
def initialize_session_state():
    
    if "chats" not in st.session_state:
        st.session_state.chats = []
        st.session_state.chat_number = 0
        
    if "history" not in st.session_state:
        st.session_state.history = []
   
    if "conversation" not in st.session_state:
        #*** ============================================================= ***
        # Add chat engine here
        #*** ============================================================= ***
        #llm = OpenAI(
        #    temperature=0,
        #    openai_api_key=st.secrets["openai_api_key"],
        #    model_name="text-davinci-003"
        #)
        #st.session_state.conversation = ConversationChain(
        #    llm=llm,
        #    memory=ConversationSummaryMemory(llm=llm),
        #)
        st.session_state.conversation = None
        pass

    if "feedback" not in st.session_state:
        st.session_state["feedback"] = None
        
    if len(st.session_state.history) == 0:
        st.session_state.history.append(
            {"role": "ai", "content": "Faz-me uma pergunta sobre IA e o mercado de trabalho portugues"}    
        )

def on_click_callback():
    if st.session_state.human_prompt == None:
        human_prompt = st.session_state.question_prompt
    else:
        human_prompt = st.session_state.human_prompt
    
    
    #llm_response = st.session_state.conversation.run(
    #    human_prompt
    #)

    llm_response = "Resposta Aqui!"
    st.session_state.history.append(
        {"role": "human", "content": human_prompt}
    )
    st.session_state.history.append(
        {"role": "ai", "content": llm_response}
    )

    st.session_state.chats[st.session_state.chat_number] = st.session_state.history

def question_click(*args):
    chat = ""
    for val in args:
        question += val

    st.write(chat)
    #st.session_state.question_prompt = question
    #on_click_callback()

def new_chat():

    st.session_state.chats[st.session_state.chat_number] = st.session_state.history
    
    st.session_state.chat_number = len(st.session_state.chats)
    st.session_state.history = []
        

#======================================================================================================================================
def main():
        
    initialize_session_state()   
    with open("./style.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

    #================================================================================================================================================================================================
    #=== Header
    container_header = st.container()
    with container_header: 
        div = """
          <div style="display: flex; align-items: center; justify-content: flex-end; width: 100%; height: 17vw;">
              <a href="https://www.randstad.pt/randstad-research/o-impacto-da-ia-no-mercado-portugues/" target="_blank">
                  <img src="https://storage.googleapis.com/gc-poc-cnn-ai-dev/sandbox-experimentation-gsaraiva/Randstad/RANDSTAD_programa%20(1).png" style="width: 100%; aspect-ratio: 6 / 1;">
              </a>
          </div>
          """
        st.markdown(div, unsafe_allow_html=True)
    #================================================================================================================================================================================================
    # Divide in two columns
    col1, col2 = st.columns([1, 4])

    # First column -> Questions
    with col1:
              
        st.header("Chats")
        st.button(    "New Chat",
                      on_click = question_click,
                      args = (first_message)
                 )
        # create a container for each chat
        container_chats = st.container(height = 300)
        
        with container_chats:
            for chat in st.session_state.chats:

                if chat[0]["role"] == "human":
                    first_message = chat[0]["content"]
                else:
                    first_message = chat[1]["content"]
                
                st.button(first_message,
                          on_click = question_click,
                          args = (first_message)
                         )
                st.divider()
    
    with col2:
        
        chat_placeholder = st.container(height = 300, border = True)
        prompt_placeholder = st.container()
        container_devoteam = st.container()
    
        
        
        with chat_placeholder:
            for chat in st.session_state.history:
                div = f"""
                            <div class="chat-row 
                                {'' if chat["role"] == 'ai' else 'row-reverse'}">
                                <img class="chat-icon" src="{
                                    'https://storage.googleapis.com/gc-poc-cnn-ai-dev/sandbox-experimentation-gsaraiva/Randstad/Randstad%20logo_stacked_color.png' if chat["role"] == 'ai' 
                                                  else 'https://cdn-icons-png.freepik.com/512/8428/8428718.png'}"
                                     width=40 height=40>
                                <div class="chat-bubble
                                {'ai-bubble' if chat["role"] == 'ai' else 'human-bubble'}">
                                    &#8203;{chat["content"]}
                                </div>
                            </div>
                    """
                st.markdown(div, unsafe_allow_html=True)
            
            for _ in range(3):
                st.markdown("")
        
        with prompt_placeholder:
            st.chat_input(
                "Chat Here!",
                on_submit = on_click_callback,
                key="human_prompt",
            )
            
        with container_devoteam:
            div = """
          <div style="display: flex; align-items: center; justify-content: flex-end; height: 70px;">
              <span style="color: #3c3c3a; margin-right: 0px; font-size: 2vh; font-weight: bold;">Powered by</span>
              <a href="https://pt.devoteam.com/pt-pt/" target="_blank">
                  <img src="https://storage.googleapis.com/gc-poc-cnn-ai-dev/sandbox-experimentation-gsaraiva/Randstad/Copy%20of%20devoteam_rgb.png" style="height: 60px;">
              </a>
          </div>
          """
            st.markdown(div, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
