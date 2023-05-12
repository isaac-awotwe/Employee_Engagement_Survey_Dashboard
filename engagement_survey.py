# -*- coding: utf-8 -*-
"""
Created on Mon May  1 18:03:18 2023

@author: isaac.awotwe.z
"""
#Import libs

import pandas as pd
import numpy as np
import openpyxl
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# page configurations

st.set_page_config(page_title = "Employee Engagement Survey Dashboard", 
                   page_icon=":bar_chart:",
                   layout="wide")



#Load Data
survey_df = pd.read_excel(
io = "survey_data.xlsx", 
 engine = "openpyxl",
 sheet_name = "data",
 )

pop_df = pd.read_excel(
io = "pop_count.xlsx", 
 engine = "openpyxl",
 sheet_name = "data",
 )
pop_df.set_index("Department Name", inplace=True)

#Metrics
overall_resp_count = len(survey_df)
overall_pop_count = pop_df["Employee Count"].sum()


#Helpful objects
dept_list = ['Asset Management', 'Business Development',
       'Corporate Communications', 'Creative Services',
       'Customer Service', 'Engineering', 'Facilities',
       'Finance and Accounting', 'Human Resources',
       'Information Technology', 'Investor Relations', 'Legal',
       'Maintenance', 'Marketing', 'Medical Services', 
       'Operations', 'Product Management',
       'Production', 'Project Management', 'Purchasing',
       'Quality Assurance', 'Research and Development', 'Sales',
       'Strategic Initiatives', 'Strategic Services',
       'Training and Development', 'Transport']

dept_list_for_filter = ['Asset Management', 'Business Development',
       'Corporate Communications', 'Creative Services',
       'Customer Service', 'Engineering', 'Facilities',
       'Finance and Accounting', 'Human Resources',
       'Information Technology', 'Investor Relations', 'Legal',
       'Maintenance', 'Marketing', 'Medical Services', 
       'Operations', 'Product Management',
       'Production', 'Project Management', 'Purchasing',
       'Quality Assurance', 'Research and Development', 'Sales',
       'Strategic Initiatives', 'Strategic Services',
       'Training and Development', 'Transport', 'Prefer not to answer', 'Not sure']

questions=['Essential information flows effectively from senior leadership to staff.',
'I have confidence in the senior leadership of my department.',
'My manager treats me with respect.',
"My manager models the organizational values.",
'I receive meaningful recognition for work well done.',
'I have opportunities to provide input into decisions that affect my work.',
'I have opportunities for career growth within the organization.',
'I would recommend the organization as a great place to work.']


questions_chart=['Essential information flows effectively \n from senior leadership to staff.',
'I have confidence in the senior \n leadership of my department.',
'My manager treats me with respect.',
"My manager models the \n organizational values.",
'I receive meaningful recognition \n for work well done.',
'I have opportunities to provide input \n into decisions that affect my work.',
'I have opportunities for career growth \n within the organization.',
'I would recommend the organization \n as a great place to work.']

cols=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']

improve_cols=['Career Advancement',
       'Inclusivity', 'Innovation', 'Learning and Development Opportunity',
       'Organizational Culture', 'Quality of Immediate Supervision',
       'Respect in the Workplace', 'Work-life Balance',
       'Safe and Healthy Workplace', 'None']

