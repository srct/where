# Where
Find stuff at GMU

## Get Started

The backend is written with [Flask](https://flask.palletsprojects.com/en/1.1.x/), a lightweight Python framework for web services.    
To run the backend, first download the dependencies with `pip install -r requirements.txt` in the base directory, then set the `FLASK_APP` environment variable.  

On Mac or Linux:
```
export FLASK_APP=where.app
```
In Windows cmd
```
set FLASK_APP=where.app
```
In Powershell
```
$env:FLASK_APP = where.app
```
After setting `FLASK_APP`, start the development server with `flask run`.  

## Frontend
The frontend is written in Angular, see [where-web](where-web/README.md) for more info

