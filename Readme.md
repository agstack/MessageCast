
gunicorn --bind 0.0.0.0:8000 AgStackRegistry.wsgi:application


##This project is built using Django Restframework 


```
All views are thouroughly commented for reference 
```

```
deployed using nginx & gunicorn
```

```
Using postgres database
```




msg (username-timestamp-geolocation)



Django 4.0 was not compatible with django-pwa, so downgraded Django to 3.2


##Elastic search implementation requirements on server

**FOR IMPLEMENTING ELASTIC SEARCH**
-   install java & run the following commands:
-   install elasticsearch version 7.x
-   https://www.alibabacloud.com/knowledge/developer/how-to-install-elasticsearch-on-linux-macos-and-windows


**need to run the following command on screen, i.e. elasticsearch server**
-   ./elasticsearch-7.3.0/bin/elasticsearch
    
**also need to rebuild index after changes in the code**
-   python manage.py search_index --rebuild  
