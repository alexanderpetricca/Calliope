# Calliope
### Description

Calliope is a personal AI powered journalling platform built using Django, HTMX, OpenAI and the Bootstrap5 grid. The platform uses AI to talk users through completing a daily personal journal. The intent of this project is to experiment with Django and HTMX to create a modern application without a utilising a front end framework, and also to dispel some of the Django 'magic' and develop a deeper understanding of the framework. This project has also allowed me to experiment with OpenAI's API functionality.

This project is currently in development as a side project.

## Table of Contents

- [Calliope](#calliope)
    - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Screenshots](#screenshots)
  - [License](#license)

## Installation

1. Ensure you have docker installed [Docker](https://www.docker.com/)
2. Add .env to root directory containing the following environment variables:
    - SECRET_KEY=**< django secret key >**
    - OPENAI_KEY=**< OpenAI API key >**
    - DJANGO_DEBUG=**< True >**
    - ADMIN_URL=**< your chosen admin url slug >**
3. `$ docker-compose up --build`
4. `$ docker-compose exec web python manage.py migrate`
5. `$ docker-compose exec web python manage.py runserver`
6. Navigate to local host [localhost](http://127.0.0.1:8000/) in your browser


## Screenshots

Homepage

![Listing Page](assets/images/listing-page.jpg)

Journal Entry Page

![Entry Page](assets/images/new-entry-page.jpg)


## License

MIT License

Copyright (c) 2024 Alexander Petricca

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---