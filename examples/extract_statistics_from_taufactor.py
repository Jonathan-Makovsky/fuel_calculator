import requests
from bs4 import BeautifulSoup

"""
    For installation - in terminal:
        $ pip install requests
        $ pip install beautifulsoup4

    The program gets from the user TAU's course number in format of 'dddd-dddd'
    and prints all the statistics of this course, using the data that is shown
    in https://www.tau-factor.com.

    The program using get request method using requests library with the 
    appropriate parameters for extracting the needed data.
"""
p = {'course_code':'0368-2200'}

# Input and validation check
course_code = input("Enter course number in 'dddd-dddd': ")
if not (len(course_code) == 9 and course_code[0:4].isnumeric() and course_code[4] == '-' and course_code[5:].isnumeric()):
    print('Invalid course name')
    exit()

p['course_code'] = course_code

response = requests.get('https://www.tau-factor.com/api/v1/courses/',params=p)

#print('Response Number: ', response.status_code)
#print(response.text)
#print("++++++++++++++++")

rslt = response.json()['results']
if len(rslt) == 0:
    print('No details for course number:', p['course_code'])
    
else:
    print('All the statistics of course number :', p['course_code'], ':')
    rsp = rslt[0]
    course_name = rsp['most_common_names']

    print(course_name)

    inst = rsp['instances']
    
    for moed in inst:
        year = moed['year']
        semester = moed['semester']
        statics = moed['statistics']
        if statics != None:
            mean = statics['mean']
        else:
            mean = 'None'
        numOfExams = moed['groups'][0]['num_exams']
        #print('num  of exams: ', numOfExams)
        if numOfExams > 0 and mean > 0:
            print('year: ', year, ' semester: ', semester, ' mean: ', mean)
