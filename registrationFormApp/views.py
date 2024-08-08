from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Student
from django.utils.crypto import get_random_string
from django.conf import settings

@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        profile_picture = request.FILES.get('profile_picture')

        # Construct a unique file name for the profile picture
        if profile_picture:
            file_extension = profile_picture.name.split('.')[-1]
            unique_filename = f'{request.user.username}_{get_random_string(10)}.{file_extension}'
            profile_picture.name = unique_filename

        student = Student(
            name=name,
            email=email,
            gender=gender,
            age=age,
            profile_picture=profile_picture
        )

        try:
            # Perform file size and type validation
            if profile_picture and profile_picture.size > settings.MAX_UPLOAD_SIZE:
                messages.error(request, 'File size exceeds the maximum limit.')
                return redirect('register')
            elif profile_picture and profile_picture.content_type not in settings.ALLOWED_FILE_TYPES:
                messages.error(request, 'Invalid file type. Please upload an image file.')
                return redirect('register')
            else:
                student.save()
                messages.success(request, 'Student registered successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while registering the student.')
            return redirect('register')

        # Retrieve all the registered students
        students = Student.objects.all()
        return render(request, 'register.html', {'students': students})
    else:
        # Retrieve all the registered students
        students = Student.objects.all()
        return render(request, 'register.html', {'students': students})

@csrf_exempt
def index(request):
    return render(request, 'index.html')