#Hello! It seems like you want to import the Streamlit library in Python. Streamlit is a powerful open-source framework used for building web applications with interactive data visualizations and machine learning models. To import Streamlit, you'll need to ensure that you have it installed in your Python environment.
#Once you have Streamlit installed, you can import it into your Python script using the import statement,


import streamlit as st
import pandas as pd

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

#Function to return the response
def load_answer(question):
    llm = OpenAI(model_name="text-davinci-003",temperature=0)
    answer=llm(question)
    return answer


#App UI starts here
st.set_page_config(page_title="Help us improve GOV.UK", page_icon=":robot:")
st.header("Help us improve GOV.UK")
st.write("Don’t include personal or financial information like your National Insurance number or credit card details.")
#st.subheader("Don’t include personal or financial information like your National Insurance number or credit card details.")

#Gets the user action
def get_action():
    input_action = st.text_area("What were you doing?", key="input_action")
    return input_action

#Gets the user problem
def get_problem():
    input_problem = st.text_area("What went wrong?", key="input_problem")
    return input_problem    


user_action=get_action()
user_problem=get_problem()

#template = """You are a binary classifier at HMRC, and the user complains that while they were {action}, 
#this problem occurred {problem}? Is this an urgent problem that requires immediate action? Reply 1 for immediate attention, 0 for everything else."""

#template = """Act as a tool that is only able to reply in the range from 1 to 5, you work at HMRC, and you the user complains that while they were {action}, 
#this problem occurred {problem}? Is this an urgent problem that requires immediate action? Rate the situation based on urgency."""

#template = """Match the following SITUATION to the category from this list: [Escalate to content team, Thank you for yuor feedback, Here is a phone number that can help

template = """Match the following SITUATION to the category from this list: [Service unavailable, link unavailable, 
The page is down,
Unable to contact HMRC,
can't deregister for VAT,
application confirmation inquiry,
address not showing,
address discrepancy,
Unclear interpretation of turnover requirement,
Unable to update marital status,
UTR Issues,
Other] 

SITUATION: {action}, {problem}.
OUTPUT:

"""

prompt = PromptTemplate.from_template(template)
request = prompt.format(action=user_action, problem=user_problem)
#prompt_template = PromptTemplate.from_template("You are a customer support agent at HMRC and you the use complains that while they were {action}, this problem occured {problem}?")
#prompt = prompt_template.format(action=user_action, problem=user_problem)

#response = load_answer(user_action + " , " + user_problem)
response = load_answer(request)

submit = st.button('Send')
#cancel = st.button('Cancel')


#If generate button is clicked
if submit:
    if response:
        if response == "Service unavailable":  
            st.subheader("Thank you for your feedback. Our team will look into this issue and work to fix it as soon as possible.")
        elif response == "Unable to contact HMRC":
            st.subheader("It appears you are having trouble connecting to HMRC. Please try contacting HMRC directly at 0300 200 3300.")
        elif response == "can't deregister for VAT":
            st.subheader("It looks like you try to cancel your VAT registration. Try contacting HMRC directly 0300 200 3300")
        elif response == "The page is down":
            st.subheader("Thank you for your feedback. Our team will look into this issue and work to fix it as soon as possible.")
        elif response == "address not showing":
            st.subheader("Thank you for your feedback.")
        elif response == "address discrepancy":
            st.subheader("Thank you for your feedback.")
        elif response == "Unclear interpretation of turnover requirement":
            st.subheader("Thank you for your feedback.")
        elif response == "Unable to update marital status":
            st.subheader("Thank you for your feedback.")
        elif response == "UTR Issues":
             st.subheader("It appears you are having trouble finding your UTR number. Please follow this page for guidance: https://www.gov.uk/find-lost-utr-number.")
        elif response == "Other":
            st.subheader("Thank you for your feedback.")
        else:
            st.subheader("Thank you for your feedback.")
        col1, col2, col3, col4 = st.columns([0.5,0.1,0.1,0.3])
        with col1:
            st.caption("This response was generated using AI tools. Was it helpful?")
        with col2:
            if st.button('👍'):
              st.write('')
        with col3:
            if st.button('👎'):
              st.write('')




   