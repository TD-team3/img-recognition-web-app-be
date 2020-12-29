from django.shortcuts import render
from django.core.files.storage import FileSystemStorage  # added
from django.http import HttpResponse
from django.core.files.temp import NamedTemporaryFile


def upload(request):
    if request.method == 'POST':
        recogn_dict = {}
        list_of_files = []  # creating an empty list where all uploaded files will go
        print(request.FILES)
        for file in request.FILES.getlist('myfile'):
            img_temp = NamedTemporaryFile()
            img_temp.write(file.read())
            img_temp.flush()
            print(img_temp.name)
            print(img_temp.tell())

            list_of_files.append(img_temp)  # per passare alla recognition

            # recognized = recognition_function(img_temp)
            recogn_dict[file.name] = recognized


        #for f in request.FILES.getlist('myfile'):  # where myFile is the name= of the HTML tag
            #filename = f.name
            #list_of_files.append(filename)


    return HttpResponse('Ok', status=200)


        # BELOW WE ACCESS THE DICTIONARY
        # THE KEY OF THE DICTIONARY WILL BE THE NAME= OF THE INPUT TAG IN THE HTML FORM (e.g. "myFile")