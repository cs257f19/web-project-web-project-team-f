# About this repository
This is the repository for the term-long database-driven web project in CS 257, Fall 2019.

Contents:
- Main: README.md, Software Design Proposal.pdf, createtable.sql, datasource.py (backend code), testDataSource.py (TDD), webapp.py (flask code)
- Data: directory, contains the raw and processed data along with any metadata
- Personas: directory, contains all personas developed for this project
- UserStories: directory, contains all your team's user stories
- static: directory, contains style.css (CSS file), Adobe Stock images, and Nutrek logo used for site
- templates: directory, contains frontend code nutrek.html (Home), Data.html (About Data), searchResults.html (search results page), and three results pages: allergens.html (Food Allegen), ingredients.html (Ingredient List), and nutrients.html (Nutrition Breakdown)
Note: Data.html has search bar in navigation, so more appropriate in templates.

Drawbacks of Dataset:
1. There is inconsistent use of punctuation and/or separating characters (e.g. ,) in .csv cells within in USDA dataset (BFPD_csv_07132018.zip). We stripped the text clean of only the most common interfering special characters in the ingredients list (i.e. comma, (,),[,],.,and * ). 
2. The USDA dataset ingredients field has duplicates. We have chosen to not delete those ingredient duplicates since they are really ingredients within larger ingredients within a food product.
3. Out of 239084 food products in database, USDA has no nutritional data on 162257 foods and no ingredients data on 2544 foods. Probability-wise, user may encounter multiple foods without nutritional data, but this is not an error. If user keeps searching, they will eventually find a food with nutritional data (e.g type granola and hit first search result).
4. The food allergies query performs a search through ingredients for food allergen input by user. We have no control over the completeness of the database ingredients list. For some foods, there are no ingredients so the food allergen search outputs a message notifying users no ingredient data exists. For foods with a seemingly limited or incomplete set of ingredients, the site will output food allergen is not contained by food since it is limited by whatever USDA put in its ingredients list. Thus if it is obvious a food contains an allergen, but the site says it does not, that means the ingredients list was incomplete/not thorough. 

Known Issues:
-Resolved all known issues as of 12/17/19
