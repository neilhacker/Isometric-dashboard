# Isometric Registry Dashboard

A real-time dashboard displaying carbon credit issuance data from the Isometric registry, featuring a 3D ASCII art visualization and live ticker feed.

## Features

- **3D ASCII Art Visualization**: Interactive 3D model rendered in ASCII characters
- **Live Credit Statistics**: Real-time display of total credits issued
- **Scrolling Ticker**: Recent issuances displayed in a continuous scrolling ticker
- **Day/Night Theme**: Automatic theme switching based on sunrise/sunset times
- **Dual Timezone Clock**: Displays both London and New York times

## Project Structure

```
.
├── index.html          # Main HTML file with embedded scripts
├── style.css           # All CSS styles
├── main.py             # FastAPI backend server
├── .env.example        # Example environment variables file
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── assets/             # Static assets (fonts, images, 3D models)
    ├── isometric-font.ttf
    ├── iso.stl.txt
    ├── favcon.png
    └── ...
```

## Setup

### Prerequisites

- Python 3.7+
- Node.js (optional, for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ascii-art
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ISOMETRIC_CLIENT_SECRET
   ```

4. **Start the FastAPI server**
   ```bash
   python3 -m uvicorn main:app --reload --port 8000
   ```

5. **Open the dashboard**
   - Open `index.html` in a web browser
   - Or serve it with a local web server:
     ```bash
     python3 -m http.server 8080
     # Then navigate to http://localhost:8080
     ```

## Environment Variables

Create a `.env` file in the root directory with the following:

```
ISOMETRIC_CLIENT_SECRET=your_client_secret_here
```

**Important**: Never commit your `.env` file to version control. The `.env.example` file shows what variables are needed without exposing secrets.

## API Endpoints

The FastAPI server provides two endpoints:

- `GET /issuances` - Returns the 10 most recent credit issuances
- `GET /credits` - Returns the total number of credits issued

## Development

### Running the Server

```bash
python3 -m uvicorn main:app --reload --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Frontend Development

The frontend is a single-page application with:
- Three.js for 3D rendering
- Vanilla JavaScript for interactivity
- External CSS for styling

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

