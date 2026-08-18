# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Question, QuizAttempt

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    history = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'quiz/dashboard.html', {'history': history})

@login_required
def take_quiz(request):
    questions = Question.objects.all()
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected == q.correct_option:
                score += 1
        
        QuizAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=total
        )
        return redirect('dashboard')

    return render(request, 'quiz/take_quiz.html', {
        'questions': questions,
        'quiz_duration_seconds': 120 # 2 minutes timer
    })