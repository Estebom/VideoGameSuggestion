#Esteban Rodriguez
#11/15/2023

#imports
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import pandas as pd
import os

#Setting up title
st.title("Video Game Suggestions")

#Setting up llm parameters and agent
llm = OpenAI(temperature=0.9, streaming=True)
tools = load_tools(['ddg-search'])
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

#options for each option 
df = pd.DataFrame({
    'Genre' : ['Select a Genre', 'RPG', 'Shooter', 'Adventure', 'Story'],
    'Players' : ['Select Player Choice', 'Single-Player', 'Multiplayer', 'Co-op', 'MMO'],
    'Price' : ['Select a Price Option', 'Live-Service', 'Free-to-Play', 'Pay Once', 'Micro-Transactions']
})

#selectboxes for game categories
option_1 = st.selectbox('Pick your Genre', df['Genre'], index=0)
option_2 = st.selectbox('Pick your player choice', df['Players'], index=0)
option_3 = st.selectbox('Pick your price', df['Price'], index=0)

#text box for extra details
prompt = st.text_input("Please add any extra details for the games you like:")

#hit submit once ready
if st.button('Submit'):
    if option_1 != 'Select a Genre' and option_2 != 'Select Player Choice' and option_3 != 'Select a Price Option':
        with st.container():
            st_callback = StreamlitCallbackHandler(st.container())
            #prompt passed into llm and duckduckgo as well as formating for output
            response = agent.run(llm.invoke(f"Please recommend 5 games that align with these features: "
                                f"Genre: {option_1}, "
                                f"Players that can play: {option_2}, "
                                f"Price of game: {option_3}. "
                                f"If they meet any of these additional details requests: '{prompt}'. "
                                f"Please give a summary of what each game is and what the gameplay is like."),
                     callbacks=[st_callback])
            st.write(response)
    #Case if categories are not picked
    else:
        st.error("Please make a selection in all categories.")