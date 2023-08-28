#/bin/bash
export PYTHONWARNINGS=default
coverage run -a --concurrency=thread start.py $*
coverage html -i
firefox htmlcov/index.html
