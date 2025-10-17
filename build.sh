set -o errexit

echo "Using Python version:"
python --version

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate