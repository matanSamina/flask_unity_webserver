# Flask webserver for WEBgl games (Unity)

##Open Heroku account :
https://signup.heroku.com

##Open an AWS account :
https://aws.amazon.com/free

On AWS creat an IAM user and add a 


## Initializing Flask app on heroku:
Clone repository (recommended with pycharm)

### Install Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

* On terminal 
```bash
$ heroku git:remote -a <your_heroku_app_name>
```
```bash
$ heroku config:set AWS_ACCESS_KEY_ID=<your_key> AWS_SECRET_ACCESS_KEY=<your_pass>
```
```bash
$ heroku config:set S3_BUCKET=<Your_bucket_name>
```
###references
https://www.stackvidhya.com/write-a-file-to-s3-using-boto3/#using_upload_file