job_categories=['Executive Management', 'Manager/Senior Manager', 'Professional/Technical', 'Administration', 'Prefer not to answer']
yos=['Less than 1 year', '1 year', '2 years', '3 years', '4 years', '5-7 years', '8-10 years', '11-15 years', '16-20 years', '21-30 years', '31 years or more', 'Prefer not to answer']
loc=['Africa', 'Asia', 'Europe', 'North America', 'Rest of the World', 'Prefer not to answer']
age=['Less than 25', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65 or older', 'Prefer not to answer']

survey_data_4index=survey_df.copy()
index_mapping={'Strongly Disagree': 'Negative', 'Disagree':'Negative', 
               'Strongly Agree':'Positive', 'Agree':'Positive', 'Neither Agree Nor Disagree': 'Neutral'}
for col in cols:
    survey_data_4index[col]=survey_data_4index[col].map(index_mapping)

improve_yes_df=survey_df[survey_df["Q11"]=="Yes"]

comm_mode_cols = ["Email", "Town hall", "Other"]
org_comm_mode_count = [np.round(survey_df[col].sum()/overall_resp_count*100, 4) for col in comm_mode_cols]

#Define Functions

## Engineer data
@st.cache_data    #add
def response_rate_df():
    department_and_counts=[]
    department_name_only =[]
    rates=[]
    for dept in dept_list:
        dept_resp_num = len(survey_df[survey_df["Q13"]==dept])
        dept_pop_count = pop_df.loc[dept, "Employee Count"]
        department_and_counts.append(dept+" "+"("+"n="+"{:,.0f}".format(dept_resp_num)+")")
        department_name_only.append(dept)
        rates.append(dept_resp_num/dept_pop_count*100)
    department_and_counts.append("Whole Organization"+" "+"("+"n="+"{:,.0f}".format(overall_resp_count)+")")
    rates.append(overall_resp_count/overall_pop_count*100)
    department_name_only.append("Whole Organization")
    rr_df=pd.DataFrame({"department":department_and_counts, "name_only":department_name_only, "response_rate":rates})
    rr_df.sort_values(by="response_rate", inplace=True)
    rr_df.reset_index(inplace=True, drop=True)
    rr_df["category"] = [str(i) for i in rr_df.index]
    rr_df["label"]=np.round(rr_df["response_rate"], 0)
    rr_df["label"]=rr_df["label"].astype("int")
    rr_df["label"]=pd.Series(["{}%".format(val) for val in rr_df["label"]],index=rr_df.index)
    return rr_df

@st.cache_data  
def stacked_horizontal_bar(top_labels, colors, x_data, y_data):
    fig = go.Figure()
    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation="h",
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                    )
                ))
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
            ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=True,
            ),
        barmode="stack",
        paper_bgcolor="rgb(248, 248, 255)",
        plot_bgcolor="rgb(248, 248, 255)",
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
        )
    annotations = []
    
    for yd, xd in zip(y_data, x_data):
        #labelling the y-axis
        annotations.append(dict(xref="paper", yref="y",
                                x=0.14, y=yd,
                                xanchor="right",
                                text=str(yd),
                                font=dict(family="Arial", size=10,
                                          color="rgb(67, 67, 67)"),
                                showarrow=False, align="right"))
        # labelling the first percentage of each bar (x_axis)
        annotations.append(dict(xref="x", yref="y",
                                x=xd[0]/2, y=yd,
                                text="{}%".format(int(np.round(xd[0],1))),
                                font=dict(family="Arial", size=10,
                                          color="rgb(0, 0, 0)"),
                                showarrow=False))
        # labelling the first likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref="x", yref="paper",
                                    x=xd[0]/2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family="Arial", size=14,
                                              color="rgb(67, 67, 67)"),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            # labelling the rest of the percentages for each bar (x_axis)
            annotations.append(dict(xref="x", yref="y",
                                    x=space + (xd[i]/2), y=yd,
                                    text="{}%".format(int(np.round(xd[i],1))),
                                    font=dict(family="Arial", size=10,
                                              color="rgb(0, 0, 0)"),
                                    showarrow=False))
            # labelling the likert scale
            if yd == y_data[-1]:
                annotations.append(dict(xref="x", yref="paper",
                                        x=space + (xd[i]/2), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family="Arial", size=14,
                                                  color="rgb(67, 67, 67)"),
                                        showarrow=False))
            space += xd[i]
            
    fig.update_layout(annotations = annotations)
    
    return fig
  
      
