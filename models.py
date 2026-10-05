# Question model
class Question(models.Model):
    # Foreign key to Lesson (one lesson can have multiple questions)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # Question text / description
    question_text = models.CharField(max_length=500)
    # Grade point for question
    grade = models.IntegerField(default=1)

    def __str__(self):
        return f"Question: {self.question_text}"

    # Method to calculate if the selected choices get full score
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_incorrect = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        # Full points only if all correct choices are picked and zero incorrect choices are picked
        if all_answers == selected_correct and selected_incorrect == 0:
            return True
        return False


# Choice model
class Choice(models.Model):
    # Foreign key to Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Choice text
    choice_text = models.CharField(max_length=300)
    # Indicates whether this choice is correct
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.choice_text} (Correct: {self.is_correct})"


# Submission model
class Submission(models.Model):
    # Foreign key to Enrollment
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    # Many-to-many relationship with Choice
    choices = models.ManyToManyField(Choice)
    # Submission timestamp
    date = models.DateField(default=now)

    def __str__(self):
        return f"Submission by {self.enrollment.user.username} on {self.enrollment.course.name}"
