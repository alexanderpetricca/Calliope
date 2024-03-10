# Journal

## Description

Journal is a personal journalling platform built using Django, Bootstrap and Docker.

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

1. Ensure you have docker installed [Docker](https://www.docker.com/)
2. Add .env to root directory containing the following environment variables:
    - "SECRET_KEY= < django secret key >
    - "DJANGO_DEBUG=True
    - "ADMIN_URL= < your chosen admin url >
3. `$ docker-compose up`
4. `$ docker-compose exec web python manage.py migrate`
5. `$ docker-compose exec web python manage.py runserver`
6. Navigate to local host [localhost](http://127.0.0.1:8000/) in your browser


## Screenshots

Homepage

![Homepage](assets/images/JournalHome.jpg)

Journal Entry Page

![Journal Entry Page](assets/images/JournalPost.jpg)


## License

MIT License

Copyright (c) 2022 Alexander Petricca

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


## Features

- Signup
- Journal entry CRUD functionality
- Bookmark / favourite entry
- Search entries
- Update user profile information
- Password reset / forgotten password


## Tests

`$ docker-compose exec web python manage.py test`