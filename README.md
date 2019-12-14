# About this repository
This is the repository for the term-long database-driven web project in CS 257, Fall 2019.

Contents:
- Data: directory, contains the raw and processed data along with any metadata
- Personas: directory, contains all personas developed for this project
- UserStories: directory, contains all your team's user stories
- static: directory, contains style.css (CSS file), Adobe Stock images, and Nutrek logo used for site
- templates: directory, contains nutrek.html (Home), Data.html (About Data), searchResults.html (search results page), and three results pages: allergens.html (Food Allegen), ingredients.html (Ingredient List), and nutrients.html (Nutrition Breakdown)


Known Issues: 
1. [Errno 98]: Address already in use. This error implies that another person may be using our port number but this is not always true. Solution: Exit perlman and re-run. 
2. On rare occassions, every food search yields 'food is not in our database'. This is solved by cutting the connection and reconnecting to perlman. 
