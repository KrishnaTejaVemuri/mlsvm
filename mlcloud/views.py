from django.shortcuts import render
from .forms import ImageForm
from .models import Image
from mysite.settings import BASE_DIR
import os

#ML
from sklearn import svm
import numpy as np
import PIL
#ML

def home(request):
    return render(request, "home.html")

def trainImage(request):
    if request.method=="POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            image.train = True
            image.save()
    else:
        form = ImageForm()
    return render(request, "train.html", {'form':form})

def process_image(image):
    path=os.path.join(BASE_DIR, str(image.url))
    data=os.path.join(BASE_DIR, 'static/haarcascade_frontalface_alt2.xml')
    pil_image = PIL.Image.open(path).convert("L")
    image_array=np.array(pil_image,"uint8")

    return image_array.flatten(), image.name

def train():
    X=[]
    Y=[]
    for image in Image.objects.filter(train=True):
        x, y = process_image(image)
        X.append(x)
        Y.append(y)

    print(X)
    print(Y)
    return (X,Y)

def testImage(request):
    if request.method=="POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            test_image = form.save()
            X,Y = train()
            clf=svm.SVC(kernel='linear',gamma=0.01, C=100)
            clf.fit(X,Y)
            processed_image, answer = process_image(test_image)
            detected_image = clf.predict([processed_image])
            #detected_image = Image.objects.get(pk=pk)
            return render(request, "test.html", {'test_image': test_image, 'detected_image': detected_image})
    else:
        form = ImageForm()

    return render(request, "test.html", {'form':form})