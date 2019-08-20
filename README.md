# official-website
Official Website for XSible

## Set up & Run server
```bash
# Clone repo and submodules
git clone --recursive https://github.com/xsible/official-website.git
cd official-website

# Setup environment (regular)
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# Running the app
python3 app.py
```

## Pulling changes from `ssd.pytorch` submodule
```bash
# Pull updated changes from submodules only
git submodule update --remote

# Pull updated changes from this repo AND submodules
git pull --recurse-submodules
```