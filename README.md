# Image Recognition Web App (Back-end)

This project builds a simple image recognition webapp where users can
upload up to 10 images and get a recognition of what each image shows
as a result.\
In order to use the webapp, the user will have to login with a username
and a password, after that he/she will be redirect to the upload page.

Check the front-end documentation for more info:\
https://github.com/TD-team3/img-recognition-web-app-fe

## Framework
The back-end project was built on [Django](https://www.djangoproject.com/).
The server was hosted on [imgrecognitionteam3.pythonanywhere.com]().\

## Project Structure
The Django project was structured in this way: a core **server** folder and
two Django *apps* for implementing the main functionalities of the webapp:
login and upload. The two apps are inside the **authentication_app**
and **upload_app** directories.\
Each app has its own *view* for handling Http requests and returning
responses: they were called respectively `login` and `upload`.

## OOP
The code was written following an OOP approach in order to better organize
functionalities and make the project more testable and adaptable.
Below are the main classes that were used:
- `Authentication`
- `Token`
- `ImgRecognition`
- `ImgRecognitionHandler`

## Request-Response flow and Recognition Output
The used data-interchange format is JSON.
### Authentication phase
The server receives username and password. In case of success,
it returns a token which is valid for 3 hours and gives permission
to access the upload page.
### Upload phase
The server receives username and token as well a file of images (1 to 10).\
In case of success (correct username, valid token, valid images' formats and sizes)\,
it performs recognitions based on a pre-trained model
(ResNet model trained on the ImageNet-1000 dataset)
and after that it returns a JSON with a recognition string for each image name.

