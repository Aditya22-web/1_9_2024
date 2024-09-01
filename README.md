# Cricket Player Selection Web Application

This project is a web application for selecting cricket players based on pitch conditions and player performance. It features a React.js frontend and a FastAPI backend with machine learning capabilities.

## Prerequisites

- Node.js and npm (for frontend)
- Python 3.8+ (for backend)
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Aditya22-web/1_9_2024.git
   cd 1_9_2024
   ```

2. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```
   cd ../cricket_backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the frontend:
   ```
   cd frontend
   npm start
   ```
   The frontend will be accessible at `http://localhost:3000`

2. Start the backend:
   ```
   cd cricket_backend
   uvicorn app:app --reload
   ```
   The backend API will be available at `http://localhost:8000`

## Features

- 22 input fields for entering cricket player names with autocomplete functionality
- Description box for entering the pitch report
- Submit button to process the input data
- Machine learning model to recommend the best 11 players, including a captain and vice-captain

## Technologies Used

- Frontend: React.js with Chakra UI
- Backend: FastAPI
- Machine Learning: Random Forest Classifier

## Troubleshooting

If you encounter any issues while setting up or running the application, please check the following:

1. Ensure all prerequisites are installed correctly.
2. Make sure you're in the correct directory when running commands.
3. Check if all required packages are installed for both frontend and backend.

If problems persist, please open an issue in the GitHub repository.

## Contributing

Contributions to improve the application are welcome. Please fork the repository and create a pull request with your changes.

## License

[MIT License](https://opensource.org/licenses/MIT)
// Temporary change
