# Table Soccer (Kicker) Analytics

A Python application for tracking and analyzing table soccer matches, built with Kivy for the user interface and SQLite for data storage.

## Features

- Track match results between teams of two players each
- View match history and statistics
- Add new players to the system
- Simple, intuitive interface optimized for touch input
- Visual team and score tracking

## Screenshots
*(Screenshots will be added here)*

## Requirements

- Python 3.7 or higher
- Kivy 2.0.0 or higher
- SQLite3 (included in Python standard library)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tablesoccer_analytics.git
   cd tablesoccer_analytics
   ```

2. Install the required dependencies:
   ```bash
   pip install kivy
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Main Interface:
   - Select players by clicking on their names (first two for Team A, next two for Team B)
   - Use the numpad to enter scores
   - Click "Spiel speichern" to save the match
   - Use the navigation buttons to switch between screens

## Project Structure

- `main.py` - Main application entry point
- `entry_screen.py` - Match entry screen with player selection and score input
- `history_screen.py` - Screen for viewing match history
- `db.py` - Database operations and queries
- `config.py` - Configuration settings

## Dependencies

- **Kivy** - Cross-platform Python framework for creating multi-touch applications
  ```
  pip install kivy
  ```

## Database

The application uses SQLite to store match data. The database file (`kicker.db`) will be created automatically in the project directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - 

## Author

Anithos

---

