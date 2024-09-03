import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Course
from django.views import View
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all().values()
        return JsonResponse(list(courses), safe=False)

    def post(self, request):
        data = json.loads(request.body)
        course = Course.objects.create(
            title=data['title'],
            instructor=data['instructor'],
            duration_weeks=data['duration_weeks']
        )
        return JsonResponse({"id": course.id, "message": "Course created successfully"}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class CourseDetailView(View):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)
        data = {
            "id": course.id, 
            "title": course.title, 
            "instructor": course.instructor, 
            "duration_weeks": course.duration_weeks
        }
        return JsonResponse(data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)
        data = json.loads(request.body)
        course.title = data.get('title', course.title)
        course.instructor = data.get('instructor', course.instructor)
        course.duration_weeks = data.get('duration_weeks', course.duration_weeks)
        course.save()
        return JsonResponse({"message": "Course updated successfully"})

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return JsonResponse({"error": "Course not found"}, status=404)
        course.delete()
        return JsonResponse({"message": "Course deleted successfully"}, status=204)
    

@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all().values()
        return JsonResponse(list(courses), safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        course = Course.objects.create(
            title=data['title'],
            instructor=data['instructor'],
            duration_weeks=data['duration_weeks']
        )
        return JsonResponse({"id": course.id, "message": "Course created successfully"}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)

    if request.method == 'GET':
        data = {
            "id": course.id, 
            "title": course.title, 
            "instructor": course.instructor, 
            "duration_weeks": course.duration_weeks
        }
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        course.title = data.get('title', course.title)
        course.instructor = data.get('instructor', course.instructor)
        course.duration_weeks = data.get('duration_weeks', course.duration_weeks)
        course.save()
        return JsonResponse({"message": "Course updated successfully"})
    elif request.method == 'DELETE':
        course.delete()
        return JsonResponse({"message": "Course deleted successfully"}, status=204)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
