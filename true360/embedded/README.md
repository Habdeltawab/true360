# Embedded

This is the folder that contains the embedded (hardware) side of the project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Install Python 2.7.*

```
https://www.python.org/downloads/
```

Install Ffmpeg 3.4.1

```
https://www.ffmpeg.org/download.html
```

Install pipevn

```
https://github.com/pypa/pipenv
```
Clone the repository

```
git clone git@git.ece.iastate.edu:sd/sddec18-12.git
```

Go into the embedded directory

```
cd sddec18-12/embedded/
```

Install packages

```
pipenv install
```

## Running Locally

To run locally for development:

Run the python virtual environment

```
pipenv shell
```

Run the script

```
python true360.py
```

## Deploying

To deploy to production:

```shellscript
TBD
```
