# KNUKI University Backend

## Setup

```bash
git clone <repo_url>
cd knuki_uni

python -m venv .venv
source .venv/bin/activate  # windows: .venv\\Scripts\\activate

pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py runserver
