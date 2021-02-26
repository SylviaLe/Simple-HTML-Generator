#Sylvia Le, Jack Zimmerman, Hang Nguyen, Melissa Alexander
#Programming Assignment 1
#File: generateHTML.py
#Date: 02-23-2021

#import libraries. re for regular expression
import re
from random import randrange
import datetime

def wrap(tag, word):
    #Wrap the string with the HTML tag
    temp = '<{0}>{1}</{2}>'.format(tag, word, tag)

    #Check if the end tag has components like 'id' or 'class' (we assume only these two are used at the moment)
    pattern = re.compile(r'</.+?>')     #use regex to find the end tag
    endtag = pattern.findall(temp)[0]
    openpart = temp[:temp.find(endtag)] #string slicing to keep the opening tag
    result = ''
    
    if ('id' in endtag):    #if the word 'id' is found
        substr = endtag[endtag.find('id'):-1]   #find its index in the end tag
        new_endtag = endtag.replace(substr, '') #then remove it
        result = openpart + new_endtag          #the new string with HTML tag wrap around
        return result
    
    elif ('class' in pattern.findall(temp)[0]):
        substr = temp[temp.find('class'):-1]
        new_endtag = endtag.replace(substr, '')
        result = openpart + new_endtag
        return result
    
    else: #if no 'id' or 'class' found, return the 1st result
        return temp


def table_gen(row, col):
    #Generate a blank HTML table, with the designate number of row and column
    table = ''
    k = 0 #the index for the table cell, used for formatting later
    for i in range(row):
        table_row = ''
        for j in range(col): #generate the <td> tag. Number of <td> tag inside a <tr> = col
            table_row += '<td>{' + str(k) + '}</td>' #The {} is for inserting value later, using format()
            k += 1
        table_row = wrap('tr', table_row) #wrap the chunk of <td> with the <tr> tag
        table += table_row  #concatenate all the table row together

    result = wrap('table', table) #wrap the entire thing with the <table> tag
    
    return result

def letter_table(row, col):
    #Create an HTML table filled with randomly generated letter
    #The number of row and col is specified

    temp = random_let(row, col)
    letters = []
    for l in temp:
        ptag = wrap('p class="table"', l)   #extra step to wrap the letter inside a p tag to style it
        letters.append(ptag)

    letters = tuple(letters)    #create a tuple of letters
    
    table = table_gen(row, col) #generate a blank table
    result = table.format(*letters) #insert the letters
    return result

def pic_table(row, col, img_list):
    #Create an HTML table filled with image specified
    imgs_tag = []
    for i in range(len(img_list)):  #generate a list of <img> tag given the images source list
        tag = "<img src='" + img_list[i] + "'>" #since img is a self-closing tag, we don't need to use wrap here
        imgs_tag.append(tag)
    
    imgs_tup = tuple(imgs_tag)  #turn that list into a tuple
    table = table_gen(row, col) #create a blank table
    result = table.format(*imgs_tup)    #insert the image link

    return result

def random_let(row, col):
    #Generate random letter for the random letter table and return a tuple of random letter
    
    n = row*col + 2 #+2 because redundant is better than not enough
    letter_list = []
    for i in range(n):
        index = randrange(65, 123)
        while index in range(91, 97):
            index = randrange(65, 123) #because the character from 91 to 97 is not a letter, so if index in that range, redo 
        letter_list.append(chr(index)) #from number to corresponding character
    
    result = tuple(letter_list) #turn the letter list into a tuple
    return result

def main():
    #THE FIRST HTML CHUNK, CONTAINING CSS AND THE TABLE TITLE
    #NOTE: 
    css_str = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style type="text/css">
        body {{
            background-color: {0};
            }}
        h1{{
            text-align: center; 
            font-size: 36px;
            font-weight: 600;
            }}
        table{{
            border: {1}px solid {2};
            text-align:center;
            border-collapse:collapse; 
            margin-left: auto; 
            margin-right: auto; 
            width: 60%
            }}
        tr td {{
            border: {1}px solid {2};
            background-color: {3}; 
            vertical-align: middle;
            padding: 20px;
            }}
        tr:nth-child(even) td:nth-child(odd), tr:nth-child(odd) td:nth-child(even){{
            background-color: {4};
            }}
        p {{
            text-align: center; 
            font-size: 21px;
            font-weight: 600;
            }}
         p.table{{
            text-align: center; 
            font-size: 21px;
            font-style: bold;
        }}
        img{{
            min-width = 100px !important;
            max-height = 100px !important;
            object-fit: contain;
        }}
    </style>    
    </head>
    <body>
    <h1>{5}</h1>
    '''
    css_values =[]

    #THE SECOND HTML CHUNK, THE TABLE BEGINS
    table_str = ''''''

    #THE THIRD HTML CHUNK, THE AUTHORS AND END TAGS
    authors_str = '''
    <p>Created automatically for COM214 HW1 on {0}</p>
    <p>Authors: {1}</p>

    </body>
    </html>
    '''
    authors_values = []

    #code for reading the file
    with open('config1.txt', 'r') as f:
        bodybg = f.readline()
        bodybg = bodybg[bodybg.find('\t'):].strip()

        cell1 = f.readline()
        cell1 = cell1[cell1.find('\t'):].strip()

        cell2 = f.readline()
        cell2 = cell2[cell2.find('\t'):].strip()

        bordercolor = f.readline()
        bordercolor = bordercolor[bordercolor.find('\t'):].strip()

        borderpx = f.readline()
        borderpx = borderpx[borderpx.find('\t'):].strip()

        authors = f.readline()
        authors = authors[authors.find('\t'):].strip()

        title = f.readline()
        title = title[title.find('\t'):].strip()

        mode = f.readline().lower().strip()

        date = datetime.datetime.now() #footnote require info about time create the document
        date_str = date.strftime(('%a %b %d %I:%M:%S %Y')) #format for creating a datetime string

        #append the values in the list for 1st HTML chunk (CSS)
        css_values.append(bodybg)
        css_values.append(borderpx)
        css_values.append(bordercolor)
        css_values.append(cell1)
        css_values.append(cell2)
        css_values.append(title)
        #append the values in the list for 3rd HTML chunk (authors
        authors_values.append(date_str)
        authors_values.append(authors)

        #insert the values in
        css_str = css_str.format(*tuple(css_values))
        authors_str = authors_str.format(*tuple(authors_values))
        
        
        rows, cols = 0, 0
        if mode == 'images':    #if the user specifies he want a table of images
            imgs = f.readlines()
            #get the table dimension
            row = len(imgs)
            col = imgs[0].count('\t') + 1
            
            #create a list of image link
            imgsList = []
            for item in imgs:
                line = item.split()
                imgsList += line

            #create a table of images
            table_str = pic_table(row, col, imgsList)
            
        elif mode == 'letters':
            #get the table dimension
            dimension = f.readline().split('x')
            row, col = int(dimension[0]), int(dimension[1])

            #create a table of random letters
            table_str = letter_table(row, col)
            

    result = css_str + table_str + authors_str  #concatenate the generated HTML string
    print(result)   #print it on the shell to check
    with open('Your Custom Site.html', 'w') as file:    #write to file
        file.write(result)

main()
