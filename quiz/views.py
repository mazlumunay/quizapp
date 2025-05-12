from django.shortcuts import render, redirect
from .models import Question, Result
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Views for quiz functionality

@login_required(login_url='/login/')
def index_page(request):
    """
    View for displaying the quiz questions and handling quiz submission.

    GET: Renders the quiz page with randomly selected questions.
    POST: Processes the submitted quiz answers, calculates the result, and redirects to the result page.
    """
    questions = Question.objects.order_by('?')[:5]
    context = {'questions': questions}

    if request.method == "GET":
        return render(request, 'quiz.html', context)

    if request.method == "POST":
        questions_id = []
        answers_given = []
        correct_answer = 0
        # Collect answers and corresponding question IDs
        for i in range(1, 6):
            questions_id.append(int(request.POST.get(f'question{i}')))
            answers_given.append(request.POST.get(f'q{i}o'))

        # Check answers and calculate correct answers
        for i in range(len(questions_id)):
            question = Question.objects.get(id=questions_id[i])
            if question.answer == answers_given[i]:
                correct_answer += 1

        # Save result to database
        result = Result(user=request.user)
        result.total = 5
        result.got = correct_answer
        result.save()

        percentage = (correct_answer / 5) * 100

        # Display appropriate message based on the result
        if correct_answer < 3:
            messages.error(request, f'{percentage} % Please try again!')
        elif correct_answer == 3:
            messages.success(request, f'{percentage} % Good Job!')
        elif correct_answer == 4:
            messages.success(request, f'{percentage} % Excellent Work!')
        else:
            messages.success(request, f'{percentage} % You are a genius!')
        return redirect('result')


@login_required(login_url='/login/')
def result(request):
    """
    View for displaying the user's quiz results.

    GET: Renders the results page with the user's quiz history and average score.
    """
    if request.method == "GET":
        results = Result.objects.filter(user=request.user)
        average_score = 0
        if results:
            total_attempt = results.count() * 5
            total_correct = 0

            for result in results:
                total_correct += result.got
            average_score = (total_correct / total_attempt) * 100

        return render(request, 'results.html', {"results": results, "average_score": average_score})
