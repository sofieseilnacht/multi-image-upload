My first python multi-image-upload app.
# multi-image-upload

# setting up pipenv for intellij
https://www.jetbrains.com/help/idea/pipenv.html
 note - in order to use pipenv, need to use python3 (not python3.7)

# theory
http://www.astro.sunysb.edu/metchev/AST443/lecture15.pdf

# relevant documentation
https://astrometrynet.readthedocs.io/en/stable/net/api.html

http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
https://media.readthedocs.org/pdf/astrometrynet/latest/astrometrynet.pdf
https://docs.python-guide.org/scenarios/json/
https://realpython.com/python-json/

http://docs.python-requests.org/en/master/user/quickstart/

# virtualenv notes
project settings - create a python SDK global to projects in ~/venv
settings - set path to pipenv to match venv python (/usr/bin/pip-3.7)

# google API
https://pygsheets.readthedocs.io/en/latest/authorization.html

1. go to https://console.developers.google.com/
2. go to library (sidebar)
3. expand 'G Suite' by clicking on 'View All ...) button
4. click on 'Google Sheet API'
5. enable by clicking on 'Google Sheet API' buttong
4. click on 'Create Credentials'
    a. 'Google Sheets API', 'Other non-UI (e.g. cron job, daemon)', Application Data, 'No, I'm not using them'
    b. service account name: 'astrometry.net'
    c. role: owner
    d. keytype json
5. save the file for later
6. Open up the JSON file, share your spreadsheet with the "XXX-compute@developer.gserviceaccount.com" email listed.
7. Save the JSON file wherever you're hosting your project, you'll need to load it in through Python later.
