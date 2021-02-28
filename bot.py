import os

import discord
import base64
import ratemyprofessor


client = discord.Client()

authData = "5d5fb173-1f9a-477a-aeda-4832cd1c7392:ENGNPhD73LgiOzbZIdqDKC5JrFr8TDDJ"
authHeaderValue = base64.b64encode(authData.encode('ascii')).decode('ascii')

attendance = []
questions = []
teachers = [271501547219845120]

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
        await message.channel.send("'attendance: shows list of students that attended class.'")
        await message.channel.send("'clear attendance: clears list of students for next class.'")
        await message.channel.send("'? 'QUESTION': adds question to pending question list.'")
        await message.channel.send("'questions: shows all pending questions.'")
        await message.channel.send("'professor info 'PROFESSOR NAME': Shows professors department and ratemyprofessor ratings.'")
    elif message.content == 'attendance':
        await message.channel.send(attendance)
    elif message.content == 'clear attendance':
        await message.channel.send("Attendance Cleared!")
        attendance.clear()
    elif message.content == 'encode key':
        await message.channel.send(base64.b64encode(authData.encode('ascii')).decode('ascii'))
    #elif message.content == 'list professors':
    #   await message.channel.send(ratemyprofessor)
    elif message.content.startswith('?'):
        questions.append(message.content[1:])
    elif message.content == 'questions':
        await message.channel.send(questions)
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
        
        
client.run("ODE1MjgzODE0MTI1MDEwOTU2.YDqKOA.kRb_d9plY7G2tgqGchZGp_hxeJI")
