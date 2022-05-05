# AlgoMarket ![Picture](https://img.shields.io/github/repo-size/Tamaarine/KTMFC) ![Picture](https://img.shields.io/uptimerobot/status/m791588377-b1dbefff25107b3b3be4f8d5)  ![Picture](https://img.shields.io/github/contributors/Tamaarine/KTMFC)

# Table of Contents
1. [Introduction](#intro)
2. [How This Project was Published](#how)
3. [Code Organization](#code)
4. [Deploying Our Code Locally](#local)
5. [Acknowledgement](#ack)
6. [Team Members](#team)

# <a name="intro"></a>Introduction
This project was created for CSE 416 - Software Engineering Class in Stony Brook University. This project was created by a team of five group members. We took inspirations from Fiverr and Patreon and combined it with Algorand, a popular Cryptocurrency. This project was implemented via Django's web framework and the blockchain was a private blockchain running on Docker. 

# <a name="how"></a>How is This Project Was Published
This project is hosted in a Virtual Machine. NGINX web server and WSGI is used to forward the request to the Django web application, then the response is sent back to the client by the WSGI server. 

# <a name="code"></a>Code Organization
The code for our main project can be found by navigating from the main branch into the AlgoMarket folder. There you can find the default django code for running an application found in `manage.py`, and the code to run our sandbox for algorand transactions in `renewl.py`. If you then navigate into the app folder you will find the following important files: 
* `urls.py`: contains all of our url pathways and where they navigate to
* `requests.py`: handles logic involving the POST and GET requests for each of our url pathways
* `views.py`: handles putting the results of `requests.py` into the proper format to be passed into our HTML to generate the website
* `models.py`: contains the structurs of our database models
* `forms.py`: includes the Form objects used by our HTML classes to collect user input

If you would like to see the HTML used to generate our website, go to the templates folder, then the app folder and you will find all of our HTML pages. 

# <a name="local"></a>Deploying Our Code Locally
To locally deploy our project on your machine, you need to `sh` to the folder you store our project in, then run `python manage.py migrate` followed by `python manage.py runserver`. This will make sure the database is properly set up, then start the localhost server that includes our front end and backend. If you make any modifications to the structure of our database, make sure to run `python manage.py makemigrations` to make sure that the updates to the database are applied before you rerun the server. 

# <a name="ack"></a>Acknowledgement
* Thank you Professor Kevin McDonnell for allowing us using his face as part of our presentation.
* Thank you stackoverflow for the countless answers that you have provided for our obscure questions.
* Thank you Shuai for making this class an interesting and relevant course. 

# <a name="team"></a>Team Members
1. Ricky Lu
2. Sydney Walker
3. Wei Wen Zhou
4. Quinten De Man
5. Daniel Wu
