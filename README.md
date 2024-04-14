### Install python 🐍
from here: https://www.python.org/downloads/

#### Make sure python installed successfully by checking its version
```
python --version
```

#### Install pipenv to work with virtual environments
```
pip install pipenv
```
```
pipenv --version
```

#### Activate virtual environment to install packages in a separate space
```
pipenv shell
```
or if you want to specific about python version
```
pipenv --python 3.10 shell
```

#### Install packages mentioned in project's requirements.txt file
```
pip install -r requirements.txt
```

#### Make sure django installed successfully by checking its version
```
python -m django --version
```


#### Start server
```
python manage.py runserver
```
