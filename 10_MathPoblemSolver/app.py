import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from dotenv import load_dotenv
from langchain.callbacks import StreamlitCallbackHandler


# Set up the streamlit app
st.set_page_config(page_title="Text to math problem solver and Data Search Assistant")
st.title("Text to Math Problem Solver using Google Gemma 2")

groq_api_key  = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key yo continue")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the internet to find the various info on the topics mentioned"
)


# Initialize the Math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answeing math related questions. Only mathematical expression to be provided"
)

prompt = """
You are a agent taked for solving users mathematical questions. 
Logically arrive at the solutions and provide a detailed explanation and display it point wise for the question below.
Question: {question}
Answer: 
"""

prompt_template = PromptTemplate(
    input_variables=["questions"],
    template=prompt
)

# Combine all the tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answeing logic-based and reasoning questions."
)

# Initialize the agents
assistnat_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm Math chatbot who can answer all your Maths questions"}
    ]

for mesg in st.session_state.messages:
    st.chat_message(mesg["role"]).write(mesg["content"])


# Lets start the interaction
question = st.text_area("Enter your question: ", "What 7 plus 9?")
if st.button("Find my answer"):
    if question:
        with st.spinner("Generate response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistnat_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write('### Response: ')
            st.success(response)
    else:
        st.warning("Please enter the question")
