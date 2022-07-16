from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from Image_Upload_Task import settings
from .models import Image
from .form import ImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import psycopg2
from django.core.exceptions import *


conn = psycopg2.connect(database="image_db", user='postgres', password='04mint35', host='127.0.0.1', port='5432')
cursor = conn.cursor()


# Create your views here.
def images(request):
    try:
        keyword = request.GET.get("keyword")
        if keyword:
            images = Image.objects.filter(title__contains=keyword)
            return render(request, "images.html", {"images": images})

        images = Image.objects.all()
        return render(request, "images.html", {"images": images})
    except Image.DoesNotExist:
        return HttpResponse('Exception: Data Not Found')
    except FieldDoesNotExist:
        return HttpResponse("Exception: The Field is Missing!")
    except MultipleObjectsReturned:
        return HttpResponse("Exception: More than one object with the same name are present in the Database")


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    images = Image.objects.filter(author=request.user)
    context = {
        "images": images
    }
    return render(request, "dashboard.html", context=context)


@login_required(login_url="user:login")
def addImage(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        image = form.save(commit=False)
        image.author = request.user
        image.save()
        messages.info(request, 'Image successfully uploaded.')
        return redirect('index')
    return render(request, "add_image.html", {'form': form})


@login_required(login_url="user:login")
def updateImages(request, id):
    cursor.execute('SELECT * from "Image_image" where id = {}'.format(id))
    id_numbers = [item[4] for item in cursor.fetchall()]
    print(id_numbers)
    for id_n in id_numbers:
        if id_n == request.user.id:
            image = get_object_or_404(Image, id=id)
            form = ImageForm(request.POST or None, request.FILES or None, instance=image)
            if form.is_valid():
                image = form.save(commit=False)
                image.author = request.user
                image.save()
                messages.info(request, 'Image successfully updated.')
                return redirect("image:dashboard")

            return render(request, "update.html", {"form": form})
        else:
            messages.info(request, "There is no such image or you are not authorized to edit this image!")
            return redirect("index")


@login_required(login_url="user:login")
def deleteImage(request, id):
    cursor.execute('SELECT * from "Image_image" where id = {}'.format(id))
    id_numbers = [item[4] for item in cursor.fetchall()]
    for id_n in id_numbers:
        if id_n == request.user.id:
            image = get_object_or_404(Image, id=id)
            image.delete()
            messages.info(request, "Image successfully deleted.")
        else:
            messages.info(request, "There is no such image or you are not authorized to edit this image!")
            return redirect("index")
    return redirect("image:dashboard")


def detail(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request, "detail.html", {"image": image})
