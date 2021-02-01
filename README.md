# Instruction

## Introduction: the application

The main objective is to develop a new online web software to drive a
3d model printer: run process on input model, check the result and send instruction to the printer.

The applications is composed of "pages":

- Three web pages, home, inspector and printer
- Home: list all previous uploaded model
- Inspector: upload new model, run process on it, vizualize the results
- Printer: drive a printer API to send model and read the printer states

## Instructions

A "boilerplate" is provided to lay the foundations but you can bypass
it to provide your own solution, or piece of solution.

You can choose to develop any part of the project, interact with the
team to ask any questions.

You can choose/use any open-source libraries but you _MUST_ give link in
the source code to the library webpage

## Parts description

Pick only tasks you want to develop.

### Frontend

- Develop a modern, pretty web pages with React or Vue.js or any other "modern" framework
- You can find [here](https://preview.uxpin.com/3bb216c737ccee066be5c6b327a4c958c9a903cf#/pages/136070899) the prototype of the application
- Add 3d viewer in the frontend for raw input file and the output
- Drive state of the printer:
  ![State Machine](https://github.com/ORTHOIN3D/interntest/blob/main/modelworkshtop/static/imgs/state-machine.jpg)

### Backend/Infrastructure

- Add all the project in a docker container with a "production ready" configuration
- Currently all the files are store locally, suggest scallable solution to store files and implement it
- Add Endpoint to run algorithms (see Algorithms section), you don't have to implement them, but set all the stuff to call them and store the result
- Add a register/login/logout/reset_password features to the application, ensure the security, a user must not be able to get a model of an other user

### Algorithms

- _Mesh simplification_: simplify the mesh to reduce the file size and decrease computing time. The maximum authorized error is a modification of 0.01 milimeters of a vertex
- _Verification_: verify if the model is ready to be printed by testing if it is watertight (with no holes)
- _Reparation_: if the model is not watertight, repair it
- _Support_: create a support structure if needed according to [this site](https://all3dp.com/1/3d-printing-support-structures/#:~:text=3D%20printing%20support%20structures%20are,added%20cost%20to%20the%20model.)
- _Edges_: find "sharp edges", or "sharp features", by implementing for example: [this article](http://ljk.imag.fr/membres/Stefanie.Hahmann/PUBLICATIONS/WHH10small.pdf)

You can provide your solution integrated to the (python) backend or in a standalone solution.

#### Integrated

- Provide your solution as a python module with instruction to use it
- If you want, you can integrate the solution with the provided backend
- The target python must at least Python3.6
- Provide all depedencies for each algorithms in a requirements.txt file

#### Standalone

- Provide for each algorithm the source code and the instruction to execute and/or compile the executable
- The executable must take the input stl file as first argument
- The second argument of the executable give the path of the result file
- If the result is a new 3d model, the result must be a (binary) stl file
- If the result is a text or numbers, please provide the result as a json file

## Evaluation criteria

- Do not block, ask questions, the test objective is to "simulate" a team work
- Add comments/documentation in your delivery
- Use git and commit regularly, the commit comment will be read, and the quality of the git history will be evaluated
- Quality of code: try to respect the good practices of the using language
- Provide tests
- KISS: keep it simple stupid
- Premature optimization is the root of all evil
- More quality, less quantity
- Reactive, pretty interface for the frontend
- If you add API endpoint, please respect a RESTful philosophy

## Some assets

- The "boilerplate" source code is available [here](https://github.com/ORTHOIN3D/interntest)
- A test stl [test file](https://github.com/ORTHOIN3D/interntest/blob/main/modelworkshtop/static/stl/test.stl) can be used to test algorithms and frontend page (download it)
- Django [here](https://www.djangoproject.com/)
- Django rest framework [here](https://www.django-rest-framework.org/)

## Boilerplate instructions

You can fork and use this project as a starting point for your delivery.
This is a (python) django project

Install the dependencies

```
$ pip install -r requirements.txt
```

Create migrations and initialize (sqlite3) database and collect statics.

```console
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
```

Launch the server

```
$ python manage.py runserver
```

Check the web application got to the [home](http://localhost:8000/static/index.html)
