"""Streamlit 101.

Docs:
- https://docs.streamlit.io/library/get-started
- https://docs.streamlit.io/library/api-reference/session-state
- https://discuss.streamlit.io/t/new-component-streamlit-chat-a-new-way-to-create-chatbots/20412

Examples:
    $ streamlit hello
    $ streamlit run chatefficient/streamlit_demo.py
"""

import datetime
import numpy as np
import streamlit as st
import pandas as pd
from streamlit_chat import message

baseData = pd.read_csv("../top10Classified_v2.csv")
baseData["top10_summary"] = baseData["top10_summary"].str.lower()

summary = pd.DataFrame({'count' : baseData.groupby(["top10_summary","date"])["top10_summary"].count()}).reset_index()
summary = summary.pivot(index='date', columns='top10_summary', values='count')

summary2 = pd.DataFrame({'count' : baseData.groupby("top10_summary")["top10_summary"].count()}).reset_index()
#summary2 = summary2.sort_values("count", ascending = False)
#summary2 = summary2[:10]

simplified_df = baseData[["date", "sentiment"]]
plot_df = simplified_df.pivot_table(index="date", columns="sentiment", aggfunc=len, fill_value=0)

summary3 = pd.DataFrame({'count' : baseData.groupby(["website_issue","tax_issue"])["top10_summary"].count()}).reset_index()

minDate = datetime.datetime.strptime(baseData["date"].min(),"%Y-%m-%d")
maxDate = datetime.datetime.strptime(baseData["date"].max(),"%Y-%m-%d")
MIN_MAX_RANGE = (minDate, maxDate)
PRE_SELECTED_DATES = (minDate, maxDate)


st.text("Top 10 feedback topics")
col1, col2 = st.columns(2)
with col1:
    st.write(summary2)
with col2:
    st.bar_chart(summary2, x = "top10_summary", y = "count")
st.text("Top 10 feedback topics, day by day")
st.bar_chart(summary)

    #st.line_chart(plot_df)
#st.write(summary3)
