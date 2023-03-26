How to run this applicaiton

1)- WITH DOCKER FILE:
    Use these as ENV docker run or edit docker file for these ENVs


     ENV ALLOWED_HOSTS=url-or-hostname-without-port-and-http-s
     ENV CORS_ALLOWED_ORIGINS="http://your-url:3000"
     ENV CSRF_TRUSTED_ORIGINS="http://your-url:3000"
     
     RUN : docker build . -t imagename:tag
     RUN : docker run -p 8000:8000 -d imagename:tag   OR use your ENVs here in this command


2)- WITHOUT DOCKER FILE:
    if want to run without Dockerfile then make changes in /backend/settings.py file
    
    write this:
   
    1)- Add local host or hostname wihtout port and http or https
      ALLOWED_HOSTS = [
        'localhost'
      ]
      
   2)- write hostname or ip with port and http or https
       CORS_ALLOWED_ORIGINS = [
          "http://localhost:3000",
       ]

    3)- write hostname or ip with port and http or https

        CSRF_TRUSTED_ORIGINS = [
          "http://localhost:3000",
          "http://localhost:8000",
        ]   
        
     4)- Comment out these lines of code
         # ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
         # CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
         # CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
         
     5)- RUN commands
     
        RUN : python manage.py runserver
 
     
      
     
     
