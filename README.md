# official-website
Official Website for XSible

## Setting up
```bash
# Clone repo and submodules
git clone https://github.com/xsible/official-website.git
cd official-website
git submodule update --init --recursive

# Setup environment
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
```