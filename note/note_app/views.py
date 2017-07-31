from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from note_app.forms import AuthenticateForm, UserCreateForm, NoteForm
from note_app.models import Note
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import rake
import Recommendation
import re
import os
def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        note_form = NoteForm()
        user = request.user
        notes_self = Note.objects.filter(user=user.id)
        notes_buddies = Note.objects.filter(user__userprofile__in=user.profile.follows.all)
        notes = notes_self | notes_buddies
 
        return render(request,
                      'buddies.html',
                      {'note_form': note_form, 'user': user,
                       'notes': notes,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')
 
 
def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')


@login_required
def submit(request):
    if request.method == "POST":
        note_form = NoteForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect(next_url)
        else:
            return public(request, note_form)
    return redirect('/')


@login_required
def public(request, note_form=None):
    note_form = note_form or NoteForm()
    notes = Note.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'note_form': note_form, 'next_url': '/notes',
                   'notes': notes, 'username': request.user.username})
 
def get_latest(user):
    try:
        return user.note_set.order_by('-id')[0]
    except IndexError:
        return ""
 
 
@login_required
def users(request, username="", note_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        notes = Note.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'notes': notes, })
        return render(request, 'user.html', {'user': user, 'notes': notes, 'follow': True, })
    users = User.objects.all().annotate(note_count=Count('note'))
    notes = map(get_latest, users)
    obj = zip(users, notes)
    note_form = note_form or NoteForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'note_form': note_form,
                   'username': request.user.username, })

@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')

#bug 1 solution is to assign to a global heading='' the current heading
#then uset it in instance=note.obje....(heading=heading_global)
global_heading=''
@login_required
def note(request, heading=""):
    if heading:	
        try:
            new_note = Note.objects.get(heading=heading)
            form = NoteForm(request.POST or None, instance=new_note)
            print 'line 142'
            global_heading=heading
        except Note.DoesNotExist:
            redirect('/')
        return render(request, 'detailed_note.html', {'note':new_note, 'form': form})

    if request.POST.get('extract'):
        extractor = rake.Rake(os.getcwd()+'/note_app/SmartStoplist.txt')
        note = Note.objects.get(heading=request.POST['heading'])
        keywords = extractor.run(note.content)
        keywords = [str(keywords[x][0]) for x in range(len(keywords))]
        keywords=str(keywords)[1:-1]
        note.keywords = keywords
        note.save()
        h=request.POST['heading']
        return redirect('/note/'+h)
    
    if request.POST.get('recommend'):
        rec = Recommendation.Recommendation()
        note = Note.objects.get(heading=request.POST['heading'])
        keywords = note.keywords
        keywords = re.sub('[\']', '', keywords)
        keywords = keywords.split(',')
        results = rec.recommend(keywords)

        print keywords
        return render(request, 'recommendation.html', {'results': results}) 
    if request.method == "POST":
        note_form = NoteForm(request.POST, instance=Note.objects.get(heading=request.POST['heading']	))
        #note_form = NoteForm(request.POST, instance=Note.objects.get(heading=global_heading))

        if note_form.is_valid():
            note_form.save()
            h=request.POST['heading']
            return redirect('/note/'+h)


def recommendation(request, form=None):
	if request.method =='POST':
		redirect('/notes')
	
