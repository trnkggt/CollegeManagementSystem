from io import BytesIO
from celery import shared_task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def graduation(course_name, student_name, student_last_name, student_email):
    subject = "Graduation Certificate"
    message = f"Dear, {student_name}, congratulations on your graduation of {course_name}. We wish you best of luck."
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [student_email,]
    )

    html = render_to_string('classroom/certificate.html',
                            {"course": course_name,
                             "student_name": student_name,
                             "student_last_name": student_last_name})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    email.attach(f'{course_name}_certificate.pdf',
                 out.getvalue(),
                 "application/pdf")
    email.send()