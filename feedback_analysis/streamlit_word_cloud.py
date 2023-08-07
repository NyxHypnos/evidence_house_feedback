import streamlit as st
import numpy as np
import pandas as pd
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv("../data/feedback_output_v3.csv")

words = df.keywords.values[[type(value) != float for value in df.keywords.values]]
comb_words = []
for word_list in words:

    for word in word_list.split(","):

        comb_words.append(word.strip())
    
text = " ".join(comb_words)

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot()