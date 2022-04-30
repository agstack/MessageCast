
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