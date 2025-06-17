from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Avg
from .models import Question, Result
import random


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    """Main quiz index page."""
    
    def get(self, request):
        """Display the quiz start page."""
        return render(request, 'quiz/index.html')


@method_decorator(login_required, name='dispatch')
class QuizView(View):
    """Main quiz taking functionality."""
    
    def get(self, request):
        """Display quiz questions."""
        # Get 5 random questions
        questions = Question.objects.order_by('?')[:5]
        
        if not questions.exists():
            messages.error(request, 'No questions available. Please contact administrator.')
            return redirect('index_page')
        
        # Store question IDs in session for validation
        request.session['quiz_questions'] = list(questions.values_list('id', flat=True))
        
        context = {
            'questions': questions
        }
        return render(request, 'quiz.html', context)
    
    def post(self, request):
        """Process quiz submission."""
        quiz_questions = request.session.get('quiz_questions', [])
        
        if not quiz_questions:
            messages.error(request, 'Invalid quiz session. Please start again.')
            return redirect('index_page')
        
        questions = Question.objects.filter(id__in=quiz_questions)
        total_questions = questions.count()
        correct_answers = 0
        
        # Check answers
        for i, question in enumerate(questions, 1):
            user_answer = request.POST.get(f'q{i}o')
            if user_answer and user_answer.strip() == question.answer.strip():
                correct_answers += 1
        
        # Save result
        result = Result.objects.create(
            user=request.user,
            total_questions=total_questions,
            correct_answers=correct_answers
        )
        result.calculate_percentage()
        result.save()
        
        # Clear session
        if 'quiz_questions' in request.session:
            del request.session['quiz_questions']
        
        messages.success(
            request, 
            f'Quiz completed! You scored {correct_answers}/{total_questions} '
            f'({result.score_percentage:.1f}%)'
        )
        
        return redirect('result')


@method_decorator(login_required, name='dispatch')
class ResultView(View):
    """Display quiz results."""
    
    def get(self, request):
        """Show user's quiz results."""
        results = Result.objects.filter(user=request.user)
        
        # Calculate average score
        average_score = results.aggregate(
            avg_score=Avg('score_percentage')
        )['avg_score'] or 0
        
        context = {
            'results': results,
            'average_score': round(average_score, 1)
        }
        return render(request, 'results.html', context)