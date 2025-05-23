<h2 align="center">BackCourt Api</h2>
<p align="center"><i>Repository for the BackCourt | NBA Stats & News Api</i></p>

<div align="center">
  
![GitHub top language](https://img.shields.io/github/languages/top/kaikyMoura/BackCourt-api)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ce1f958181d743b98107dbc70dfac5ed)](https://app.codacy.com/gh/kaikyMoura/BackCourt-api/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![Repository size](https://img.shields.io/github/repo-size/kaikyMoura/BackCourt-api)
![Github last commit](https://img.shields.io/github/last-commit/kaikyMoura/BackCourt-api)
![License](https://img.shields.io/aur/license/LICENSE)
![Languages count](https://img.shields.io/github/languages/count/kaikyMoura/BackCourt-api)
<!-- ![Languages count](https://img.shields.io/docker/cloud/build/kaikyMoura/BackCourt-api) -->
</div>


---


### 1. About the Project

This project is a FastAPI-based web scraping API designed to collect and provide advanced basketball statistics from various online sources. The API fetches articles and data related to basketball using web scraping techniques, processes the extracted information, and serves it through RESTful endpoints. Also, it uses the [nba_api](https://github.com/swar/nba_api) retrieve official NBA statistics.

---

### 2. Key Features

- Fetches basketball-related articles from multiple websites
- Extracts relevant data using BeautifulSoup
- Provides endpoints to access filtered and categorized statistics
- Optimized for performance with FastAPI and asynchronous requests
- Supports query parameters to filter data by team, player, source, etc.

---

### 3. Technologies
<p display="inline-block">
  <img alt="python-logo" width="48" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" />
  <img alt="fastapi-logo" width="48" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original-wordmark.svg" />  
  <img alt="swagger-logo" width="48" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/swagger/swagger-original.svg" />
  <img alt="pandas-logo" width="48" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" />
</p>

---

### 4. Installation and Virtual Environment Activation
First, you need to create a virtual environment:
```console
python -m venv venv
or
python3 -m venv venv
```

Then, active it:
```console
# Windows (cmd)
venv\Scripts\activate

# Linux/macOS (bash)
source venv/bin/activate
````

After setting up the environment, install the dependencies:

You can install the dependencies using the requerements.txt file:

```console
pip install -r requirements.txt
```
or install directly using:
```console
pip install fastapi uvicorn requests beautifulsoup4 numpy pandas nba_api
```

---

### 5. Running
``` console
uvicorn app.main:app --reload
```

---

### 6. OpenApi Documentation
- Every new endpoint is automatically added to the documentation.
- You can access the documentation to learn how to use it:

```bash
http://localhost:8000/docs
```

---

### 7. Deployment
The application is deployed on Railway, a cloud platform that simplifies backend and API hosting.

You can access the live API at:

[https://backcourt-api-production.up.railway.app](https://backcourt-api-production.up.railway.app)
<br/>
>⚠️ Please use responsibly to avoid exceeding the free-tier usage limits.

---

### 8. Terms of Use
- This repository has no commercial or business intentions
- All rights are reserved to the [NBA](https://www.nba.com).
- Check the [Terms of Use](https://www.nba.com/termsofuse#ownership-and-use-restrictions) to learn about the usage of the data.
