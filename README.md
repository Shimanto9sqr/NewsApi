
---

## ⚙️ Installation & Setup

### Clone the repository
```bash
git clone https://github.com/<your-username>/news-api.git
cd news-api

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload
