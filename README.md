# Anime Downloader GUI

A modern, user-friendly GUI application for downloading anime episodes using the powerful anipy-api.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## Features

- 🎨 **Modern GUI** — Clean, responsive interface using ttkbootstrap (themed tkinter)
- 🔍 **Easy Search** — Search anime by name with instant results
- 📺 **Multiple Providers** — Uses AllAnime (default) and other sources via anipy-api
- 🎯 **Episode Selection** — Download individual episodes or entire series
- 🎭 **Language Options** — Support for both SUB and DUB versions
- 📱 **Quality Selection** — Choose from 360p to 1080p quality
- 📁 **Custom Download Path** — Set your preferred download location
- 📊 **Progress Tracking** — Real-time download progress with visual feedback
- 🔄 **Background Downloads** — Non-blocking downloads with queue management
- 🛡️ **Error Handling** — Robust error handling with retry mechanisms

---

## Installation

### Prerequisites

- Python 3.8 or higher
- ffmpeg (for video processing)

### Linux (Ubuntu/Debian/Arch/Other)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg  # Ubuntu/Debian
# For Arch: sudo pacman -S ffmpeg python python-pip

# Clone the repository
git clone <repository-url>
cd anime_downloader

# (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

---

## Usage

### Quick Start

1. **Launch the application:**
   ```bash
   ./run_anime_downloader.sh
   ```
   Or run directly with Python:
   ```bash
   python src/main.py
   ```

2. **Search for anime:**
   - Enter the anime name in the search box
   - Press Enter or click "Search"
   - Double-click on a result to select it

3. **Configure download settings:**
   - Select episode number
   - Choose language (SUB/DUB)
   - Set video quality (360p–1080p)
   - Set download path

4. **Download:**
   - Click "Download Episode" for a single episode
   - Click "Download All Episodes" for the complete series

### Desktop Integration

To add to your applications menu:

```bash
./install.sh
# Then follow the instructions to move the .desktop file:
mv anime_downloader.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

---

## Technical Details

- **GUI Framework:** ttkbootstrap (themed tkinter)
- **Anime API:** anipy-api for accessing anime sources
- **Download Engine:** Built-in downloader with ffmpeg integration
- **Threading:** Background operations to keep UI responsive
- **Supported Formats:** MKV (default), MP4 (if supported by provider)
- **Quality:** 360p, 480p, 720p, 1080p
- **Languages:** SUB (Subtitled) and DUB (Dubbed)
- **Providers:** AllAnime (default), others via anipy-api

---

## Troubleshooting

- **Provider initialization failed:**
  - Check your internet connection
  - Ensure anipy-api is installed correctly
- **Download failed:**
  - Verify ffmpeg is installed and in PATH
  - Check available disk space
  - Try a different quality setting
- **Search returns no results:**
  - Try different search terms
  - Check if the anime exists on the provider
- **GUI appears broken:**
  - Ensure ttkbootstrap and ttkthemes are installed
  - Try running with `python -m tkinter` to test tkinter installation

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd anime_downloader

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python src/main.py
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [anipy-api](https://github.com/sdaqo/anipy-cli) — The powerful API that makes this possible
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) — Modern themes for tkinter
- [ttkthemes](https://github.com/rdbende/ttkthemes) — Additional themes for tkinter
- The anime community for inspiration and feedback

---

**Note:** This application requires an active internet connection to search and download anime. Make sure you have sufficient bandwidth and storage space for downloads.



