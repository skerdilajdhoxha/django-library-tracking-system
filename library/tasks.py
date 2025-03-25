from datetime import timezone
from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    """Really sorry for Copilot, forgot I had it. It autocompletes even this :)"""
    overdue_loans = Loan.objects.filter(due_date__lt=timezone.now().date(), is_returned=False)
    for loan in overdue_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Overdue Book Reminder',
            message=f'Hello {loan.member.user.username},\n\nThe book "{book_title}" is overdue. Please return it as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )

    """If I had a little bit more time I would have fifnished all of the tasks and fixed the bugs. 
    """