
# Acknowledgements<br/>
•	Bootstrap: https://getbootstrap.com/<br/>
•	Twitter Button: https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/overview <br/>
•	Google Maps API: https://developers.google.com/maps/documentation<br/>
•	JQuery: https://api.jquery.com/ <br/>
•	Feather Icons: https://github.com/feathericons/feather#feather<br/>

# How to deploy

Clone this repository
```
git clone https://github.com/CormacMuir/wad_project.git
```
Navigate into the repo
```
cd wad_project
```
Create a virtual environment using anaconda
```
conda create venv
```
Install from the requirements txt
```
pip install -r requirements.txt
```
Ensure that all migrations have been made
```
Python manage.py makemigrations
```
Apply all migrations
```
python manage.py migrate
```
Execute the population script
```
python populate_script.py
```
Run the server
```
python manage.py runserver
```
