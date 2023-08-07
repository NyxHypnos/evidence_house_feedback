import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px


df = pd.read_csv("../data/feedback_output_v3.csv")

sent_df = df[["date", "sentiment"]]
plot_sent_df = sent_df.pivot_table(index="date", columns="sentiment", aggfunc=len, fill_value=0)

# st.text("Sentiment over time")
st.line_chart(plot_sent_df)

simplified_df = df[["website_issue", "tax_issue", "guidance_issue"]]
plot_df = pd.DataFrame({"values": simplified_df.sum(), "names": simplified_df.columns})


fig = px.pie(plot_df, values='values', names='names')
#fig.show()
st.plotly_chart(fig, use_container_width=True)
# st.plotly_chart(fig, use_container_width=True)