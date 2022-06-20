import json
from django.shortcuts import redirect, render
from django.contrib import messages
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    username=''
    if request.user.is_authenticated:
        username = request.user
    context = {'username': username}
    return render(request, 'dashboard/home.html', context)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} Registered Successfully!')
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    if len(homeworks)==0:
        homework_done = True
    else:
        homework_done = False

    if len(todos)==0:
        todo_done = True
    else:
        todo_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/profile.html', context)

@login_required
def notes(request):
    if request.method=="POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            form = NotesForm()
            messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model=Notes

@login_required
def homework(request):
    if request.method=="POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homeworks = Homework(
                user=request.user, 
                subject=request.POST['subject'], 
                title=request.POST['title'], 
                description=request.POST['description'],
                due=request.POST['due'], 
                is_finished = finished
            )
            homeworks.save()
            form = HomeworkForm()
            messages.success(request,f"Homework Added from {request.user.username} Successfully!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done = True
    else:
        homework_done = False

    context = {'homeworks': homework, 'homework_done': homework_done, 'form': form}
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
        
        context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method=="POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todos = Todo(
                user=request.user, 
                title=request.POST['title'],
                is_finished = finished
            )
            todos.save()
            form = TodoForm()
            messages.success(request,f"Todo Added from {request.user.username} Successfully!")
    else:
        form= TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todo_done = True
    else:
        todo_done = False
    context = {'todos': todo, 'form': form, 'todos_done': todo_done}
    return render(request, 'dashboard/todo.html', context)

@login_required
def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            thumb= answer['items'][i]['volumeInfo'].get('imageLinks')
            if thumb:
                result_dict = {
                    'title':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                }
            else:
                result_dict = {
                    'title':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                }
            
            result_list.append(result_dict)
        
        context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    search = False
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + text
        r = requests.get(url)
        answer = r.json()
        
        search = True
        try:
            phonetics=''
            audio=''
            definition=''
            example=''
            synonyms=''

            Jdata = json.loads(json.dumps(answer))
            for data in Jdata:
                for phonetic in data['phonetics']:
                    if 'text' not in phonetic:
                        continue
                    phonetics = phonetic['text']
                    break
                # phonetics = answer[0]['phonetics'][0]['text']

                for phonetic in data['phonetics']:
                    if 'audio' not in phonetic:
                        continue
                    audio = phonetic['audio']
                    break
                # audio = answer[0]['phonetics'][0]['audio']

                for mean in data['meanings']:
                    defn = mean['definitions']
                    for d in defn:
                        if 'definition' not in d or d['definition'] == '':
                            continue
                        definition = d['definition']
                        break
                    if definition:
                        break
                # definition = answer[0]['meanings'][0]['definitions'][0]['definition']

                for mean in data['meanings']:
                    defn = mean['definitions']
                    for d in defn:
                        if 'example' not in d or d['example'] == '':
                            continue
                        example = d['example']
                        break
                    if example:
                        break
                # example = answer[0]['meanings'][0]['definitions'][0]['example']

                for mean in data['meanings']:
                    if 'synonyms' in mean and mean['synonyms'] != '':
                        synonyms = mean['synonyms']
                        break
                    defn = mean['definitions']
                    for d in defn:
                        if 'synonyms' not in d or d['synonyms'] == '':
                            continue
                        synonyms = d['synonyms']
                        break
                    if synonyms:
                        break
                # synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
                'search':search
            }
            # print(context)
        except Exception as e:
            # print(str(e))
            context = {
                'form':form,
                'input':'',
                'search':search
            }
        return render(request, 'dashboard/dictionary.html', context)
    
    form = DashboardForm()
    context = {'form': form, 'input':'', 'search':search}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = WikiForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title':search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)

    form = WikiForm()
    context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        
        if request.POST['measurement'] == 'temperature':
            measurement_form = ConversionTempForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first=='celsius' and second=='fahrenheit':
                        answer= f'{input} \u00B0C = {int(input)*1.8 + 32} \u00B0F'
                    if first=='fahrenheit' and second=='celsius':
                        answer= f'{input} \u00B0F = {(int(input)-32)*5/9} \u00B0C' 
                    if first=='kelvin' and second=='fahrenheit':
                        answer= f'{input} K = {(int(input)-273.15)*1.8 + 32} \u00B0F'
                    if first=='fahrenheit' and second=='kelvin':
                        answer= f'{input} \u00B0F = {(int(input)-32)*5/9 + 273.15} K'
                    if first=='kelvin' and second=='celsius':
                        answer= f'{input} K = {int(input)-273.15} \u00B0C'
                    if first=='celsius' and second=='kelvin':
                        answer= f'{input} \u00B0C = {int(input) + 273.15} K'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first=='yard' and second=='foot':
                        answer= f'{input} yard = {int(input)*3} foot'
                    if first=='foot' and second=='yard':
                        answer= f'{input} foot = {int(input)/3} yard'
                    if first=='meter' and second=='foot':
                        answer= f'{input} meter = {int(input)*3.28084} foot'
                    if first=='foot' and second=='meter':
                        answer= f'{input} foot = {int(input)*0.3048} meter'  
                    if first=='meter' and second=='yard':
                        answer= f'{input} meter = {int(input)*1.09361} yard'
                    if first=='yard' and second=='meter':
                        answer= f'{input} yard = {int(input)*0.9144} meter'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first=='pound' and second=='kilogram':
                        answer= f'{input} pound = {int(input)*0.453592} kilogram'
                    if first=='kilogram' and second=='pound':
                        answer= f'{input} kilogram = {int(input)*2.20462} pound'  
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
    else:    
        form = ConversionForm()
        context= {'form': form, 'input':False}
    return render(request, 'dashboard/conversion.html', context)



