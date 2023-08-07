
import time
import pandas as pd
import openai

# INSERT YOUR OPENAI KEY HERE
openai.api_key = ""

def submitAIQuery(systemMessage, contentMessage, tokens, model = "gpt-3.5-turbo"):
    return openai.ChatCompletion.create(
            model = model,
            messages = [
                        {
                            "role": "system",
                            "content": systemMessage
                        },
                        {
                            "role": "user",
                            "content": contentMessage
                        }
            ],
            temperature = 0.1,
            max_tokens = tokens
        )

# Load Jesse's output file and identify distinct problem summaries
print("Loading data")
df = pd.read_csv('../data/feedback_output_v3.csv')
df["problem_summary"] = df["problem_summary"].str.lower()
new = pd.DataFrame({'count' : df.groupby('problem_summary')['problem_summary'].count()}).reset_index()
new = new.sort_values("count", ascending = False)

# Ask LLM for distinct problem summaries
print("Getting standardised problem summaries")
systemMessage = 'You will receive data formatted as CSV. Extract the following ' +\
                'data:\n' + \
                'problem_summary: the original problem summary\n' + \
                'corrected_summary: if a problem_summary in a different row expresses a similar concept in a shorter form, return that. Otherwise, return problem_summary. If you are not sure, return problem_summary.\n' + \
                'Format the result as json'
correctedList = submitAIQuery(systemMessage,
                            new[:25]["problem_summary"].to_csv(),
                            10000, 
                            model = "gpt-3.5-turbo-16k")
correctionsDF = pd.read_json(correctedList.choices[0].message.content)

# "Correct" the problem summaries to LLM's standardised text
print("Standardising problem summaries")
originalsList = correctionsDF["problem_summary"].values.tolist()
correctionsList = correctionsDF["corrected_summary"].values.tolist()
corrections = dict()
for o,c in zip(originalsList, correctionsList):
    corrections[o] = c
def correct(x):
    if isinstance(x, str) and x.lower() in corrections:
        return corrections[x.lower()]
    return x
df["problem_summary"] = df["problem_summary"].apply(correct)

# Calculate top problem summaries
print("Computing top problem summaries")
new = pd.DataFrame({'count' : df.groupby('problem_summary')['problem_summary'].count()}).reset_index()
new = new.sort_values("count", ascending = False)
topProblems = new[:10]["problem_summary"].values.tolist()
print("------------------\nTop problems:\n" 
        + "\n".join(topProblems)
        +"\n------------------\n")

# Load the original feedback
print("Loading original data")
baseData = pd.read_csv("../hrmc_feedback.csv")
colNames = [s for s in baseData.columns]
colNames[0] = "row_number"
baseData.columns = colNames

# Re-classify messages according to our revised categories
systemMessage = 'You will receive data formatted as CSV. Extract the ' + \
                'following data:\n' + \
                'row_number: the first column in the original data' + \
                'top10_summary: whether the problem is best described as "'+ \
                        '" or "'.join(topProblems)+'". If you are not sure '+ \
                        'then say "Other".\n'+ \
                'Format the result as json'
nRows = len(baseData)
batchSize = 5
nBatches = nRows // batchSize
resultsJSON = []
timestamps = []
for i in range(nBatches):
    print("Processing data batch " + str(i+1) + "/" + str(nBatches))
    oldI = i * batchSize
    newI = (i + 1) * batchSize
    thisResult = submitAIQuery(systemMessage,
                                baseData[oldI:newI].to_csv(),
                                10000, 
                                model = "gpt-3.5-turbo-16k")
    thisResult = thisResult["choices"][0]["message"]["content"]
    resultsJSON.append(thisResult)
    timestamps.append(time.time())

# Convert JSON to data frame
print("Converting JSON to dataframe")
outputDF = pd.DataFrame()
for i,response in enumerate(resultsJSON):
    try:
        thisDF = pd.read_json(response)
        outputDF = pd.concat([outputDF, thisDF])
    except:
        print("Broke at block",i+1)

# Merge (kinda...) new "top 10" summary column to Jesse's data and export
print("Attaching new column and exporting")
resultsDF = pd.concat([df, outputDF.reset_index()], axis = 1)
resultsDF.to_csv("../data/top10Classified_v2.csv")

