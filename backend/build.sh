#!/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Check if superuser exists before creating
if
  [ $(echo "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | python manage.py shell) == "False" ];
then
  # Create your super user (check your env vars)
  python manage.py createsuperuser --no-input
fi
