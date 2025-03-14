# Exercise as Medicine MVP

A web application that empowers healthcare professionals to prescribe and monitor exercise as medicine for their patients.

## Features

- Patient Profile Management
- Personalized Exercise Prescriptions
- Progress Tracking
- Real-time Monitoring

## Setup

1. Create a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install streamlit pandas numpy scikit-learn
```

3. Run the application:
```bash
streamlit run src/app.py
```

## Project Structure

```
exercise_as_medicine_mvp/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── data_models.py      # Data models and structures
│   └── mock_data.py        # Sample data for development
├── data/                   # Data storage (for future use)
├── tests/                  # Test files (for future use)
└── README.md              # Project documentation
```

## Next Steps

1. Implement proper database storage
2. Add user authentication
3. Expand exercise library
4. Add video integration
5. Implement progress analytics and reporting# exercise_as_medicine_mvp
