import os

import discord
import base64
import ratemyprofessor
import json
import matplotlib.pyplot as plt


client = discord.Client()

authData = "5d5fb173-1f9a-477a-aeda-4832cd1c7392:ENGNPhD73LgiOzbZIdqDKC5JrFr8TDDJ"
authHeaderValue = base64.b64encode(authData.encode('ascii')).decode('ascii')

attendance = []
questions = []
teachers = [271501547219845120]
resources = []


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.channel == client.get_channel(815387717956272186):
        if message.content == 'here':
            attendance.append(message.author.name)
        await message.delete()
    if message.content == 'hello':
        await message.channel.send("Hello, there.")
    elif message.content == 'help':
        await message.channel.send("'add professor 'DISCORD ID': adds a user to the list of professors and gives them access to professor only commands.(PROFESSOR ONLY)'")
        await message.channel.send("'add resource 'URL': adds a URL to the list of resources that students can access.(PROFESSOR ONLY)'")
        await message.channel.send("'resources: shows list of all professor resources that they have added.'")
        await message.channel.send("'here: adds student to list of attendance'")
        await message.channel.send("'attendance: shows list of students that attended class.(PROFESSOR ONLY)'")
        await message.channel.send("'clear attendance: clears list of students for next class.(PROFESSOR ONLY)'")
        await message.channel.send("'? 'QUESTION': adds question to pending question list.'")
        await message.channel.send("'questions: shows all pending questions.'")
        await message.channel.send("'! 'QUESTION NUMBER' 'ANSWER': removes the question from pending questions and adds it to answered questions with an answer.'")
        await message.channel.send("'professor info 'PROFESSOR NAME': Shows professors department and ratemyprofessor ratings.'")
        await message.channel.send("'grade distribution 'SUBJECT''CATALOG NUMBER''SEMESTER''YEAR':\
             Shows grade distributions for all sections and professors.'")
        #grade distribution CS 2336 Summer 2018
    elif message.content.startswith('add professor'):
        for teacher in teachers:
            if message.author.id == teacher:
                teachers.append(int(message.content[13:]))
                await message.channel.send("Professor Added!")
                break
    elif message.content == 'attendance':
        for teacher in teachers:
            if message.author.id == teacher:
                await message.channel.send(attendance)
    elif message.content == 'clear attendance':
        for teacher in teachers:
            if message.author.id == teacher:
                await message.channel.send("Attendance Cleared!")
                attendance.clear()
                break
    elif message.content.startswith('add resource'):
        for teacher in teachers:
            if message.author.id == teacher:
                resources.append(message.content[12:])
                await message.channel.send("Resource Added!")
                break
    elif message.content == 'resources':
        await message.channel.send(resources)
    elif message.content == 'encode key':
        await message.channel.send(base64.b64encode(authData.encode('ascii')).decode('ascii'))
    #elif message.content == 'list professors':
    #   await message.channel.send(ratemyprofessor)
    elif message.content.startswith('?'):
        questions.append(message.content[1:])
        await message.channel.send("Question Added!")
    elif message.content.startswith('!'):
        number = int(message.content[2:3])
        answer = message.content[3:]
        answered_questions[questions[number-1]] = answer
        await message.channel.send("Answer Added to Question " + str(number))
    elif message.content == 'questions':
        for i in range(0,len(questions)):
            await message.channel.send(str(i+1) + ".) " + questions[i])
    elif message.content == 'answered questions':
        for question in answered_questions:
            await message.channel.send(question + "\n\n" + answered_questions[question])
    elif message.content.startswith('professor info'):
        professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of Texas at Dallas"), message.content[14:])
        if professor is not None:
            await message.channel.send("%s works in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
            await message.channel.send("Rating: %s / 5.0" % professor.rating)
            await message.channel.send("Difficulty: %s / 5.0" % professor.difficulty)
            await message.channel.send("Total Ratings: %s" % professor.num_ratings)
            if professor.would_take_again is not None:
                await message.channel.send(("Would Take Again: %s" % round(professor.would_take_again, 1)) + '%')
            else:
                await message.channel.send("Would Take Again: N/A")
        else:
            await message.channel.send("Professor not found")
        await message.channel.send("https://www.ratemyprofessors.com/campusRatings.jsp?sid=1273")
    #Grade Distribution Graph
    #TODO: input validation
    elif message.content.startswith('grade distribution'):
        # Format input
        substr = message.content[19:]
        values = substr.split(' ')
        subj = values[0]
        catalogNum = values[1]
        term = values[3] + ' ' + values[2]
        # Load json file
        if term == '2020 Summer':
            data = open(r'Summer 2020\summer2020.json','r')
        elif term == '2019 Summer':
            data = open(r'Summer 2019\Summer2019.json','r')
        elif term == '2018 Summer':
            data = open(r'Summer 2018\summer2018.json','r')
        elif term == '2020 Spring':
            data = open(r'Spring 2020\spring2020.json','r')
        elif term == '2019 Spring':
            data = open(r'Spring 2019\spring2019.json','r')
        elif term == '2018 Spring':
            data = open(r'Spring 2018\spring2018.json','r')
        elif term == '2019 Fall':
            data = open(r'Fall 2019\Fall2019.json','r')
        elif term == '2018 Fall':
            data = open(r'Fall 2018\fall2018.json','r')
        elif term == '2017 Fall':
            data = open(r'Fall 2017\fall2017.json','r')
        dict = json.load(data)
        # Select class section
        grade_dist = []
        for keyval in dict:
            if term == '2020 Summer':
                if (term.lower() == keyval['term'].lower()) and\
                    (catalogNum.lower() == keyval['Catalog\nNumber'].lower())and (subj.lower() == keyval['subj'].lower()):
                    grade_dist.append(keyval)
            else:
                if (term.lower() == keyval['term'].lower()) and\
                    (catalogNum.lower() == keyval['num'].lower()) and (subj.lower() == keyval['subj'].lower()):
                    grade_dist.append(keyval)
        for distribution in grade_dist:
            # Create arrays with letter grades and their counts
            gradeLetters = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
            gradeCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            grades = distribution['grades']
            for key in grades:
                counter = 0
                for letter in gradeLetters:
                    if key == letter:
                        if type(10) == type(grades[key]):
                            gradeCount[counter] = grades[key]
                        else:
                            gradeCount[counter] = int(grades[key])
                    counter += 1
            # Create bar graph
            fig = plt.figure(figsize=(7,5))
            positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            plt.bar(positions, gradeCount, width=0.5, color=['forestgreen','limegreen','yellowgreen','lime','greenyellow','khaki','gold','orange',\
                'tomato','orangered','red','firebrick','darkred'])
            plt.xticks(positions, gradeLetters)
            plt.ylabel("Number of Students")
            plt.title(subj + " " + catalogNum + "." + distribution['sect'] + "\n" + distribution['prof'] + " - " + term)
            # Display image
            fig.savefig('temp.png')
            myfile = discord.File(open('temp.png', 'rb'))
            await message.channel.send(file=myfile)
        #If no sections of the class were given during the semester
        if len(grade_dist) == 0:
            await message.channel.send("No sections of this class during this semester")
        
client.run("ODE1MjgzODE0MTI1MDEwOTU2.YDqKOA.kRb_d9plY7G2tgqGchZGp_hxeJI")
