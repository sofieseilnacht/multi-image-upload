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
    g. confirm aws secrets are properly configured
        i. aws s3 ls astrometry-images/
    h. command line copy files to S3/images
        i. one file: aws s3 cp <filename>s3://astrometry-images/pending
            aws s3 cp ~/Desktop/LSQ12hzj.png s3://astrometry-images/pending/LSQ12hzj.png
        ii. many files: aws s3 cp <dirpath>  s3://astrometry-images/pending --recursive  --include "*.png"
            1. example: aws s3 cp ./  s3://astrometry-images/pending --recursive  --include "*.png" --include “*.jpg” —include “*”
            2. example: aws s3 cp ./images  s3://astrometry-images/pending --recursive  --include "*"
            3. example: aws s3 cp ~/Projects/images  s3://astrometry-images/pending —exclude “*” —include “*.fits”
            4. example: aws s3 cp /Users/sofie/Projects/images  s3://astrometry-images/pending —exclude “*” —include “*.fits”
            5. **example:  aws s3 cp ./images/ s3://astrometry-images/pending --recursive  --acl public-read-write --include "*.png"
# astrometry and google configuration files
1. mkdir ~/Projects
2. cd ~/Projects
3. git clone git@github.com:sofieseilnacht/multi-image-upload.git
   a. git pull if the repository is already cloned
        i. git pull git@github.com:sofieseilnacht/multi-image-upload.git
4. mkdir ~/.astrometry
5. #### add secrets to config.ini and google_credentials.json - (astrometry.net api and google credentials)
5. cp myconfig.ini ~/.astrometry
6. open -a TextEdit ~/.astrometry/myconfig.ini
    a. edit myconfig.ini [astrometry.net] apikey
7. cp google_credentials.json ~/.astrometry
8. open -a TextEdit ~/.astrometry/google_credentials.json
    a. edit google_credentials.json to add google apikey
    
# python virtual env setup
1. create virtual env
    a. python3 -m venv ~/venv 
2. activate virtual env
    a. source ~/venv/bin/activate
3. install project dependencies
    a. pip install -r requirements.txt
4. ## deactive will exit the virtual env in the shell

# run the image uploaded program
1. cd ~/Projects/multi-image-upload/
2. activate virtual env with the cmd below
    a. source ~/venv/bin/activate
3. run program 
    a. copy files from local machine to S3 bucket - see aws s3 cp examples above
    a. python main.py
4. exit the virtual env with the cmd below
    a. deactivate 
-- my stuff is in ~/.astrometry
-- edit my stuff in intellij (idea ~/.astrometry/myconfig.ini)