@st.cache_data        
def overall_index(df, dept):
    """ 
    Generates a data frame of overall engagement scores for whole organization and for specified department
    
    df: the data frame that has 'Strongly Agree' and 'Agree' converted to 'Positive',
        'Strongly Disagree' and 'Disagree' converted to 'Negative', and 'Neither Agree not Disagree' converted to 'Neutral'
    dept: the name of the department as a string
    
    return: the dataframe of overall engagement index values
    
    """
    Positive=[]
    Negative=[]
    Neutral=[]
    n=[]
    for col in cols:
        counts=df[col].value_counts(normalize=True)
        index=counts.index
        n.append(len(survey_data_4index))
        if ("Positive" in index) and ("Negative" in index) and ("Neutral" in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" in index) and ("Negative" in index) and ("Neutral" not in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(0)
        elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(0)
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" in index):
            Positive.append(0)
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" not in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(0)
            Neutral.append(0)
        elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" not in index):
            Positive.append(0)
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(0)
        elif ("Positive" not in index) and ("Negative" not in index) and ("Neutral" in index):
            Positive.append(0)
            Negative.append(0)
            Neutral.append(np.round(counts["Neutral"]*100,4))
    index_df_aps=pd.DataFrame({"questions":questions, "pos":Positive, "neu":Neutral, "neg":Negative, "n":n})   
    aps_pos=index_df_aps["pos"].mean()
    aps_neu=index_df_aps["neu"].mean()
    aps_neg=index_df_aps["neg"].mean()
    aps_n=index_df_aps["n"].mean()
    aps_org="Whole Organization"+" ("+"n="+"{:,.0f}".format(aps_n)+")"
    
    survey_data_4index_dept=df[df["Q13"]==dept]
    Positive=[]
    Negative=[]
    Neutral=[]
    n=[]
    for col in cols:
         counts=survey_data_4index_dept[col].value_counts(normalize=True)
         index=counts.index
         n.append(len(survey_data_4index_dept))
         if ("Positive" in index) and ("Negative" in index) and ("Neutral" in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" in index) and ("Negative" in index) and ("Neutral" not in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(0)
         elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(0)
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" in index):
             Positive.append(0)
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" not in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(0)
             Neutral.append(0)
         elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" not in index):
             Positive.append(0)
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(0)
         elif ("Positive" not in index) and ("Negative" not in index) and ("Neutral" in index):
             Positive.append(0)
             Negative.append(0)
             Neutral.append(np.round(counts["Neutral"]*100,4))
    index_df_dept=pd.DataFrame({"questions":questions, "pos":Positive, "neu":Neutral, "neg":Negative, "n":n})
    dept_pos=index_df_dept["pos"].mean()
    dept_neu=index_df_dept["neu"].mean()
    dept_neg=index_df_dept["neg"].mean()
    dept_n=index_df_dept["n"].mean()
    dept_org=department_select+" ("+"n="+"{:,.0f}".format(dept_n)+")"
    
    index_df=pd.DataFrame({"org":[aps_org, dept_org], "Positive":[aps_pos, dept_pos], 
                       "Neutral":[aps_neu, dept_neu], "Negative":[aps_neg, dept_neg]})
    #index_df.sort_values(by="Positive", ascending=False, inplace=True)
    index_df["positives_label"]=np.round(index_df["Positive"], 0)
    index_df["positives_label"]=index_df["positives_label"].astype(int)
    index_df["positives_label"]=pd.Series(["{}%".format(val) for val in index_df["positives_label"]],index=index_df.index)
    index_df["neutrals_label"]=np.round(index_df["Neutral"], 0)
    index_df["neutrals_label"]=index_df["neutrals_label"].astype(int)
    index_df["neutrals_label"]=pd.Series(["{}%".format(val) for val in index_df["neutrals_label"]],index=index_df.index)
    index_df["negatives_label"]=np.round(index_df["Negative"], 0)
    index_df["negatives_label"]=index_df["negatives_label"].astype(int)
    index_df["negatives_label"]=pd.Series(["{}%".format(val) for val in index_df["negatives_label"]],index=index_df.index)
    
    return index_df



@st.cache_data 
def overall_index_filter(df):
    """ 
    Generates a data frame of overall engagement scores for whole organization and for specified department
    
    df: the data frame that has 'Strongly Agree' and 'Agree' converted to 'Positive',
        'Strongly Disagree' and 'Disagree' converted to 'Negative', and 'Neither Agree not Disagree' converted to 'Neutral'
    dept: the name of the department as a string
    
    return: the dataframe of overall engagement index values
    
    """

    Positive=[]
    Negative=[]
    Neutral=[]
    n=[]
    for col in cols:
         counts=df[col].value_counts(normalize=True)
         index=counts.index
         n.append(len(df))
         if ("Positive" in index) and ("Negative" in index) and ("Neutral" in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" in index) and ("Negative" in index) and ("Neutral" not in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(0)
         elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(0)
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" in index):
             Positive.append(0)
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(np.round(counts["Neutral"]*100,4))
         elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" not in index):
             Positive.append(np.round(counts["Positive"]*100,4))
             Negative.append(0)
             Neutral.append(0)
         elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" not in index):
             Positive.append(0)
             Negative.append(np.round(counts['Negative']*100,4))
             Neutral.append(0)
         elif ("Positive" not in index) and ("Negative" not in index) and ("Neutral" in index):
             Positive.append(0)
             Negative.append(0)
             Neutral.append(np.round(counts["Neutral"]*100,4))
    index_df_dept=pd.DataFrame({"questions":questions, "pos":Positive, "neu":Neutral, "neg":Negative, "n":n})
    dept_pos=index_df_dept["pos"].mean()
    dept_neu=index_df_dept["neu"].mean()
    dept_neg=index_df_dept["neg"].mean()
    dept_n=index_df_dept["n"].mean()
    dept_org="Selected Employee Group"+" ("+"n="+"{:,.0f}".format(dept_n)+")"
    
    index_df=pd.DataFrame({"org":[dept_org], "Positive":[dept_pos], 
                       "Neutral":[dept_neu], "Negative":[dept_neg]})
    #index_df.sort_values(by="Positive", ascending=False, inplace=True)
    index_df["positives_label"]=np.round(index_df["Positive"], 0)
    index_df["positives_label"]=index_df["positives_label"].astype(int)
    index_df["positives_label"]=pd.Series(["{}%".format(val) for val in index_df["positives_label"]],index=index_df.index)
    index_df["neutrals_label"]=np.round(index_df["Neutral"], 0)
    index_df["neutrals_label"]=index_df["neutrals_label"].astype(int)
    index_df["neutrals_label"]=pd.Series(["{}%".format(val) for val in index_df["neutrals_label"]],index=index_df.index)
    index_df["negatives_label"]=np.round(index_df["Negative"], 0)
    index_df["negatives_label"]=index_df["negatives_label"].astype(int)
    index_df["negatives_label"]=pd.Series(["{}%".format(val) for val in index_df["negatives_label"]],index=index_df.index)

    return index_df


@st.cache_data 
def index_by_question_dept(df):
    Positive=[]
    Negative=[]
    Neutral=[]
    n=[]
    for col in cols:
        counts=df[col].value_counts(normalize=True)
        index=counts.index
        n.append(len(df))
        if ("Positive" in index) and ("Negative" in index) and ("Neutral" in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" in index) and ("Negative" in index) and ("Neutral" not in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(0)
        elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(0)
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" in index):
            Positive.append(0)
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(np.round(counts["Neutral"]*100,4))
        elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" not in index):
            Positive.append(np.round(counts["Positive"]*100,4))
            Negative.append(0)
            Neutral.append(0)
        elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" not in index):
            Positive.append(0)
            Negative.append(np.round(counts['Negative']*100,4))
            Neutral.append(0)
        elif ("Positive" not in index) and ("Negative" not in index) and ("Neutral" in index):
            Positive.append(0)
            Negative.append(0)
            Neutral.append(np.round(counts["Neutral"]*100,4))
    index_df=pd.DataFrame({"questions":questions, "Positive":Positive, "Neutral":Neutral, "Negative":Negative, "n":n})
    #index_df.sort_values(by="Positive", ascending=False, inplace=True)
    #index_df["positives_label"]=np.round(index_df["Positive"], 0)
    #index_df["positives_label"]=index_df["positives_label"].astype(int)
    #index_df["positives_label"]=pd.Series(["{}%".format(val) for val in index_df["positives_label"]],index=index_df.index)
    #index_df["neutrals_label"]=np.round(index_df["Neutral"], 0)
    #index_df["neutrals_label"]=index_df["neutrals_label"].astype(int)
    #index_df["neutrals_label"]=pd.Series(["{}%".format(val) for val in index_df["neutrals_label"]],index=index_df.index)
    #index_df["negatives_label"]=np.round(index_df["Negative"], 0)
    #index_df["negatives_label"]=index_df["negatives_label"].astype(int)
    #index_df["negatives_label"]=pd.Series(["{}%".format(val) for val in index_df["negatives_label"]],index=index_df.index)
    return index_df


@st.cache_data 
def overal_index_cat(df, category, qnum):
    avg_pos=[]
    avg_neg=[]
    avg_neu=[]
    n=[]
    #job_cat=survey_data_4index_dept["Q15"].unique()
    cat_list=[]
    for item in category:
        if item in df[qnum].unique():
            cat_list.append(item)
    #if 'Prefer not to answer' in job_cat:
        #job_cat.remove('Prefer not to answer')
    for cat in cat_list:
        survey_data_4index_cat=df[df[qnum]==cat]
        Positive=[]
        Negative=[]
        Neutral=[]
        for col in cols:
            counts=survey_data_4index_cat[col].value_counts(normalize=True)
            index=counts.index
            if ("Positive" in index) and ("Negative" in index) and ("Neutral" in index):
                Positive.append(np.round(counts["Positive"]*100,4))
                Negative.append(np.round(counts['Negative']*100,4))
                Neutral.append(np.round(counts["Neutral"]*100,4))
            elif ("Positive" in index) and ("Negative" in index) and ("Neutral" not in index):
                Positive.append(np.round(counts["Positive"]*100,4))
                Negative.append(np.round(counts['Negative']*100,4))
                Neutral.append(0)
            elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" in index):
                Positive.append(np.round(counts["Positive"]*100,4))
                Negative.append(0)
                Neutral.append(np.round(counts["Neutral"]*100,4))
            elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" in index):
                Positive.append(0)
                Negative.append(np.round(counts['Negative']*100,4))
                Neutral.append(np.round(counts["Neutral"]*100,4))
            elif ("Positive" in index) and ("Negative" not in index) and ("Neutral" not in index):
                Positive.append(np.round(counts["Positive"]*100,4))
                Negative.append(0)
                Neutral.append(0)
            elif ("Positive" not in index) and ("Negative" in index) and ("Neutral" not in index):
                Positive.append(0)
                Negative.append(np.round(counts['Negative']*100,4))
                Neutral.append(0)
            elif ("Positive" not in index) and ("Negative" not in index) and ("Neutral" in index):
                Positive.append(0)
                Negative.append(0)
                Neutral.append(np.round(counts["Neutral"]*100,4))
        index_df=pd.DataFrame({"questions":questions, "Positives":Positive, "Neutrals":Neutral, "Negatives":Negative})
        avg_pos.append(index_df["Positives"].mean())
        avg_neg.append(index_df["Negatives"].mean())
        avg_neu.append(index_df["Neutrals"].mean())
        n.append(len(survey_data_4index_cat))
    cat_df=pd.DataFrame({"Category":cat_list, "Positive":avg_pos, "Neutral":avg_neu, "Negative":avg_neg, "n":n})
    #cat_df.sort_values(by="Positive", inplace=True)
    cat_df["positives_label"]=np.round(cat_df["Positive"], 0)
    cat_df["positives_label"]=cat_df["positives_label"].astype(int)
    cat_df["positives_label"]=pd.Series(["{}%".format(val) for val in cat_df["positives_label"]],index=cat_df.index)
    cat_df["neutrals_label"]=np.round(cat_df["Neutral"], 0)
    cat_df["neutrals_label"]=cat_df["neutrals_label"].astype(int)
    cat_df["neutrals_label"]=pd.Series(["{}%".format(val) for val in cat_df["neutrals_label"]],index=cat_df.index)
    cat_df["negatives_label"]=np.round(cat_df["Negative"], 0)
    cat_df["negatives_label"]=cat_df["negatives_label"].astype(int)
    cat_df["negatives_label"]=pd.Series(["{}%".format(val) for val in cat_df["negatives_label"]],index=cat_df.index)
    categories=[word[0]+" (n="+"{:,.0f}".format(word[1])+")" for word in zip(cat_df["Category"], cat_df["n"])]
    cat_df["Category"]=pd.Series(categories)
    return cat_df



@st.cache_data 
def comm_mode(df):
    '''
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    qnum : TYPE
        DESCRIPTION.
    comm_type : TYPE - list
        DESCRIPTION.- whether the communication frequncy or communication mode list

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    depmt = [np.round(df[col].sum()/len(df)*100, 4) for col in comm_mode_cols]
    return pd.DataFrame({"mode":comm_mode_cols, "selected group":depmt, "whole org":org_comm_mode_count})

@st.cache_data 
def comm_freq(df):
    '''
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    survey_value_counts=df["Q10"].value_counts(normalize=True)
    index=np.sort(survey_value_counts.index)
    survey = [np.round(survey_value_counts[item]*100, 4) for item in index]
    org_value_counts=survey_df["Q10"].value_counts(normalize=True)
    population = [np.round(org_value_counts[item]*100, 4) if item in org_value_counts.index else 0 for item in index]
    return pd.DataFrame({"sentiment":index, "selected group":survey, "whole org":population})


@st.cache_data
def improve_yesno(df):
    counts_org=survey_df["Q11"].value_counts(normalize=True).reset_index()
    counts_org.columns=["Improvement", "Percentage"]
    counts_org["Percentage"]=np.round(counts_org["Percentage"]*100, 4)
    org_yes=counts_org.loc[counts_org["Improvement"]=="Yes", "Percentage"].values[0]
    org_no=counts_org.loc[counts_org["Improvement"]=="No", "Percentage"].values[0]
    
    counts=df["Q11"].value_counts(normalize=True)
    counts=counts.reset_index()
    counts.columns=["Improvement", "Percentage"]
    counts["Percentage"]=np.round(counts["Percentage"]*100, 4)
    dept_yes=counts.loc[counts["Improvement"]=="Yes", "Percentage"].values[0]
    dept_no=counts.loc[counts["Improvement"]=="No", "Percentage"].values[0]
    return pd.DataFrame({"response":["Yes", "No"], "selected group":[dept_yes, dept_no], "whole org":[org_yes, org_no]})


def improve_detail(df):
    improve_score_org = [np.round(improve_yes_df[col].sum()/len(improve_yes_df)*100, 4) for col in improve_cols]
    improve_score_dept = [np.round(df[col].sum()/len(df)*100, 4) for col in improve_cols]
    return pd.DataFrame({"improvement_area":improve_cols, "whole org":improve_score_org, "selected group":improve_score_dept})
    


# Summary Data


## What metrics will be relevant?
## Difference from baseline
## Percent change from status quo

# build dashboard
##tab1, tab2 = st.tabs(["Results by Department", "Overall Results with Filters"])


st.sidebar.header("Departmental or Overall Results")
add_sidebar = st.sidebar.selectbox("Please select dimension", ("Results by Department", "Overall Results with Filters"))

if add_sidebar == "Results by Department":
    department_select = st.selectbox("Pick a department:", dept_list)
    
    survey_data_4index_dept=survey_data_4index[survey_data_4index["Q13"]==department_select]
    improve_yes_df_dept=improve_yes_df[improve_yes_df["Q13"]==department_select]
    
    # survey response rate
    response_df = response_rate_df()
    color_discrete_sequence = ['#99CCFF']*len(response_df)
    dept_pos = int(response_df.loc[response_df["name_only"]==department_select, "category"].values)
    org_pos = int(response_df.loc[response_df["name_only"]=="Whole Organization", "category"].values)
    color_discrete_sequence[dept_pos] = '#0070C0'
    color_discrete_sequence[org_pos] = '#ED7D31'
    fig = px.bar(response_df, y = "department", x= "response_rate", color='category', 
                 color_discrete_sequence=color_discrete_sequence, height=600, 
                 title = "Survey Response Rate", text="label")
    fig.update_traces(textfont_size=12, textfont_color = 'rgb(0, 0, 0)',textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)
    
    st.markdown("---") # create a space before the next object
    
    # write the definition of the engagement survey
    st.write("Engagement index score measures employee sentiment towards the areas of engagement represented by questions in the Pulse Survey.")
    st.write("A higher index score (positive score) reflects a higher level of staff engagement.")
    st.write("The engagement index score is calculated by averaging the positive responses (agree or strongly agree) for the following engagement questions:")
    
    '''
    1. *Essential information flows effectively from senior leadership to staff.*
    2. *I have confidence in the senior leadership of my department.* 
    3. *My manager treats me with respect.*
    4. *My manager models the organizational values.*
    5. *I receive meaningful recognition for work well done.*
    6. *I have opportunities to provide input into decisions that affect my work.*
    7. *I have opportunities for career growth within the organization.*
    8. *I would recommend the organization as a great place to work.*
    '''
    
    # engagement index - overall score
    overall_index_df = overall_index(df=survey_data_4index, dept=department_select) # create dataframe for overall index
    top_labels = ["Positive", "Neutral", "Negative"] # begin chart of overall index - department compared to APS
    colors = ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = overall_index_df[["Positive", "Neutral", "Negative"]].values
    y_data = overall_index_df[["org"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_overall_score = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_overall_score.update_layout(height=400, width=700, title = "Engagement Index - Overall Score ({} Versus Whole Organization)".format(department_select))
    st.plotly_chart(fig_overall_score)
    
    # Engagement Index - Detail
    index_detail_dept_df = index_by_question_dept(df=survey_data_4index_dept)
    top_labels = ["Positive", "Neutral", "Negative"] # begin chart of overall index - department compared to APS
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_detail_dept_df[["Positive", "Neutral", "Negative"]].values
    ## y_data = questions_chart
    y_data = index_detail_dept_df[["questions"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_detail_dept = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_detail_dept.update_layout(height=400, width=700, title = "Engagement Index - Detail ({})".format(department_select))
    st.plotly_chart(fig_index_detail_dept)
    
    # Engagement Index by Job category
    index_jobcat_df = overal_index_cat(df = survey_data_4index_dept, category = job_categories, qnum="Q15")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_jobcat_df[["Positive", "Neutral", "Negative"]].values
    y_data = index_jobcat_df[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_jobcat = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_jobcat.update_layout(height=400, width=700, title = "Engagement Index by Job Category ({})".format(department_select))
    st.plotly_chart(fig_index_jobcat)
    
    # Engagement Index by Years of Service
    index_yos_df = overal_index_cat(df = survey_data_4index_dept, category = yos, qnum="Q14")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_yos_df[["Positive", "Neutral", "Negative"]].values
    y_data = index_yos_df[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_yos = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_yos.update_layout(height=400, width=700, title = "Engagement Index by Years of Service ({})".format(department_select))
    st.plotly_chart(fig_index_yos)
    
    # Engagement Index by Location
    index_loc_df = overal_index_cat(df = survey_data_4index_dept, category = loc, qnum="Q16")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_loc_df[["Positive", "Neutral", "Negative"]].values
    y_data = index_loc_df[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_loc = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_loc.update_layout(height=400, width=700, title = "Engagement Index by Location ({})".format(department_select))
    st.plotly_chart(fig_index_loc)
    
    # Engagement by Age Group
    index_age_df = overal_index_cat(df = survey_data_4index_dept, category = age, qnum="Q17")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_age_df[["Positive", "Neutral", "Negative"]].values
    y_data = index_age_df[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_age = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_age.update_layout(height=400, width=700, title = "Engagement Index by Age ({})".format(department_select))
    st.plotly_chart(fig_index_age)
    
    
    # Mode of Communication
    comm_mode_df = comm_mode(df = survey_data_4index_dept)
    fig_mode_dept = go.Figure(data=[
        go.Bar(name=department_select, x=comm_mode_df['mode'].values, y = comm_mode_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in comm_mode_df['selected group']]),
        go.Bar(name = "Whole Organization", x = comm_mode_df['mode'].values, y = comm_mode_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in comm_mode_df['whole org']])
        ])
    fig_mode_dept.update_layout(title = "How do you prefer to hear from your senior leaders? (Select all that apply)")
    st.plotly_chart(fig_mode_dept)
    
    # Frequency of Communication
    comm_freq_df = comm_freq(df = survey_data_4index_dept)
    fig_freq_dept = go.Figure(data=[
        go.Bar(name=department_select, x=comm_freq_df['sentiment'].values, y = comm_freq_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in comm_freq_df['selected group']]),
        go.Bar(name = "Whole Organization", x = comm_freq_df['sentiment'].values, y = comm_freq_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in comm_freq_df['whole org']])
        ])
    fig_freq_dept.update_layout(title = "How often would you like to hear from your Chief Executive officer?")
    st.plotly_chart(fig_freq_dept)
    
    # Improvement in Workplace - Yes or No
    improve_yesno_df = improve_yesno(df = survey_data_4index_dept)
    fig_improve_yesno = go.Figure(data=[
        go.Bar(name=department_select, x=improve_yesno_df['response'].values, y = improve_yesno_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in improve_yesno_df['selected group']]),
        go.Bar(name = "Whole Organization", x = improve_yesno_df['response'].values, y = improve_yesno_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in improve_yesno_df['whole org']])
        ])
    fig_improve_yesno.update_layout(title = "I have seen improvements in my current workplace")
    st.plotly_chart(fig_improve_yesno)
    
    # Improvement in Workplace - Details
    improve_detail_df = improve_detail(df = improve_yes_df_dept)
    fig_improve_detail = go.Figure(data=[
        go.Bar(name=department_select, x=improve_detail_df['improvement_area'].values, y = improve_detail_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in improve_detail_df['selected group']]),
        go.Bar(name = "Whole Organization", x = improve_detail_df['improvement_area'].values, y = improve_detail_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in improve_detail_df['whole org']])
        ])
    fig_improve_detail.update_layout(title = "If yes, I have seen improvements in (select all that apply):")
    st.plotly_chart(fig_improve_detail)
    
    
    
    
    
if add_sidebar == "Overall Results with Filters":
    st.subheader("Please Filter Here:")
    dept_filter = st.multiselect(
        "Select the Department:",
        options = dept_list_for_filter,
        default = "Human Resources")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
       job_filter = st.multiselect(
           "Select the Job Category:",
           options = job_categories,
           default = job_categories)
    with col2:
      loc_filter = st.multiselect(
          "Select the Location:",
          options = loc,
          default = loc)
    with col3:
       age_filter = st.multiselect(
           "Select the Age Group:",
           options = age,
           default = age)
    with col4:
       yos_filter = st.multiselect(
           "Select the Years of Service:",
           options = yos,
           default = yos)

    
    st.markdown("##")
    
    df_selection = survey_data_4index.query(
        "Q13 == @dept_filter & Q14 == @yos_filter & Q15 == @job_filter & Q16 == @loc_filter & Q17 == @age_filter"
        )
    
    st.markdown("##### Full Survey Data for Selected Group")
    st.dataframe(df_selection)
    
    st.markdown("##")
    
    # engagement index - overall score
    overall_index_df_filter = overall_index_filter(df=df_selection) # create dataframe for overall index
    top_labels = ["Positive", "Neutral", "Negative"] # begin chart of overall index - department compared to APS
    colors = ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = overall_index_df_filter[["Positive", "Neutral", "Negative"]].values
    y_data = overall_index_df_filter[["org"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_overall_score_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_overall_score_filter.update_layout(height=400, width=700, title = "Engagement Index - Overall Score")
    st.plotly_chart(fig_overall_score_filter)
    
    # Engagement Index by Job category
    index_jobcat_df_filter = overal_index_cat(df = df_selection, category = job_categories, qnum="Q15")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_jobcat_df_filter[["Positive", "Neutral", "Negative"]].values
    y_data = index_jobcat_df_filter[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_jobcat_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_jobcat_filter.update_layout(height=400, width=700, title = "Engagement Index by Job Category")
    st.plotly_chart(fig_index_jobcat_filter)
    
    # Engagement Index by Years of Service
    index_yos_df_filter = overal_index_cat(df = df_selection, category = yos, qnum="Q14")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_yos_df_filter[["Positive", "Neutral", "Negative"]].values
    y_data = index_yos_df_filter[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_yos_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_yos_filter.update_layout(height=400, width=700, title = "Engagement Index by Years of Service")
    st.plotly_chart(fig_index_yos_filter)
    
    # Engagement Index by Location
    index_loc_df_filter = overal_index_cat(df = df_selection, category = loc, qnum="Q16")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_loc_df_filter[["Positive", "Neutral", "Negative"]].values
    y_data = index_loc_df_filter[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_loc_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_loc_filter.update_layout(height=400, width=700, title = "Engagement Index by Location")
    st.plotly_chart(fig_index_loc_filter)
    
    # Engagement by Age Group
    index_age_df_filter = overal_index_cat(df = df_selection, category = age, qnum="Q17")
    top_labels = ["Positive", "Neutral", "Negative"]
    colors =  ["rgb(146, 208, 80)", "rgb(166, 166, 166)", "rgb(255, 102, 0)"]
    x_data = index_age_df_filter[["Positive", "Neutral", "Negative"]].values
    y_data = index_age_df_filter[["Category"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_age_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_age_filter.update_layout(height=400, width=700, title = "Engagement Index by Age")
    st.plotly_chart(fig_index_age_filter)
    
    # Engagement Index - Detail
    index_detail_df = index_by_question_dept(df=df_selection)
    top_labels = ["Positive", "Neutral", "Negative"] # begin chart of overall index - department compared to APS
    colors =  ["rgb(153, 204, 255)", "rgb(191, 191, 191)", "rgb(0, 112, 192)"]
    x_data = index_detail_df[["Positive", "Neutral", "Negative"]].values
    y_data = index_detail_df[["questions"]].values
    y_data_list =[y_data[i][0] for i in range(y_data.shape[0])]
    fig_index_detail_filter = stacked_horizontal_bar(top_labels=top_labels, colors=colors, x_data=x_data, y_data=y_data_list)
    fig_index_detail_filter.update_layout(height=400, width=700, title = "Engagement Index - Detail")
    st.plotly_chart(fig_index_detail_filter)
    
    # Mode of Communication
    comm_mode_df = comm_mode(df = df_selection)
    fig_mode_dept = go.Figure(data=[
        go.Bar(name="Selected Employee Group", x=comm_mode_df['mode'].values, y = comm_mode_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in comm_mode_df['selected group']]),
        go.Bar(name = "Whole Organization", x = comm_mode_df['mode'].values, y = comm_mode_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in comm_mode_df['whole org']])
        ])
    fig_mode_dept.update_layout(title = "How do you prefer to hear from your senior leadership? (Select all that apply)")
    st.plotly_chart(fig_mode_dept)
    
    # Frequency of Communication
    comm_freq_df = comm_freq(df = df_selection)
    fig_freq_filter = go.Figure(data=[
        go.Bar(name="Selected Employee Group", x=comm_freq_df['sentiment'].values, y = comm_freq_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in comm_freq_df['selected group']]),
        go.Bar(name = "Whole Organization", x = comm_freq_df['sentiment'].values, y = comm_freq_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in comm_freq_df['whole org']])
        ])
    fig_freq_filter.update_layout(title = "How often would you like to hear from your Chief Executive officer?")
    st.plotly_chart(fig_freq_filter)
    
    # Improvement in Workplace - Yes or No
    improve_yesno_df_filter = improve_yesno(df = df_selection)
    fig_improve_yesno_filter = go.Figure(data=[
        go.Bar(name="Selected Employee Group", x=improve_yesno_df_filter['response'].values, y = improve_yesno_df_filter['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in improve_yesno_df_filter['selected group']]),
        go.Bar(name = "Whole Organization", x = improve_yesno_df_filter['response'].values, y = improve_yesno_df_filter['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in improve_yesno_df_filter['whole org']])
        ])
    fig_improve_yesno_filter.update_layout(title = "I have seen improvements in my current workplace")
    st.plotly_chart(fig_improve_yesno_filter)
    
    # Improvement in Workplace - Details
    improve_yes_df_grp = df_selection[df_selection["Q11"]=="Yes"]
    improve_detail_df = improve_detail(df = improve_yes_df_grp)
    fig_improve_detail = go.Figure(data=[
        go.Bar(name="Selected Employee Group", x=improve_detail_df['improvement_area'].values, y = improve_detail_df['selected group'], text = ["{}%".format(int(np.round(num,1))) for num in improve_detail_df['selected group']]),
        go.Bar(name = "Whole Organization", x = improve_detail_df['improvement_area'].values, y = improve_detail_df['whole org'], text = ["{}%".format(int(np.round(num,1))) for num in improve_detail_df['whole org']])
        ])
    fig_improve_detail.update_layout(title = "If yes, I have seen improvements in (select all that apply):")
    st.plotly_chart(fig_improve_detail)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   

        
    
    
    

    



