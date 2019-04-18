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

# S3 bucket access
1. download an S3 aware client application
    a. windows: winscp(https://winscp.net/), cyberduck(https://cyberduck.io/), or filezillapro(https://filezillapro.com/)
2. configure S3 client for access
    a. Bucket name: Full name of the S3 bucket you are connecting to.
    b. Access Key ID: Access Key ID with permissions for this bucket.
    c. Secret Access Key: Secret Access Key with permissions for this bucket.
    d. cyberduck
        i. click '+' to add a new bookmark
        ii. select Amazon S3 as the connection type
        iii. name the connection
        iv. set server to s3-us-west-2.amazonaws.com, port 443
        v. set the access key id to 'b' above
        vi. set the path to the bucket (astrometry-images)
    e. winscp (https://winscp.net/eng/docs/s3)
        i. follow instructions at https://winscp.net/eng/docs/guide_amazon_s3
    f. filezillapro (https://filezillapro.com/)
        i. follow instructions at https://filezillapro.com/connect-amazon-s3/
 