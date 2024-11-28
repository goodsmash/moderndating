# DateMe - Modern Dating Platform

A sophisticated dating platform that uses advanced matching algorithms to help users find meaningful connections based on compatibility and shared interests.

## Features

- Smart matching algorithm based on questionnaire responses
- User profiles with photos and detailed information
- Real-time messaging system
- Match suggestions with compatibility scores
- Modern, responsive UI with Bootstrap 5
- Secure authentication and data protection

## Tech Stack

- Python 3.11
- Flask 2.0.1
- SQLAlchemy 1.4.23
- Bootstrap 5.1.3
- SQLite Database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/goodsmash/moderndating.git
cd moderndating
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///dateme.db
```

4. Initialize the database:
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `routes.py`: Application routes
- `forms.py`: Form definitions
- `matching_system.py`: Matching algorithm implementation
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Ryan - [@goodsmash](https://github.com/goodsmash)

Project Link: [https://github.com/goodsmash/moderndating](https://github.com/goodsmash/moderndating)
