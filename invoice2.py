import pandas
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from tkinter import filedialog
from tkinter import *


#input file
filename = ""
path = ""


def browseFiles():

    global path, filename

    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files",
                                                        "*.*"),
                                                       ("all files",
                                                        "*.*")))
    
    path = get_path(filename)

    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename +"\n " + "Save Destination: " + path)


#for getting the path of a file 
def get_path(filename):
    path = filename
    while path[-1] != '/':
        path = path[0:-1]
        print(path)

    return path

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

# def rate_time_calc(time: str, rate: int):
    
#     i = 0
#     time = str(time)
#     time = time[:-3]
#     for c in time:
        
#         if c == ":":
#             break 
#         i += 1
            
#     hours = int(time[:i])

#     if time[i+1:] != "00":
#         hours += float(int(time[i+1:]) / 60)
    
#     return hours * rate

def rate_time_calc(time:str, rate: int) :
    times = time.split(":")
    hours = float(times[0])
    minutes = float(int(times[1])/60.0)

    hours += minutes

    return hours * rate
    
      

#for generating invoice files from filename

def get_invoice(input_filename: str):
    
    print(input_filename)
    df = pandas.read_csv(input_filename)

    worker_rates = {
        "Wayne Tirrell": 50,
        "Samuel H Wakeman": 45,
        "Kyle R. Pinard": 44,
        "Charles Tirrell" : 40
    }

    classes = {}
    notes = {}

    #dates_df = df['Date']
    names_df = df['Name']
    notes_df = df['Notes']
    class_df = df['Class']
    duration_df = df['Duration']


    
    for i in range(len(names_df)):
        
        #if names_df[i] == "Wayne Tirrell" or names_df[i] == "Samuel H Wakeman" or names_df[i] == "Kyle R. Pinard" :
        if names_df[i] in worker_rates.keys():

            rate = worker_rates[names_df[i]]
            notesList = list(notes.keys())

            if class_df[i] not in classes:
                print(duration_df[i])
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

     
        output_filename = input_filename[:-5]
        final_class_df.to_excel(output_filename + 'class_invoice.xlsx')
        final_notes_df.to_excel(output_filename + 'notes_invoice.xlsx')


def generateFiles():
    print("filename" +  filename)
    get_invoice(filename) 
    label_file_explorer.configure(text ="Files saved to: " + path)


                                                                                                  
# Create the root window
window = Tk()
  
# Set window title
window.title('NECC INVOICE APP')
  
# Set window size
window.geometry("500x500")
  
#Set window background color
window.config(background = "green")
  
# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "Choose your file, make sure it is in .csv format",
                            width = 100, height = 4,
                            fg = "blue")
  
      
button_explore = Button(window,
                        text = "Browse for .csv File",
                        command = browseFiles)
  
# button_exit = Button(window,
#                      text = "Exit",
#                      command = exit)
                     
  
button_generate_files = Button(window,
                     text = "Run",
                     command = generateFiles)
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)
  
button_explore.grid(column = 1, row = 3)
  
button_generate_files.grid(column = 1,row = 5)
#button_exit.grid(column = 1,row = 7)
  
# Let the window wait for any events
window.mainloop()


