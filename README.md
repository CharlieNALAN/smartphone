### Backend

**1. Install Dependencies**

```
pip install -r requirements.txt
```

**2. Configure the database**

- Create MySQL Database

```
mysql -u root -p
CREATE DATABASE scenic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql -u root -p scenic < scenic.sql
```

- Modify database connection configuration

Open `back_end\settings.py`, modify database connection information：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scenic',
        'USER': 'root',
        'PASSWORD': 'your password',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```



**3. Run the backend**

- Database migration

```
python manage.py makemigrations
python manage.py migrate
```

- Start the development server

```
python manage.py runserver
```



### MiniProgram

1. Use **HbuilderX** to open the project directory (**wx_front**), configure the WeChat Mini Program configuration of the project in the **manifest.json** file, configure the **AppID** of the WeChat Mini Program and the location interface of the Mini Program permission configuration.
1. Select **Run** -> **Run to Mini Program Simulator** -> **WeChat Developer Tools** in the menu bar of HbuilderX to run the project into the WeChat Mini Program Developer Tools.

