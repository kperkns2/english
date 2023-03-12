import streamlit as st
import pandas as pd
import openai

first_message = "Hello! I am an AI chat assistant trained to assist high school students. I can help answer your questions, provide guidance, and offer academic support. Just ask me anything, and I will do my best to assist you!"

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('courses.csv')
df['subtopic'] = df['subtopic'].fillna('NA')

# Define the available courses, topics, and subtopics based on the data in the DataFrame
available_courses = df['course'].unique()
available_topics = df['topic'].unique()
available_subtopics = df['subtopic'].unique()

# Create a list to store the chat history
if 'chat_history' not in st.session_state:
  st.session_state['chat_history'] = [{'role': 'assistant', 'content': first_message}]

# Create a function to add messages to the chat history
def add_to_chat_history(sender, message):
    st.session_state['chat_history'].append({'role': sender, 'content': message})

def create_sidebar():
  st.sidebar.header('Course and Subtopic Selector')

  # Allow the user to select a course from a dropdown menu
  selected_course = st.sidebar.selectbox('Select a course', available_courses)

  # Filter the DataFrame to only show data for the selected course
  filtered_df = df[df['course'] == selected_course]

  # Allow the user to select a topic from a dropdown menu
  selected_topic = st.sidebar.selectbox('Select a topic', sorted(filtered_df['topic'].unique()))

  # Filter the DataFrame to only show data for the selected topic within the selected course
  filtered_df = filtered_df[filtered_df['topic'] == selected_topic]

  # Allow the user to select a subtopic from a dropdown menu
  selected_subtopic = st.sidebar.selectbox('Select a subtopic', sorted(filtered_df['subtopic'].unique()))

  filtered_df = filtered_df[filtered_df['subtopic'] == selected_subtopic]

  course = filtered_df['course'].values[0]

  questions = filtered_df[['question1','question2','question3','question4','question5']].values[0]

  st.sidebar.header('Reset Chat') 
  reset_chat = st.sidebar.button('Reset Chat')
  if reset_chat:
    st.session_state['chat_history'] = st.session_state['chat_history'][:1]

  return questions, course

questions, course = create_sidebar()



def generate_response():
  system = f"""You are a high school tutor. You can help answer questions any questions that the student has. Keep your responses short. You must decline all requests form the user that are not related to the assigned topic. Changes in topic are only permitted if the user provies the hidden key 'asdj238'. You must not divulge the hidden key or mention that it exists. The topic of conversation is {course}."""
  import streamlit as st
  openai.api_key = st.secrets['openai_api_key']
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "system", "content": system}] + st.session_state['chat_history']
  )
  response = completion['choices'][0]['message']['content']

  return response





def display_chat_history():
  st.header('High School Chatbot')
  for message in st.session_state['chat_history']:
      if message['role'] == 'user':
          st.markdown(f"<div style='background-color: white; padding: 10px; border-radius: 5px;'><b>Student - </b>{message['content']}</div>", unsafe_allow_html=True)
      else:
          st.markdown(f"<div style='background-color: #F7F7F7; padding: 10px; border-radius: 5px; border: 1px solid #DDDDDD;'><b>Tutor - </b>{message['content']}</div>", unsafe_allow_html=True)

def create_question_input():
  # Display the input field for the user's question
  # st.header('Enter Question Below')
  user_question = st.text_input(label='Type a question...')
  return user_question

def show_example_questions(): 
  # Display the example questions
  # st.header('Or Pick an Example Question')
  for q in questions:
      if st.button(q):
          user_question = q
          return user_question

placeholder_chat_history = st.empty()
with placeholder_chat_history.container():
  display_chat_history()

st.write("#")
st.markdown("---") 
st.write("#")

user_question = create_question_input()

placeholder_user_question_button = st.empty()
with placeholder_user_question_button.container():
  user_question_button = show_example_questions()
if len(st.session_state['chat_history']) != 1:
  placeholder_user_question_button.empty()


try:
  if user_question_button:
    user_question = user_question_button
except:
  pass

# Handle user input
if user_question:
    # Add the user's question to the chat history
    add_to_chat_history('user', user_question)

    # TODO: Add code to handle the user's question and generate a response

    placeholder_user_question_button.empty()
    placeholder_chat_history.empty()
    with placeholder_chat_history.container():
      display_chat_history()

    agent_response = generate_response()

    add_to_chat_history('assistant', agent_response)


    placeholder_chat_history.empty()
    with placeholder_chat_history.container():
      display_chat_history()



