#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import time
import datetime
import dateutil.parser
from datetime import datetime
import pandas as pd


# In[15]:


# def isEndorsedByStaff(endorsements):
#     for endorsement in endorsements:
#         if 'role' in endorsement and ('professor' in endorsement['role'] or 'instructor' in endorsement['role'] or 'ta' in endorsement['role']):
#             return True
    
# def checkValidAnswer(post):
#     return ('i_answer' in post['type']) or ('tag_endorse' in post and isEndorsedByStaff(post['tag_endorse']))

def getAnswerList(post):
    answerList = []
    if('children' in post):
        postAnswers = post['children']
        for postAnswer in postAnswers:
            #whoAnswered = ''
            answer = ''
            if 'type' in postAnswer and 'history' in postAnswer and 'subject' not in postAnswer['history']:
                whoAnswered = postAnswer['type']
                #last_modified = postAnswer['history'][len(postAnswer['history']) - 1]
                last_modified = getLastModified(postAnswer)
                answer = last_modified['content']
                answerToWhoAnswered = (answer, whoAnswered)
                answerList.append(answerToWhoAnswered)
            elif 'type' in postAnswer and 'followup' in postAnswer['type']:
                question = postAnswer['subject']
                whoAsked = 'followup_question'
                questionToWhoAsked = (question, whoAsked)
                answerList.append(questionToWhoAsked)
                if 'children' in postAnswer:
                    followup_question_answers = postAnswer['children']
                    for i in range(0, len(followup_question_answers)):
                        whoAnswered = followup_question_answers[i]['type']
                        answer = followup_question_answers[i]['subject']
                        answerToWhoAnswered = (answer, whoAnswered)
                        answerList.append(answerToWhoAnswered)
                        
    return answerList

def getLastModified(post):
    history = post['history']
    last_modified_answer = history[0]
    last_modified_datetime = dateutil.parser.parse(history[0]['created'])
    for i in range(0, len(history)):
        post_datetime = dateutil.parser.parse(history[i]['created'])
        if(post_datetime > last_modified_datetime):
            last_modified_datetime = post_date
            last_modified_answer = history[i]
            
    return last_modified_answer

def extractData(filename):
    with open(filename, 'r') as openfile:
        input = json.load(openfile)
        #print(input)
        df = pd.DataFrame(columns = ['Post','Link','Sentence','WhoAnswered'])
        for i in range(0, len(input)):
            post = input[i]
            if 'history' in post:
                last_modified = getLastModified(post)
                if 'subject' in last_modified and 'content' in last_modified and '<img' not in last_modified['content']:
                    subject = last_modified['subject']
                    content = last_modified['content']
                    post_ID = post['nr']
                    question_link = post['question_link']
                    answerList = getAnswerList(input[i])
                    df = df.append({'Post': post_ID, 'Link': question_link,'Sentence': subject + "." + content, 'WhoAnswered': 'question'}, ignore_index = True)  
                    for i in range(0, len(answerList)):
                        df = df.append({'Post': post_ID, 'Link': question_link,'Sentence': answerList[i][0], 'WhoAnswered': answerList[i][1]}, ignore_index = True)

        return df
#     for i in range(0, len(df)):
#         print("Post: "+str(int(df.iloc[i]['Post'])))
#         print("Sentence: "+df.iloc[i]['Sentence'])


# In[17]:


#usage
#final_df = pd.concat([extractData("data/fall_22_nlp.json"), extractData("data/spring_22_nlp.json")])
#print(final_df.to_string())
#final_df

