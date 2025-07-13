# Anime Downloader GUI

A modern, user-friendly GUI application for downloading anime episodes using the powerful anipy-api.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Modern GUI** - Clean, responsive interface using themed tkinter
- 🔍 **Easy Search** - Search anime by name with instant results
- 📺 **Multiple Providers** - Uses gogoanime and other reliable sources
- 🎯 **Episode Selection** - Download individual episodes or entire series
- 🎭 **Language Options** - Support for both SUB and DUB versions
- 📱 **Quality Selection** - Choose from 360p to 1080p quality
- 📁 **Custom Download Path** - Set your preferred download location
- 📊 **Progress Tracking** - Real-time download progress with visual feedback
- 🔄 **Background Downloads** - Non-blocking downloads with queue management
- 🛡️ **Error Handling** - Robust error handling with retry mechanisms

## Installation

### Prerequisites

- Python 3.8 or higher
- ffmpeg (for video processing)

### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv ffmpeg

# Clone the repository
git clone <repository-url>
cd anime_downloader

# Install Python dependencies
pip install -r requirements.txt
```

### Other Linux Distributions

```bash
# Install ffmpeg using your package manager
# For Arch Linux: sudo pacman -S ffmpeg
# For Fedora: sudo dnf install ffmpeg
# For CentOS/RHEL: sudo yum install ffmpeg

# Clone and install
git clone <repository-url>
cd anime_downloader
pip install -r requirements.txt
```

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
   - Set video quality (360p-1080p)
   - Set download path

4. **Download:**
   - Click "Download Episode" for single episode
   - Click "Download All Episodes" for complete series

### Advanced Features

#### Custom Download Path
- Click "Browse" to select your preferred download folder
- Default path is `~/Downloads`

#### Batch Downloads
- Select "Download All Episodes" to download the entire anime series
- Downloads run sequentially with progress tracking

#### Quality Selection
- Choose from multiple quality options: 360p, 480p, 720p, 1080p
- Higher quality means larger file sizes

### Desktop Integration

To add to your applications menu:

```bash
# Copy desktop entry (optional)
cp anime_downloader.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

## Screenshots

### Main Interface
The clean, modern interface makes it easy to search and download anime:
- Search bar with instant results
- Episode and quality selection
- Progress tracking with visual feedback

### Search Results
Double-click any anime from the search results to load episode information.

### Download Progress
Real-time progress bars show download status for individual episodes or entire series.

## Technical Details

### Architecture
- **GUI Framework:** tkinter with ttkthemes for modern styling
- **Anime API:** anipy-api for accessing anime sources
- **Download Engine:** Built-in downloader with ffmpeg integration
- **Threading:** Background operations to keep UI responsive

### Supported Formats
- **Video:** MP4, MKV (auto-conversion with ffmpeg)
- **Quality:** 360p, 480p, 720p, 1080p
- **Languages:** SUB (Subtitled) and DUB (Dubbed)

### Providers
Currently supports:
- GoGoAnime (default)
- Additional providers available through anipy-api

## Troubleshooting

### Common Issues

1. **"Provider initialization failed"**
   - Check your internet connection
   - Ensure anipy-api is installed correctly

2. **"Download failed"**
   - Verify ffmpeg is installed and in PATH
   - Check available disk space
   - Try a different quality setting

3. **"Search returns no results"**
   - Try different search terms
   - Check if the anime exists on the provider

4. **GUI appears broken"**
   - Ensure ttkthemes is installed
   - Try running with `python -m tkinter` to test tkinter installation

### Performance Tips

- **Slower downloads:** Try lower quality settings or check your internet connection
- **High memory usage:** Close other applications during large batch downloads
- **GUI freezing:** This shouldn't happen due to threading, but restart if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd anime_downloader

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python src/main.py
```

## Legal Notice

This application is for educational purposes only. Please respect copyright laws and only download anime that you have the legal right to access. The developers are not responsible for any misuse of this software.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [anipy-api](https://github.com/sdaqo/anipy-cli) - The powerful API that makes this possible
- [ttkthemes](https://github.com/rdbende/ttkthemes) - Modern themes for tkinter
- The anime community for inspiration and feedback

---

**Note:** This application requires an active internet connection to search and download anime. Make sure you have sufficient bandwidth and storage space for downloads.
- [License](#license)

## Usage

To create a new repository using this template, follow these steps:

1. Click the "Use this template" button on the main page of the repository.
2. Fill in the necessary details for your new repository.
3. Click "Create repository from template".

You now have a new repository initialized with the predefined structure and files from this template.

## Features

- Standard directory structure
- Example configuration files
- GitHub workflows for dependency review and managing stale issues
- Contribution guidelines and code of conduct

## File Structure

The template repository includes the following structure:

```plaintext
repo-template/
├── docs/
│   └── index.md
├── .github/
│   ├── CODE_OF_CONDUCT.md
│   ├── COMMIT_CONVENTION.md
│   ├── CONTRIBUTING.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── dependency-review.yml
│       └── stale.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.yml
│       ├── feature_request.yml
│       ├── general_inquiry.yml
│       └── config.yml
├── LICENSE
├── README.md
└── .gitignore
```

<details><summary>Expand file structure</summary>

- `docs/`: Contains the documentation files for the repository.

  - `index.md`: Main documentation file.

- `.github/`: Contains the GitHub-specific files for the repository.

  - `CODE_OF_CONDUCT.md`: Code of conduct for the repository.
  - `COMMIT_CONVENTION.md`: Commit message convention for the repository.
  - `CONTRIBUTING.md`: Contribution guidelines for the repository.
  - `PULL_REQUEST_TEMPLATE.md`: Pull request template for the repository.
  - `workflows/`: Contains the GitHub workflows for the repository.
    - `dependency-review.yml`: Workflow for dependency review.
    - `stale.yml`: Workflow for managing stale issues.
  - `ISSUE_TEMPLATE/`: Contains the issue templates for the repository.
    - `bug_report.yml`: Bug report template.
    - `feature_request.yml`: Feature request template.
    - `general_inquiry.yml`: General inquiry template.
    - `config.yml`: Configuration file for the issue templates.

- `LICENSE`: License file for the repository.
- `README.md`: Readme file for the repository.
- `.gitignore`: Git ignore file for the repository.
</details>

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m "feat(feature-name): add new feature"'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Create a new Pull Request.

Please ensure your pull request adheres to the [Code of Conduct](./.github/CODE_OF_CONDUCT.md).

## License

This project is licensed under the CC0 1.0 License. See the [LICENSE](./LICENSE) file for details.



