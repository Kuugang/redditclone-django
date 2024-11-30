
# Reddit Clone


[![Contributors][contributors-shield]][contributors-url] [![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url] [![Issues][issues-shield]][issues-url] [![MIT License][license-shield]][license-url]

  

## Overview

A Reddit-like web application built with Django, offering users the ability to create posts, comments, and interact within different subreddits.


📝 [Functional Requirements](https://github.com/Kuugang/redditclone-django/blob/main/REQUIREMENTS.md)

📊 [Gantt Chart](https://cebuinstituteoftechnology-my.sharepoint.com/:x:/g/personal/jake_bajo_cit_edu/Ee29YTLKZ1pLtF9Xad1_AwoB7-jkcPAkn0pUXL2K43xK2A?e=ADtZYN)

🔗 [ERD](https://lucid.app/lucidchart/97505632-7c36-4a42-8e0b-0c35e601ae62/edit?viewport_loc=472%2C-102%2C3328%2C1664%2C0_0&invitationId=inv_464b9039-4bae-4303-9247-44c7dba671cd)

🎨 [UI/UX](<https://www.figma.com/design/NGYo7aSrLyiRIMNURErlfU/Reddit-Material-Design-Redesign-(Community)?node-id=174-887&node-type=frame&t=mZZ28ghmMMy0gySY-0>)

  

## 🛠 Tech Stack
[![Django][Django.com]][Django-url] [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url] [![HTML][HTML.com]][HTML-url]  [![Javascript][Javascript.com]][Javascript-url] [![Tailwind][Tailwindcss.com]][Tailwind-url]  

  

## 📦 Prerequisites
<div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pip-3775A9?style=for-the-badge&logo=pypi&logoColor=white" alt="pip">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
</div>
  

## 🚀 Installation

1. Clone the repository

```bash
git clone https://github.com/Kuugang/redditclone-django.git
cd redditclone-django
```

  

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

  

3. Install dependencies

```bash
pip install -r requirements.txt
```

  
4. Create .env file

```bash
touch .env
```

5. Configure environment variables in `.env`

```bash
DATABASE_HOST = 'YOUR DATABASE HOST'
DATABASE_NAME = 'YOUR DATABASE NAME'
DATABASE_PORT = 'YOUR DATABASE PORT'
DATABASE_USER = 'YOUR DATABASE USER'
DATABASE_PASSWORD = 'YOUR DATABASE PASSWORD'
GOOGLE_OAUTH_CLIENT_ID= 'YOUR GOOGLE WEB APP OAUTH CLIENT ID'
EMAIL_HOST_USER = 'YOUR EMAIL HOST USER'
EMAIL_HOST_PASSWORD = 'YOUR EMAIL HOST PASSWORD'
```
  
6. Run migrations and seeding

```bash
python manage.py migrate
python manage.py populate_topics
```

7. Collect static files

```bash
python manage.py collectstatic
```

8. Start the development server

```bash
python manage.py runserver
```
## 🔒 Security Note

-   Never commit `.env` file to version control
-   Use a `.gitignore` file to exclude sensitive credentials
-   Rotate credentials periodically
  

## 🤝 Contributing

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request

  
  

## 🎉 Acknowledgements

- Django

- Tailwind CSS

- Flowbite

  

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]:  https://img.shields.io/github/contributors/Kuugang/redditclone-django.svg?style=for-the-badge

[contributors-url]:  https://github.com/Kuugang/redditclone-django/graphs/contributors

[forks-shield]:  https://img.shields.io/github/forks/Kuugang/redditclone-django.svg?style=for-the-badge

[forks-url]:  https://github.com/Kuugang/redditclone-django/network/members

[stars-shield]:  https://img.shields.io/github/stars/Kuugang/redditclone-django.svg?style=for-the-badge

[stars-url]:  https://github.com/Kuugang/redditclone-django/stargazers

[issues-shield]:  https://img.shields.io/github/issues/Kuugang/redditclone-django.svg?style=for-the-badge

[issues-url]:  https://github.com/Kuugang/redditclone-django/issues

[license-shield]:  https://img.shields.io/github/license/Kuugang/redditclone-django.svg?style=for-the-badge

[license-url]:  https://github.com/Kuugang/redditclone-django/blob/master/LICENSE.txt

  

[PostgreSQL-url]:  https://www.postgresql.org/

[PostgreSQL.com]:  https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white

[Python-url]:  https://www.python.org/

[Python.com]:  https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white

[Pip-url]:  https://pip.pypa.io/

[Pip.com]:  https://img.shields.io/badge/pip-3775A9?style=for-the-badge&logo=pypi&logoColor=white

[Django-url]:  https://www.djangoproject.com/

[Django.com]:  https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white

[Tailwind-url]:  https://tailwindcss.com/

[Tailwindcss.com]:  https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white

[HTML-url]:  https://html.com/

[HTML.com]:  https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white

[Javascript-url]:  https://www.javascript.com/

[Javascript.com]:  https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black