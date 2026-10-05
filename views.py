from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

# 1. Submit view: Handles exam form submission and grading
@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    # Get or create active enrollment for the current user in this course
    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    if not enrollment:
        enrollment = Enrollment.objects.create(user=user, course=course, mode='audit')
    
    if request.method == 'POST':
        # Create a new submission instance
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Extract selected choice IDs from POST request (e.g. choice_1, choice_2...)
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        # Link chosen choices to this submission
        choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(choices)
        submission.save()
        
        # Redirect to the exam result page
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))
    
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


# 2. Show exam result view: Calculates final score and displays the result template
@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Extract IDs of choices selected in this submission
    selected_choice_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    grade = 0
    
    # Iterate through all questions across all lessons in the course
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            # Use the model method implemented in Task 1
            if question.is_get_score(selected_choice_ids):
                grade += question.grade
                
    # Calculate percentage or pass status (typically 80% or 70% based on course rubrics)
    passed = False
    if total_score > 0 and (grade / total_score) >= 0.7:
        passed = True
        
    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'total_score': total_score,
        'passed': passed,
        'selected_ids': selected_choice_ids,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
