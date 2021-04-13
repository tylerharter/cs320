# P7: Predicting User Interest

## Corrections/Clarifications

Nothing yet. 


## Overview

You are the owner of a retail website. You're planning on running a promotion on 
a laptop and you want to send emails out about it. However, you only want to send it to 
people that may be interested in it so as to now annoy people that aren't interested. 
You're looking to use your data from 2020 to help you predict which users may be 
interested in the promotion. 


## Dataset

You will be given the training and one of the testing portions of a dataset
that has user and log data from a website, found in (train/test1)_users.csv 
and (train/test1)_logs.csv. The users portion contains their 
id for the dataset, their name, their age, their badge (1,2,3 corresponding to 
bronze, silver, and gold levels), and their past purchase amount. 
Each row is one user. 

The logs portion contains visits to the website. Each row is one website visit. 
Each row contains the date, the id of the user that visited the page, their ip address, 
the url that they visited, and the number of minutes spent on the page. 

There are also (train/test1)_y.csv files that contain, for each user, if they would be 
interested in a certain product. In this case, that product is a laptop. 



# Group Part (100%)

First off, this project has no individual part; it's all group work! So feel free to collaborate 
with others in your group. This could take several forms: everyone could tackle some different 
columns of the data, people could try different models, etc. 

The goal of this project is to build a classifier that, given user and log data, 
can predict whether those users will be interested in our product. 
There are a number of ways that you can go about this and a number of ways that you 
can use the data (or not use portions of the data); the freedom is yours.  
  
The only requirements that the tester has for this project are that you have a class 
called `UserPredictor` that can be created like `up = UserPredictor()`, that it has a fit method that can 
be called like `up.fit(train_users, train_logs, train_y)`,
and that it has a function called `up.predict(test1_users, test1_logs)` 
that returns an array of predictions. 
The class should also be in a .py file called 'main.py'. 
  
Your tester will create a UserPredictor instance and call the get_predictions function with the first test set 
and return the accuracy. When we run the tester, it will instead use a second test set, which should 
provide a different, but similar, accuracy.   

Hint: The log csvs contain a lot of helpful information such as 
what items they're interested in and where they're from. 

Hint: The log csvs also contain more logs than there are users (although every user 
may not have any log info). You will need to figure out how you want to 
aggregate this data. 

## Testing/Grade

While the accuracy that the tester returns isn't your score, it is related. 
65% will correspond to a grade of 60% and a 85% accuracy will correspond to a 100.  

The score from the test1 set that you have will be close to your final accuracy, but we 
will be running the tester with a different test2 set. So, your final accuracy may be slightly off 
from the accuracy that you get from test1, so it's best to overshoot the grade that 
you're looking for by a bit!  

Feel free to open up the tester and take a look at what's going on! It has been stripped back a 
little bit to make it a bit less daunting to look at. 

