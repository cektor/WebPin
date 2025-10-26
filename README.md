# WebPin - Modern Web Application Manager

<div align="center">

![WebPin Logo](webpinlo.png)

**Transform any website into a native desktop application**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GTK](https://img.shields.io/badge/GTK-4.0-green.svg)](https://www.gtk.org/)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Contributing](#contributing)

</div>

---

## 🌟 Features

- **🎨 Modern GTK4/Libadwaita Interface** - Beautiful, native Linux desktop experience
- **🌐 Multi-Browser Support** - Works with Firefox, Chrome, Chromium, Brave, Edge, and more
- **🔒 Isolated Profiles** - Run web apps with separate browser profiles
- **🕶️ Private Mode** - Launch apps in incognito/private browsing mode
- **🎯 Auto Favicon Download** - Automatically fetch and set app icons
- **📊 Usage Statistics** - Track your most used web applications
- **🌍 Multi-Language** - English and Turkish language support
- **🎨 Theme Support** - Light, Dark, and Auto theme modes
- **📤 Import/Export** - Backup and restore your web apps
- **🎁 Easter Egg** - Hidden surprise feature (click the logo 5 times in About!)

## 📋 Requirements

- Python 3.8 or higher
- GTK 4.0
- Libadwaita 1.0
- GObject Introspection
- Python GI bindings
- PIL/Pillow (optional, for better icon handling)

## 🚀 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/cektor/WebPin.git
cd WebPin

# Install dependencies (Debian/Ubuntu)
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adwaita-1 python3-pil

# Install dependencies (Fedora)
sudo dnf install python3-gobject gtk4 libadwaita python3-pillow

# Install dependencies (Arch)
sudo pacman -S python-gobject gtk4 libadwaita python-pillow

# Run the application
python3 webpin.py
```

### System Installation

```bash
# Install to system
sudo cp webpin.py /usr/local/bin/webpin
sudo chmod +x /usr/local/bin/webpin

# Install icon
sudo cp webpinlo.png /usr/share/pixmaps/

# Install desktop file
sudo cp webpin.desktop /usr/share/applications/

# Install language files
sudo mkdir -p /usr/share/webpin/language
sudo cp language/*.ini /usr/share/webpin/language/
```

## 💡 Usage

### Creating a Web App

1. Launch WebPin
2. Click the **+** button
3. Enter the app name and URL
4. (Optional) Click the icon button to auto-download favicon
5. Select your preferred browser
6. Choose a category
7. Configure advanced options if needed
8. Click Save

### Advanced Options

- **Isolated Profile**: Run the app with a separate browser profile
- **Private Window**: Launch in incognito/private mode
- **Custom Variables**: Set environment variables for the app
- **Window Size**: Define custom window dimensions
- **Tags**: Organize apps with custom tags

### Keyboard Shortcuts

- **Search**: Start typing to filter apps
- **Enter**: Launch selected app
- **Delete**: Remove selected app
- **Ctrl+A**: Select all apps

## 🎯 Supported Browsers

- Firefox (all variants)
- Chromium
- Google Chrome
- Brave
- Microsoft Edge
- Vivaldi
- Opera
- Epiphany/GNOME Web
- And many more!

## 📸 Screenshots

*Coming soon*

## 🛠️ Configuration

WebPin stores its configuration in:
- Config: `~/.config/webpin/config.json`
- Language: `~/.config/webpin/language.json`
- Desktop files: `~/.local/share/applications/webapp-*.desktop`
- Icons: `/usr/share/pixmaps/`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fatih ÖNDER (CekToR)**
- GitHub: [@cektor](https://github.com/cektor)
- Website: [algyazilim.com](https://algyazilim.com)

## 🏢 Company

**ALG Yazılım Inc.**
- Website: [algyazilim.com](https://algyazilim.com)
- Email: info@algyazilim.com

## 🙏 Acknowledgments

- GTK and GNOME teams for the amazing toolkit
- All contributors and users of WebPin
- The open-source community

## 🐛 Bug Reports

If you find a bug, please open an issue on [GitHub Issues](https://github.com/cektor/WebPin/issues).

---

<div align="center">

**Made with ❤️ by ALG Yazılım Inc.**

*"The truest guide in life is science."* - M.Kemal ATATÜRK

</div>
