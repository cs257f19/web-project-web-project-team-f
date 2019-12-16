# About this repository
This is the repository for the term-long database-driven web project in CS 257, Fall 2019.

Contents:
- Main: README.md, Software Design Proposal.pdf, createtable.sql, datasource.py (backend code), testDataSource.py (TDD), webapp.py (flask code)
- Data: directory, contains the raw and processed data along with any metadata
- Personas: directory, contains all personas developed for this project
- UserStories: directory, contains all your team's user stories
- static: directory, contains style.css (CSS file), Adobe Stock images, and Nutrek logo used for site
- templates: directory, contains frontend code nutrek.html (Home), Data.html (About Data), searchResults.html (search results page), and three results pages: allergens.html (Food Allegen), ingredients.html (Ingredient List), and nutrients.html (Nutrition Breakdown)


Known Issues: 
1. On rare occasions (usually after a large number of searches have been performed), suddenly every food search yields 'food is not in our database'. Resolve by cutting the connection and reconnecting to perlman. 

Drawbacks of Dataset:
1. There is inconsistent use of punctuation and/or separating characters (e.g. ,) in .csv cells within in USDA dataset (BFPD_csv_07132018.zip). We handled the “cleaning” special characters out of the dataset in HTML so backend processes were unaffected; however, output in View was clean. We removed instances of "(",")", and ","; however, there is an unknown number of special characters to account for, so an occasional special character may appear in ingredients list.
2. The USDA dataset has duplicate ingredients in each ingredient cell. We have chosen to not delete duplicates in ingredients since they are really ingredients within larger ingredients in a food.
3. Out of 239084 food products in database, USDA has no nutritional data on 162257 foods and no ingredients data on 2544 foods. Probability-wise, user may encounter multiple foods without nutritional data, but this is not an error. If user keeps searching, they will eventually find a food with nutritional data (e.g type granola and hit first search result).
