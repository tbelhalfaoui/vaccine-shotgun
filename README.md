# Vaccine shotgun

*Get your shot, don't miss a slot!*

Regularly ping Doctolib to check for new slots available for the next day.

## Setup

### Python virtual environment
```python
virtualenv venv --python=python3.8
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Copy `config.json.template` to `config.json` and fill in the details.

## Test notification
Send a fake notification to check your setup:
```python
python -m vaccine_shotgun --test
```

## Run
```python
    python -m vaccine_shotgun
```

## Update urls
Currently, only searching in Paris. You can extract new vaccination center URL from a HAR export of the requests while navigating on Doctolib:
```python
    python -m vaccine_shotgun.parse_har
```
Then, update `urls.txt`.

## Troubleshooting
If using Gmail SMTP server, you must (enable less secure apps)[https://myaccount.google.com/lesssecureapps] (not working if 2FA enabled).
