#!/usr/bin/env python
# coding: utf-8

# In[ ]:

print("---------- LOADING NECC INVOICE APP ----------")
import pandas
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
import nltk
nltk.download('punkt')
nltk.download('stopwords')

print("--------------- Instructions -----------------")
print()
print("Step 1: Make sure the invoice file you are uploading is on your desktop AND in .csv format. Note you can save files in csv format in Excel.")
print("Step 2: Follow the prompts to type in the input file name and the name you want to save your files under.")
print("Note that this program generates two files. ('class_' + yourFileName and 'notes_' + yourFileName)")
print("Step 3: Find your new files on your desktop.")
print("----------------------------------------------")

input_filename = input("Enter the input .csv filename. (Ex. Report_from_New_England_Coastal_Contractors_LLC.csv): ")

print("----------------------------------------------")

df = pandas.read_csv('Desktop/' + input_filename)
print(df)
worker_rates = {
    "Wayne Tirrell": 50,
    "Samuel H Wakeman": 40,
    "Kyle R. Pinard": 40,
    "Charles Tirrell": 40
}

classes = {}
notes = {}

#dates_df = df['Date']
names_df = df['Name']
notes_df = df['Notes']
class_df = df['Class']
duration_df = df['Duration']

def check_sim(s1: str, s2: str):
   
    #make lowercase
    s1 = s1.lower() 
    s2 = s2.lower() 
   
    X_list = word_tokenize(s1)  
    Y_list = word_tokenize(s2) 
  
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
   
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1)
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
        
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    
    return cosine

def rate_time_calc(time: str, rate: int):
    
    i = 0
    for c in time:
        
        if c == ":":
            break 
        i += 1
            
    hours = int(time[:i])
    if time[i+1:] != "00":
        hours += float(int(time[i+1:]) / 60)
    
    return hours * rate
            
#print(rate_time_calc("1:30", 45))
#print(rate_time_calc("1000:00", 45))


# In[4]:


for i in range(len(names_df)):
    if names_df[i] == "Wayne Tirrell" or names_df[i] == "Samuel H Wakeman" or names_df[i] == "Kyle R. Pinard" or names_df[i] == "Charles Tirrell":
        
        rate = worker_rates[names_df[i]]
        notesList = list(notes.keys())
        
        if class_df[i] not in classes:
            classes[class_df[i]] = rate_time_calc(duration_df[i],rate)
        else:
            classes[class_df[i]] += rate_time_calc(duration_df[i],rate)
        
        added = False
        for j in notesList:
            if check_sim(notes_df[i], j) > 0.85:
                #is similar to another note already in dict
                #add to that prexisting note
                notes[j] += rate_time_calc(duration_df[i],rate)
                added = True
                break
        
        if added == False:
            if notes_df[i] not in notes:
                notes[notes_df[i]] = rate_time_calc(duration_df[i],rate)
            else:
                notes[notes_df[i]] += rate_time_calc(duration_df[i],rate)

            
            
            
                
        #if notes_df[i] not in notes:
        #    notes[notes_df[i]] = rate_time_calc(duration_df[i],rate)
        #else:
        #    notes[notes_df[i]] += rate_time_calc(duration_df[i],rate)

list_len = len(classes)

class_list = classes.items()
notes_list = notes.items()


final_class_df = pandas.DataFrame(class_list, columns = ['Class','Amount'])
class_tot = 0

for amt in final_class_df['Amount']:
    class_tot += amt
    
#final_class_df.append({"Total": class_tot},ignore_index= False)
df2 = {'Class': "Total", 'Amount': class_tot} 
final_class_df = final_class_df.append(df2, ignore_index = True) 

final_notes_df = pandas.DataFrame(notes_list, columns = ['Note','Amount'])
notes_tot = 0

for amt in final_notes_df['Amount']:
    notes_tot += amt
    
#final_notes_df.append({"Total": notes_tot},ignore_index= False)
df3 = {'Note': "Total", 'Amount': notes_tot} 
final_notes_df = final_notes_df.append(df3, ignore_index = True) 

print(final_class_df)
print(final_notes_df)
#final_notes_df = final_notes_df.append(final_class_df, ignore_index = True) 
#print(final_notes_df)

output_filename = input("Enter the output excel filename (Ex. russell_invoice.xlsx): ")

final_class_df.to_excel('Desktop/class_'+ output_filename)
final_notes_df.to_excel('Desktop/notes_'+ output_filename)



# In[9]:


def get_invoice(input_filename: str, output_filename: str):
    
    df = pandas.read_csv('Desktop/' + input_filename)

    worker_rates = {
    "Wayne Tirrell": 50,
    "Samuel H Wakeman": 40,
    "Kyle R. Pinard": 40,
    "Charles Tirrell": 40
    }

    classes = {}
    notes = {}

    #dates_df = df['Date']
    names_df = df['Name']
    notes_df = df['Notes']
    class_df = df['Class']
    duration_df = df['Duration']

    
    for i in range(len(names_df)):
        if names_df[i] == "Wayne Tirrell" or names_df[i] == "Samuel H Wakeman" or names_df[i] == "Kyle R. Pinard" or names_df[i] == "Charles Tirrell":

            rate = worker_rates[names_df[i]]
            notesList = list(notes.keys())

            if class_df[i] not in classes:
                classes[class_df[i]] = rate_time_calc(duration_df[i],rate)
            else:
                classes[class_df[i]] += rate_time_calc(duration_df[i],rate)

            added = False
            for j in notesList:
                if check_sim(notes_df[i], j) > 0.85:
                    #is similar to another note already in dict
                    #add to that prexisting note
                    notes[j] += rate_time_calc(duration_df[i],rate)
                    added = True
                    break

            if added == False:
                if notes_df[i] not in notes:
                    notes[notes_df[i]] = rate_time_calc(duration_df[i],rate)
                else:
                    notes[notes_df[i]] += rate_time_calc(duration_df[i],rate)

        #use this if sentence comparor doesnt work    
                
        #if notes_df[i] not in notes:
        #    notes[notes_df[i]] = rate_time_calc(duration_df[i],rate)
        #else:
        #    notes[notes_df[i]] += rate_time_calc(duration_df[i],rate)

        list_len = len(classes)

        class_list = classes.items()
        notes_list = notes.items()


        final_class_df = pandas.DataFrame(class_list, columns = ['Class','Amount'])
        class_tot = 0
        for amt in final_class_df['Amount']:
            class_tot += amt
            
        df2 = {'Class': "Total", 'Amount': class_tot} 
        final_class_df = final_class_df.append(df2, ignore_index = True) 

        
        final_notes_df = pandas.DataFrame(notes_list, columns = ['Note','Amount'])
        notes_tot = 0
        for amt in final_notes_df['Amount']:
            notes_tot += amt
            
        df3 = {'Note': "Total", 'Amount': notes_tot} 
        final_notes_df = final_notes_df.append(df3, ignore_index = True) 

     
        
        final_class_df.to_excel('class_'+output_filename)
        final_notes_df.to_excel('notes_'+output_filename)
        
        
get_invoice(input_filename, output_filename)
print("Process Complete! Check Desktop for files.")

# In[ ]:




