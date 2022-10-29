import pandas as pd
import json
def wrangle(filename):
    #Using context we open the json file and load it in as a list of dictionary
    with open(filename,'r') as file:
        complaint_dict = json.load(file)
    # We extract only the key `_source` as it is a dictionary of data we need
    # We append each dictionary instance to a list of dictionary
    list_of_observation = [i['_source'] for i in complaint_dict]
    df = pd.DataFrame().from_dict(list_of_observation)
    # We reformat the date columns to a datetime dtype
    df['date_received'] = pd.to_datetime(df['date_received'])
    df['date_sent_to_company'] = pd.to_datetime(df['date_sent_to_company'])
    # We set the index to the date the complaint was received
    df.set_index('date_received',inplace=True)
    df.sort_index(inplace=True)
    return df
def updated_wrangle(filename):
    #Using the wrangle function to load json file into DataFrame
    df = wrangle(filename)
    # Dropping columns with high missing values
    df.drop(['company_public_response','tags'],axis=1,inplace=True)
    # Fill missing rows in the consumer_consent_provided with N/A
    df['consumer_consent_provided'].fillna('N/A',inplace=True)
    # We drop column with high and low cardinality
    df.drop(['complaint_id','product','consumer_disputed'],axis=1,inplace = True)
    # We replace the complaint what happened with length of charcter in the string
    df['complaint_what_happened'] = df['complaint_what_happened'].str.len()
    # We drop rows with the suspicious date values
    mask = df['date_sent_to_company'] <= df.index
    df = df[mask]
    # Replace the web referrals with referrals
    df['submitted_via'].replace({'Web Referral':'Referral'},inplace=True)
    # Dropping rows with null values in the state and zip code feature
    df.dropna(inplace=True)
    return df