#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import tempfile
import urllib.request
import json
import locale
import configparser
from pathlib import Path
from urllib.parse import urlparse
try:
	from PIL import Image
	PIL_AVAILABLE = True
except ImportError:
	PIL_AVAILABLE = False
import gi


			with open(self.config_file, 'w') as f:
				json.dump({'language': self.current_language}, f)
		except:
				pass
	
	def load_translations(self):
		self.translations = {}
		for lang in ['english', 'turkish']:
			lang_file = self.language_dir / f"{lang}.ini"
			if lang_file.exists():
				config = configparser.ConfigParser()
				config.read(lang_file, encoding='utf-8')
				self.translations[lang] = {}
				for section in config.sections():
					self.translations[lang][section] = dict(config[section])
	
	def set_language(self, language):
		if language in self.translations:
			self.current_language = language
			self.save_language_config()

	

		# Zaman damgası ve rastgele karakter ekleyerek benzersiz codename oluştur
		timestamp = str(int(time.time()))[-6:]  # Son 6 hanesi yeterli
		random_str = ''.join(random.choices(string.ascii_lowercase, k=4))
		clean_name = ''.join(c.lower() for c in self.name if c.isalpha())[:6] if self.name else "webapp"
		
		return f"{clean_name}{timestamp}{random_str}"

class WebPinManager:
	def __init__(self):
		self.config_dir = Path.home() / ".config/webpin"
		self.apps_dir = Path.home() / ".local/share/applications"
		# Kullanıcı tarafından belirtilen doğru ikon dizini
		self.icons_dir = Path("/usr/share/pixmaps/")
		 
		# Dizinin varlığını dene (yoksa oluşturmayı dene; izin hatalarını yut)
		try:
			self.icons_dir.mkdir(parents=True, exist_ok=True)
		except Exception as e:
			# izin yoksa devam et; debug için yazdır
			print(f"icons_dir oluşturulamadı: {e}")

		self.config_dir.mkdir(parents=True, exist_ok=True)
		self.apps_dir.mkdir(parents=True, exist_ok=True)
		
		self.config_file = self.config_dir / "config.json"
		self.load_config()

	def load_config(self):
		if self.config_file.exists():
			try:
				with open(self.config_file, 'r') as f:
					self.config = json.load(f)
			except:
				self.config = {"webapps": {}, "settings": {"theme": "auto", "view_mode": "grid"}}
		else:
			self.config = {"webapps": {}, "settings": {"theme": "auto", "view_mode": "grid"}}
			self.save_config()
	
	def save_config(self):
		with open(self.config_file, 'w') as f:
			json.dump(self.config, f, indent=2)
	
	def get_default_browser(self):
		try:
			# xdg-settings ile varsayılan tarayıcıyı al
			result = subprocess.run(['xdg-settings', 'get', 'default-web-browser'], 
								  capture_output=True, text=True, timeout=5)
			if result.returncode == 0:
				desktop_file = result.stdout.strip()
				# .desktop uzantısını kaldır ve tarayıcı komutunu çıkar
				if desktop_file.endswith('.desktop'):
					browser_name = desktop_file[:-8].lower()
					# Bilinen tarayıcı eşleştirmelerini kontrol et
					browser_mapping = {
						'firefox': 'firefox',
						'firefox-esr': 'firefox-esr',
						'firefox-developer-edition': 'firefox-developer-edition',
						'firefox-nightly': 'firefox-nightly',
						'firefox-beta': 'firefox-beta',
						'librewolf': 'librewolf',
						'waterfox': 'waterfox',
						'palemoon': 'palemoon',
						'chromium': 'chromium',
						'chromium-browser': 'chromium-browser',
						'google-chrome': 'google-chrome',
						'google-chrome-stable': 'google-chrome-stable',
						'google-chrome-beta': 'google-chrome-beta',
						'google-chrome-unstable': 'google-chrome-unstable',
						'ungoogled-chromium': 'ungoogled-chromium',
						'brave': 'brave',
						'brave-browser': 'brave-browser',
						'tor-browser': 'tor-browser',
						'mullvad-browser': 'mullvad-browser',
						'microsoft-edge': 'microsoft-edge',
						'microsoft-edge-beta': 'microsoft-edge-beta',
						'microsoft-edge-dev': 'microsoft-edge-dev',
						'vivaldi': 'vivaldi',
						'opera': 'opera',
						'opera-beta': 'opera-beta',
						'opera-developer': 'opera-developer',
						'opera-gx': 'opera-gx',
						'epiphany': 'epiphany',
						'gnome-web': 'gnome-web',
						'midori': 'midori',
						'falkon': 'falkon',
						'konqueror': 'konqueror',
						'seamonkey': 'seamonkey',
						'icecat': 'icecat',
						'basilisk': 'basilisk',
						'min': 'min',
						'qutebrowser': 'qutebrowser',
						'nyxt': 'nyxt',
						'thorium': 'thorium',
						'iridium': 'iridium',
						'iron': 'iron',
						'slimjet': 'slimjet',
						'maxthon': 'maxthon',
						'yandex-browser': 'yandex-browser'
					}
					return browser_mapping.get(browser_name, 'firefox')
		except:
			pass
		return 'firefox'  # Varsayılan olarak firefox döndür
	
	def get_installed_browsers(self):
		browsers = []
		browser_list = [
			# Firefox variants
			("Firefox", "firefox", "/usr/bin/firefox"),
			("Firefox ESR", "firefox-esr", "/usr/bin/firefox-esr"),
			("Firefox Developer Edition", "firefox-developer-edition", "/usr/bin/firefox-developer-edition"),
			("Firefox Nightly", "firefox-nightly", "/usr/bin/firefox-nightly"),
			("Firefox Beta", "firefox-beta", "/usr/bin/firefox-beta"),
			("Librewolf", "librewolf", "/usr/bin/librewolf"),
			("Waterfox", "waterfox", "/usr/bin/waterfox"),
			("Pale Moon", "palemoon", "/usr/bin/palemoon"),
			
			# Chromium variants
			("Chromium", "chromium", "/usr/bin/chromium"),
			("Chromium Browser", "chromium-browser", "/usr/bin/chromium-browser"),
			("Google Chrome", "google-chrome", "/usr/bin/google-chrome"),
			("Google Chrome Stable", "google-chrome-stable", "/usr/bin/google-chrome-stable"),
			("Google Chrome Beta", "google-chrome-beta", "/usr/bin/google-chrome-beta"),
			("Google Chrome Dev", "google-chrome-unstable", "/usr/bin/google-chrome-unstable"),
			("Ungoogled Chromium", "ungoogled-chromium", "/usr/bin/ungoogled-chromium"),
			
			# Privacy-focused browsers
			("Brave", "brave", "/usr/bin/brave"),
			("Brave Browser", "brave-browser", "/usr/bin/brave-browser"),
			("Tor Browser", "tor-browser", "/usr/bin/tor-browser"),
			("Mullvad Browser", "mullvad-browser", "/usr/bin/mullvad-browser"),
			
			# Microsoft browsers
			("Microsoft Edge", "microsoft-edge", "/usr/bin/microsoft-edge"),
			("Microsoft Edge Beta", "microsoft-edge-beta", "/usr/bin/microsoft-edge-beta"),
			("Microsoft Edge Dev", "microsoft-edge-dev", "/usr/bin/microsoft-edge-dev"),
			
			# Other popular browsers
			("Vivaldi", "vivaldi", "/usr/bin/vivaldi"),
			("Opera", "opera", "/usr/bin/opera"),
			("Opera Beta", "opera-beta", "/usr/bin/opera-beta"),
			("Opera Developer", "opera-developer", "/usr/bin/opera-developer"),
			("Opera GX", "opera-gx", "/usr/bin/opera-gx"),
			
			# Webkit-based browsers
			("Epiphany", "epiphany", "/usr/bin/epiphany"),
			("GNOME Web", "gnome-web", "/usr/bin/gnome-web"),
			("Midori", "midori", "/usr/bin/midori"),
			("Luakit", "luakit", "/usr/bin/luakit"),
			("Surf", "surf", "/usr/bin/surf"),
			
			# Alternative browsers
			("Falkon", "falkon", "/usr/bin/falkon"),
			("Konqueror", "konqueror", "/usr/bin/konqueror"),
			("Seamonkey", "seamonkey", "/usr/bin/seamonkey"),
			("Icecat", "icecat", "/usr/bin/icecat"),
			("IceCat", "icecat", "/usr/bin/icecat"),
			("Basilisk", "basilisk", "/usr/bin/basilisk"),
			("Min", "min", "/usr/bin/min"),
			("Qutebrowser", "qutebrowser", "/usr/bin/qutebrowser"),
			("Nyxt", "nyxt", "/usr/bin/nyxt"),
			("Links", "links", "/usr/bin/links"),
			("Lynx", "lynx", "/usr/bin/lynx"),
			("W3M", "w3m", "/usr/bin/w3m"),
			
			# Electron-based browsers
			("Beaker Browser", "beaker", "/usr/bin/beaker"),
			("Franz", "franz", "/usr/bin/franz"),
			("Ferdi", "ferdi", "/usr/bin/ferdi"),
			("Rambox", "rambox", "/usr/bin/rambox"),
			("Station", "station", "/usr/bin/station"),
			
			# Mobile-style browsers
			("Thorium", "thorium", "/usr/bin/thorium"),
			("Iridium", "iridium", "/usr/bin/iridium"),
			("SRWare Iron", "iron", "/usr/bin/iron"),
			("Slimjet", "slimjet", "/usr/bin/slimjet"),
			("Maxthon", "maxthon", "/usr/bin/maxthon"),
			("Yandex Browser", "yandex-browser", "/usr/bin/yandex-browser"),
		]
		
		for name, cmd, path in browser_list:
			if os.path.exists(path) or shutil.which(cmd):
				browsers.append((name, cmd))
		
		return browsers if browsers else [("Firefox", "firefox")]
	
	def export_webapps(self, file_path):
		import time
		try:
			webapps_data = {}
			for webapp in self.get_webapps():
				webapps_data[webapp.codename] = {
					"name": webapp.name,
					"url": webapp.url,
					"icon": webapp.icon,
					"browser": webapp.browser,
					"category": webapp.category,
					"custom_vars": webapp.custom_vars,
					"isolated_profile": webapp.isolated_profile,
					"private_window": webapp.private_window,
					"favorite": getattr(webapp, 'favorite', False),
					"startup": getattr(webapp, 'startup', False),
					"last_used": getattr(webapp, 'last_used', 0),
					"usage_count": getattr(webapp, 'usage_count', 0),
					"window_width": getattr(webapp, 'window_width', 1024),
					"window_height": getattr(webapp, 'window_height', 768),
					"custom_css": getattr(webapp, 'custom_css', ''),
					"tags": getattr(webapp, 'tags', [])
				}
			
			export_data = {
				"version": "2.0",
				"webapps": webapps_data,
				"exported_at": int(time.time())
			}
			with open(file_path, 'w') as f:
				json.dump(export_data, f, indent=2)
			return True
		except:
			return False
	
	def import_webapps(self, file_path):
		try:
			with open(file_path, 'r') as f:
				import_data = json.load(f)
			
			if "webapps" in import_data:
				for codename, webapp_data in import_data["webapps"].items():
					# Create WebApp object with all properties
					webapp = WebApp(
						name=webapp_data.get('name', ''),
						url=webapp_data.get('url', ''),
						icon=webapp_data.get('icon', ''),
						browser=webapp_data.get('browser', 'firefox'),
						category=webapp_data.get('category', 'WebApps'),
						custom_vars=webapp_data.get('custom_vars', ''),
						isolated_profile=webapp_data.get('isolated_profile', False),
						private_window=webapp_data.get('private_window', False)
					)
					
					# Set advanced properties
					webapp.codename = codename
					webapp.favorite = webapp_data.get('favorite', False)
					webapp.startup = webapp_data.get('startup', False)
					webapp.last_used = webapp_data.get('last_used', 0)
					webapp.usage_count = webapp_data.get('usage_count', 0)
					webapp.window_width = webapp_data.get('window_width', 1024)
					webapp.window_height = webapp_data.get('window_height', 768)
					webapp.custom_css = webapp_data.get('custom_css', '')
					webapp.tags = webapp_data.get('tags', [])
					
					# Create desktop file
					self.create_webapp(webapp)
				
				return True
		except:
			pass
		return False
	
	def update_usage_stats(self, webapp):
		import time
		webapp.last_used = int(time.time())
		webapp.usage_count += 1
		
		if webapp.codename in self.config["webapps"]:
			self.config["webapps"][webapp.codename]["last_used"] = webapp.last_used
			self.config["webapps"][webapp.codename]["usage_count"] = webapp.usage_count
			self.save_config()
	
	def get_usage_stats(self):
		stats = []
		for webapp in self.get_webapps():
			stats.append({
				"name": webapp.name,
				"usage_count": getattr(webapp, 'usage_count', 0),
				"last_used": getattr(webapp, 'last_used', 0),
				"url": webapp.url,
				"browser": webapp.browser
			})
		return sorted(stats, key=lambda x: x['usage_count'], reverse=True)
	
	def get_page_title(self, url):
		try:
			if not url.startswith(('http://', 'https://')):
				url = 'https://' + url
			
			req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req, timeout=10) as response:
				if response.status == 200:
					content = response.read().decode('utf-8', errors='ignore')
					# Extract title from HTML
					import re
					title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
					if title_match:
						title = title_match.group(1).strip()
						# Decode HTML entities
						import html
						title = html.unescape(title)
						# Clean up title
						title = re.sub(r'\s+', ' ', title)  # Replace multiple spaces
						return title[:50]  # Limit length
		except:
			pass
		return None
	
	def download_favicon(self, url):
		try:
			if not url.startswith(('http://', 'https://')):
				url = 'https://' + url
			
			parsed = urlparse(url)
			domain = parsed.netloc
			
			favicon_urls = [
				f"https://www.google.com/s2/favicons?domain={domain}&sz=128",
				f"https://www.google.com/s2/favicons?domain={domain}&sz=64",
				f"https://icons.duckduckgo.com/ip3/{domain}.ico",
				f"{parsed.scheme}://{domain}/apple-touch-icon.png",
				f"{parsed.scheme}://{domain}/favicon-32x32.png",
				f"{parsed.scheme}://{domain}/favicon.png",
				f"{parsed.scheme}://{domain}/favicon.ico",
				f"https://www.google.com/s2/favicons?domain={domain}"
			]
			
			best_icon = None
			best_size = 0
			
			for favicon_url in favicon_urls:
				try:
					req = urllib.request.Request(favicon_url, headers={'User-Agent': 'Mozilla/5.0'})
					with urllib.request.urlopen(req, timeout=10) as response:
						if response.status == 200:
							data = response.read()
							if len(data) > 100:
								temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
								temp_file.write(data)
								temp_file.close()
								
							if PIL_AVAILABLE:
								try:
									with Image.open(temp_file.name) as img:
										size = img.width * img.height
										if size > best_size:
											if best_icon:
												os.unlink(best_icon)
											best_icon = temp_file.name
											best_size = size
											if img.width >= 64:
												break
										else:
											os.unlink(temp_file.name)
								except:
									if not best_icon:
										best_icon = temp_file.name
							else:
								return temp_file.name
				except:
					continue
			
			if best_icon and PIL_AVAILABLE:
				try:
					final_path = self.icons_dir / f"favicon_{domain.replace('.', '_')}.png"
					with Image.open(best_icon) as img:
						if img.mode != 'RGBA':
							img = img.convert('RGBA')
						
							if img.width < 48 or img.height < 48:
								img = img.resize((48, 48), Image.Resampling.LANCZOS)
							
						img.save(final_path, 'PNG', optimize=True)
					
					os.unlink(best_icon)
					return str(final_path)
				except:
					pass
			
			return best_icon
		except:
			pass
		return None
	
	def get_webapps(self):
		webapps = []
		for desktop_file in self.apps_dir.glob("webapp-*.desktop"):
			try:
				webapp = self._parse_desktop_file(desktop_file)
				if webapp:
					webapps.append(webapp)
			except Exception as e:
				print(f"Error parsing {desktop_file}: {e}")
		return webapps
	
	def _parse_desktop_file(self, desktop_file):
		webapp = WebApp()
		with open(desktop_file, 'r') as f:
			for line in f:
				line = line.strip()
				if line.startswith("Name="):
					webapp.name = line[5:]
				elif line.startswith("Icon="):
					webapp.icon = line[5:]
				elif line.startswith("X-WebApp-URL="):
					webapp.url = line[13:]
				elif line.startswith("X-WebApp-Browser="):
					webapp.browser = line[17:]
				elif line.startswith("X-WebApp-ID="):
					webapp.codename = line[12:]
				elif line.startswith("Categories="):
					categories = line[11:].replace("GTK;", "").replace(";", "")
					webapp.category = categories
				elif line.startswith("X-WebApp-CustomVars="):
					webapp.custom_vars = line[20:]
				elif line.startswith("X-WebApp-IsolatedProfile="):
					webapp.isolated_profile = line[25:].lower() == "true"
				elif line.startswith("X-WebApp-PrivateWindow="):
					webapp.private_window = line[23:].lower() == "true"
				elif line.startswith("X-WebApp-Favorite="):
					webapp.favorite = line[17:].lower() == "true"
				elif line.startswith("X-WebApp-Startup="):
					webapp.startup = line[16:].lower() == "true"
				elif line.startswith("X-WebApp-LastUsed="):
					webapp.last_used = int(line[17:]) if line[17:].isdigit() else 0
				elif line.startswith("X-WebApp-UsageCount="):
					webapp.usage_count = int(line[19:]) if line[19:].isdigit() else 0
				elif line.startswith("X-WebApp-WindowSize="):
					size_parts = line[19:].split('x')
					if len(size_parts) == 2:
						webapp.window_width = int(size_parts[0]) if size_parts[0].isdigit() else 1024
						webapp.window_height = int(size_parts[1]) if size_parts[1].isdigit() else 768
				elif line.startswith("X-WebApp-CustomCSS="):
					webapp.custom_css = line[18:]
				elif line.startswith("X-WebApp-Tags="):
					webapp.tags = line[13:].split(',') if line[13:] else []
		
		if webapp.name and webapp.url:
			webapp.desktop_file = desktop_file
			if not webapp.codename:
				webapp.codename = webapp._generate_codename()
			return webapp
		return None
	
	def create_webapp(self, webapp):
		# Önceki desktop dosyasını kontrol et ve aynı isimli olan varsa sil (geri uyumluluk)
		for existing_file in self.apps_dir.glob("webapp-*.desktop"):
			try:
				with open(existing_file, 'r') as f:
					content_text = f.read()
					if f"Name={webapp.name}\n" in content_text or f"Name={webapp.name}" in content_text:
						try:
							existing_file.unlink()
						except:
							pass
						break
			except:
				continue

		desktop_file = self.apps_dir / f"webapp-{webapp.codename}.desktop"

		# Desktop içeriğini oluştur (X-WebApp-ID ile benzersiz tanımlayıcı eklenir)
		content = f"""[Desktop Entry]
Version=1.0
Name={webapp.name}
Comment=Web App
Exec={self._get_exec_command(webapp)}
Terminal=false
Type=Application
Icon={webapp.icon}
Categories=GTK;{webapp.category};
StartupWMClass=WebApp-{webapp.codename}
StartupNotify=true
X-WebApp-Browser={webapp.browser}
X-WebApp-URL={webapp.url}
X-WebApp-ID={webapp.codename}
X-WebApp-CustomVars={webapp.custom_vars}
X-WebApp-IsolatedProfile={str(webapp.isolated_profile).lower()}
X-WebApp-PrivateWindow={str(webapp.private_window).lower()}
X-WebApp-Favorite={str(getattr(webapp, 'favorite', False)).lower()}
X-WebApp-Startup={str(getattr(webapp, 'startup', False)).lower()}
X-WebApp-LastUsed={getattr(webapp, 'last_used', 0)}
X-WebApp-UsageCount={getattr(webapp, 'usage_count', 0)}
X-WebApp-WindowSize={getattr(webapp, 'window_width', 1024)}x{getattr(webapp, 'window_height', 768)}
X-WebApp-CustomCSS={getattr(webapp, 'custom_css', '')}
X-WebApp-Tags={','.join(getattr(webapp, 'tags', []))}
"""

		# Desktop dosyasını yaz
		try:
			with open(desktop_file, 'w') as f:
				f.write(content)
		except Exception as e:
			print(f"Error: Failed to write desktop file {desktop_file}: {e}")
			return None

		# Config'e ekle / güncelle
		self.config["webapps"][webapp.codename] = {
			"name": webapp.name,
			"url": webapp.url,
			"icon": webapp.icon,
			"browser": webapp.browser,
			"category": webapp.category,
			"custom_vars": webapp.custom_vars,
			"isolated_profile": webapp.isolated_profile,
			"private_window": webapp.private_window,
			"desktop_file": str(desktop_file)
		}
		self.save_config()

		return desktop_file
	
	def _get_exec_command(self, webapp):
		base_cmd = ""
		
		if "firefox" in webapp.browser:
			base_cmd = f"{webapp.browser} --new-instance --new-window --class=WebApp-{webapp.codename} --name=WebApp-{webapp.codename}"
			if webapp.private_window:
				base_cmd += " --private-window"
			if webapp.isolated_profile:
				base_cmd += f" --profile /tmp/webapp-profile-{webapp.codename}"
		elif "chromium" in webapp.browser or "chrome" in webapp.browser or "brave" in webapp.browser:
			base_cmd = f"{webapp.browser} --app='{webapp.url}' --class=WebApp-{webapp.codename} --name=WebApp-{webapp.codename} --new-window"
			if webapp.private_window:
				base_cmd += " --incognito"
			if webapp.isolated_profile:
				base_cmd += f" --user-data-dir=/tmp/webapp-profile-{webapp.codename}"
			else:
				base_cmd += f" --user-data-dir=/tmp/webapp-{webapp.codename}"
		elif "edge" in webapp.browser:
			base_cmd = f"{webapp.browser} --app='{webapp.url}' --class=WebApp-{webapp.codename} --new-window"
			if webapp.private_window:
				base_cmd += " --inprivate"
		else:
			base_cmd = f"{webapp.browser} --app='{webapp.url}' --class=WebApp-{webapp.codename} --new-window"
		
		# Add custom variables as environment variables
		if webapp.custom_vars:
			env_vars = []
			for var in webapp.custom_vars.split(';'):
				if '=' in var:
					env_vars.append(var.strip())
			if env_vars:
				base_cmd = f"env {' '.join(env_vars)} {base_cmd}"
		
		if "firefox" not in webapp.browser:
			base_cmd += f" '{webapp.url}'"
		else:
			base_cmd += f" '{webapp.url}'"
			
		return base_cmd
	
	def delete_webapp(self, webapp):
		deleted = False
		
		for desktop_file in self.apps_dir.glob("webapp-*.desktop"):
			try:
				with open(desktop_file, 'r') as f:
					content = f.read()
					# Önce X-WebApp-ID ile kontrol et
					if f"X-WebApp-ID={webapp.codename}\n" in content:
						desktop_file.unlink()
						deleted = True
						break
					# Geriye dönük uyumluluk için isim kontrolü
					elif f"Name={webapp.name}\n" in content:
						desktop_file.unlink()
						deleted = True
						break
			except Exception:
				continue
		
		if deleted:
			if webapp.codename in self.config["webapps"]:
				del self.config["webapps"][webapp.codename]
				self.save_config()
			
			# İkonu da sil
			if webapp.icon and webapp.icon.startswith(str(self.icons_dir)):
				try:
					icon_path = Path(webapp.icon)
					if icon_path.exists():
						icon_path.unlink()
				except:
					pass
					
		return deleted
	
	def run_webapp(self, webapp):
		try:
			if hasattr(webapp, 'desktop_file'):
				subprocess.Popen(['gtk-launch', webapp.desktop_file.stem])
			else:
				# Fallback: desktop dosyasını bul ve çalıştır
				for desktop_file in self.apps_dir.glob("webapp-*.desktop"):
					try:
						with open(desktop_file, 'r') as f:
								content = f.read()
								if f"X-WebApp-ID={webapp.codename}\n" in content:
									subprocess.Popen(['gtk-launch', desktop_file.stem])
									break
					except Exception:
						continue
		except Exception as e:
			print(f"Error launching webapp: {e}")

class WebPinWindow(Adw.ApplicationWindow):
	def __init__(self, app):
		dbg("WebPinWindow.__init__ başlıyor")
		super().__init__(application=app)
		self.manager = WebPinManager()
		self.selected_webapp = None
		
		self.set_title("WebPin")
		self.set_default_size(480, 520)
		self.set_resizable(False)
		
		# Apply saved theme
		self.apply_theme()
		
		self.setup_ui()
		self.load_webapps()
		dbg("WebPinWindow.__init__ tamam")
	
	def apply_theme(self):
		theme = self.manager.config.get("settings", {}).get("theme", "auto")
		style_manager = Adw.StyleManager.get_default()
		if theme == "light":
			style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
		elif theme == "dark":
			style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
		else:
			style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
	
	def setup_ui(self):
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.set_content(main_box)
		
		# Minimal header with floating add button
		header = Adw.HeaderBar()
		header.set_title_widget(Gtk.Label(label=lang.get_text('MAIN', 'app_title')))
		header.add_css_class("flat")
		main_box.append(header)
		
		# Menu button
		menu_btn = Gtk.Button()
		menu_btn.set_icon_name("open-menu-symbolic")
		menu_btn.set_tooltip_text(lang.get_text('MAIN', 'menu'))
		menu_btn.add_css_class("circular")
		menu_btn.connect("clicked", self.on_menu_clicked)
		header.pack_start(menu_btn)
		
		# Search entry
		self.search_entry = Gtk.SearchEntry()
		self.search_entry.set_hexpand(True)
		self.search_entry.connect("search-changed", self.on_search_changed)
		header.set_title_widget(self.search_entry)
		
		# View toggle button
		self.view_btn = Gtk.Button()
		self.view_btn.set_icon_name("view-grid-symbolic")
		self.view_btn.set_tooltip_text(lang.get_text('MAIN', 'toggle_view'))
		self.view_btn.add_css_class("circular")
		self.view_btn.connect("clicked", self.on_view_toggle)
		header.pack_end(self.view_btn)
		
		# Floating add button
		add_btn = Gtk.Button()
		add_btn.set_icon_name("list-add-symbolic")
		add_btn.set_tooltip_text(lang.get_text('MAIN', 'add_webapp'))
		add_btn.add_css_class("circular")
		add_btn.add_css_class("suggested-action")
		add_btn.connect("clicked", self.on_add_clicked)
		header.pack_end(add_btn)
		
		# Main content with minimal padding
		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
		content_box.set_margin_top(16)
		content_box.set_margin_bottom(16)
		content_box.set_margin_start(16)
		content_box.set_margin_end(16)
		main_box.append(content_box)
		
		# Selection controls
		selection_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		selection_box.set_margin_bottom(8)
		
		select_all_btn = Gtk.Button(label=lang.get_text('MAIN', 'select_all'))
		select_all_btn.add_css_class("flat")
		select_all_btn.connect("clicked", self.on_select_all)
		selection_box.append(select_all_btn)
		
		self.delete_selected_btn = Gtk.Button(label=lang.get_text('MAIN', 'delete_selected'))
		self.delete_selected_btn.add_css_class("flat")
		self.delete_selected_btn.add_css_class("destructive-action")
		self.delete_selected_btn.set_sensitive(False)
		self.delete_selected_btn.connect("clicked", self.on_delete_selected)
		selection_box.append(self.delete_selected_btn)
		
		content_box.append(selection_box)
		
		# Apps grid container
		scrolled = Gtk.ScrolledWindow()
		scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scrolled.set_vexpand(True)
		scrolled.set_min_content_height(320)
		content_box.append(scrolled)
		
		# Grid for webapp cards
		self.store = Gio.ListStore(item_type=WebApp)
		self.selection = Gtk.MultiSelection(model=self.store)
		self.selection.connect("selection-changed", self.on_selection_changed)
		
		self.grid_view = Gtk.GridView(model=self.selection)
		
		# Set initial view mode from config
		if "settings" not in self.manager.config:
			self.manager.config["settings"] = {"theme": "auto", "view_mode": "grid"}
			self.manager.save_config()
		view_mode = self.manager.config["settings"].get("view_mode", "grid")
		if view_mode == "grid":
			self.grid_view.set_max_columns(2)
			self.view_btn.set_icon_name("view-grid-symbolic")
		else:
			self.grid_view.set_max_columns(1)
			self.view_btn.set_icon_name("view-list-symbolic")
		
		self.grid_view.set_min_columns(1)
		
		# Card factory
		card_factory = Gtk.SignalListItemFactory()
		card_factory.connect("setup", self.setup_card_item)
		card_factory.connect("bind", self.bind_card_item)
		self.grid_view.set_factory(card_factory)
		
		scrolled.set_child(self.grid_view)
		
		# Floating action buttons at bottom
		action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		action_box.set_halign(Gtk.Align.CENTER)
		action_box.set_margin_top(12)
		content_box.append(action_box)
		
		self.run_btn = Gtk.Button()
		self.run_btn.set_icon_name("media-playback-start-symbolic")
		self.run_btn.set_tooltip_text(lang.get_text('MAIN', 'launch'))
		self.run_btn.set_sensitive(False)
		self.run_btn.add_css_class("circular")
		self.run_btn.add_css_class("suggested-action")
		self.run_btn.connect("clicked", self.on_run_clicked)
		action_box.append(self.run_btn)
		
		self.edit_btn = Gtk.Button()
		self.edit_btn.set_icon_name("document-edit-symbolic")
		self.edit_btn.set_tooltip_text(lang.get_text('MAIN', 'edit'))
		self.edit_btn.set_sensitive(False)
		self.edit_btn.add_css_class("circular")
		self.edit_btn.connect("clicked", self.on_edit_clicked)
		action_box.append(self.edit_btn)
		
	
	def on_delete_clicked(self, button):
		selected_count = self.selection.get_selection().get_size()
		
		if selected_count > 1:
			# Multiple selection - use bulk delete
			self.on_delete_selected(button)
		elif selected_count == 1 and self.selected_webapp:
			# Single selection - use individual delete
			self.show_delete_dialog(self.selected_webapp)
	
	def setup_card_item(self, factory, list_item):
		# Modern card design
		card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
		card.add_css_class("card")
		card.set_margin_top(6)
		card.set_margin_bottom(6)
		card.set_margin_start(6)
		card.set_margin_end(6)
		
		# Right-click context menu
		gesture = Gtk.GestureClick()
		gesture.set_button(3)
		gesture.connect("pressed", self.on_card_right_click)
		card.add_controller(gesture)
		
		# Icon container
		icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		icon_box.set_halign(Gtk.Align.CENTER)
		icon_box.set_margin_top(16)
		
		icon = Gtk.Image()
		icon.set_pixel_size(48)
		icon_box.append(icon)
		card.append(icon_box)
		
		# Text container
	
		# Browser badge
		browser_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
		browser_box.set_halign(Gtk.Align.CENTER)
		browser_box.add_css_class("pill")
		browser_box.set_margin_top(4)
		
		browser_icon = Gtk.Image()
		browser_icon.set_pixel_size(12)
		browser_box.append(browser_icon)
		
		browser_label = Gtk.Label()
		browser_label.add_css_class("caption")
		browser_box.append(browser_label)
		
		text_box.append(browser_box)
		card.append(text_box)
		
		list_item.set_child(card)
	
	def bind_card_item(self, factory, list_item):
		webapp = list_item.get_item()
		card = list_item.get_child()
		
		# Get elements
		icon_box = card.get_first_child()
		icon = icon_box.get_first_child()
		
		text_box = card.get_last_child()
		name_label = text_box.get_first_child()
		url_label = text_box.get_first_child().get_next_sibling()
		browser_box = text_box.get_last_child()
		browser_icon = browser_box.get_first_child()
		browser_label = browser_box.get_last_child()
		
	
		# Set text
		name_label.set_text(webapp.name)
		
		# Shorten URL for display
		display_url = webapp.url.replace('https://', '').replace('http://', '')
		if len(display_url) > 25:
			display_url = display_url[:22] + "..."
		url_label.set_text(display_url)
		
		# Set browser info
		browser_icons = {
			'firefox': 'firefox-symbolic',
			'firefox-esr': 'firefox-symbolic', 
			'chromium': 'chromium-symbolic',
			'chromium-browser': 'chromium-symbolic',
			'google-chrome': 'google-chrome-symbolic',
			'google-chrome-stable': 'google-chrome-symbolic',
			'brave': 'brave-symbolic',
			'brave-browser': 'brave-symbolic',
			'microsoft-edge': 'microsoft-edge-symbolic',
			'vivaldi': 'vivaldi-symbolic',
			'opera': 'opera-symbolic'
		}
		
		icon_name = browser_icons.get(webapp.browser, 'web-browser-symbolic')
		browser_icon.set_from_icon_name(icon_name)
		
		# Get short browser name
		browser_names = {
			'firefox': 'Firefox',
			'firefox-esr': 'Firefox', 
			'chromium': 'Chromium',
			'chromium-browser': 'Chromium',
			'google-chrome': 'Chrome',
			'google-chrome-stable': 'Chrome',
			'brave': 'Brave',
			'brave-browser': 'Brave',
			'microsoft-edge': 'Edge',
			'vivaldi': 'Vivaldi',
			'opera': 'Opera'
		}
		
		browser_name = browser_names.get(webapp.browser, webapp.browser.title())
		browser_label.set_text(browser_name)


	def on_search_changed(self, search_entry):
		search_text = search_entry.get_text().lower()
		
		# Clear and reload with filtered results
		self.store.remove_all()
		webapps = self.manager.get_webapps()
		
		for webapp in webapps:
			if (search_text in webapp.name.lower() or 
				search_text in webapp.url.lower() or
				search_text in webapp.browser.lower() or
				search_text in webapp.category.lower()):
				self.store.append(webapp)
		
		# Auto-select first result if available
		if self.store.get_n_items() > 0:
			self.selection.select_item(0, False)

	
	def on_menu_clicked(self, button):
		popover = Gtk.Popover()
		popover.set_parent(button)
		
		menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
		menu_box.set_margin_top(8)
		menu_box.set_margin_bottom(8)
		menu_box.set_margin_start(8)
		menu_box.set_margin_end(8)
		
		# Theme submenu
		theme_btn = Gtk.Button(label=lang.get_text('MAIN', 'theme'))
		theme_btn.add_css_class("flat")
		theme_btn.connect("clicked", lambda x: [popover.popdown(), self.show_theme_menu(button)])
		menu_box.append(theme_btn)
		
		# Language submenu
		lang_btn = Gtk.Button(label=lang.get_text('MAIN', 'language'))
		lang_btn.add_css_class("flat")
		lang_btn.connect("clicked", lambda x: [popover.popdown(), self.show_language_menu(button)])
		menu_box.append(lang_btn)

		
		popover.set_child(menu_box)
		popover.popup()
	
	def on_view_toggle(self, button):
		if "settings" not in self.manager.config:
			self.manager.config["settings"] = {"theme": "auto", "view_mode": "grid"}
		current_mode = self.manager.config["settings"].get("view_mode", "grid")
		new_mode = "list" if current_mode == "grid" else "grid"
		
		self.manager.config["settings"]["view_mode"] = new_mode
		self.manager.save_config()
		
		if new_mode == "grid":
			self.view_btn.set_icon_name("view-grid-symbolic")
			self.grid_view.set_max_columns(2)
		else:
			self.view_btn.set_icon_name("view-list-symbolic")
			self.grid_view.set_max_columns(1)
	
			
		auto_btn = Gtk.Button(label=lang.get_text('THEME', 'auto'))
		auto_btn.add_css_class("flat")
		auto_btn.connect("clicked", lambda x: [popover.popdown(), self.change_theme('auto')])
		theme_box.append(auto_btn)
		
		light_btn = Gtk.Button(label=lang.get_text('THEME', 'light'))
		light_btn.add_css_class("flat")
		light_btn.connect("clicked", lambda x: [popover.popdown(), self.change_theme('light')])
		theme_box.append(light_btn)
		
		dark_btn = Gtk.Button(label=lang.get_text('THEME', 'dark'))
		dark_btn.add_css_class("flat")
		dark_btn.connect("clicked", lambda x: [popover.popdown(), self.change_theme('dark')])
		theme_box.append(dark_btn)
		
		popover.set_child(theme_box)
		popover.popup()
	
	def show_language_menu(self, parent_button):
		popover = Gtk.Popover()
		popover.set_parent(parent_button)
		
		lang_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
		lang_box.set_margin_top(8)
		lang_box.set_margin_bottom(8)
		lang_box.set_margin_start(8)
		lang_box.set_margin_end(8)
		
		english_btn = Gtk.Button(label="English")
		english_btn.add_css_class("flat")
		english_btn.connect("clicked", lambda x: [popover.popdown(), self.change_language('english')])
		lang_box.append(english_btn)
		
		turkish_btn = Gtk.Button(label="Türkçe")
		turkish_btn.add_css_class("flat")
		turkish_btn.connect("clicked", lambda x: [popover.popdown(), self.change_language('turkish')])
		lang_box.append(turkish_btn)
		
		popover.set_child(lang_box)
		popover.popup()
	
	def change_theme(self, theme):
		if "settings" not in self.manager.config:
			self.manager.config["settings"] = {}
		self.manager.config["settings"]["theme"] = theme
		self.manager.save_config()
		self.apply_theme()

	
	def export_webapps(self):
		dialog = Gtk.FileChooserDialog(
			title=lang.get_text('MAIN', 'export_webapps'),
			transient_for=self,
			action=Gtk.FileChooserAction.SAVE
		)
		dialog.add_buttons(
			lang.get_text('DIALOG', 'cancel'), Gtk.ResponseType.CANCEL,
			lang.get_text('DIALOG', 'save'), Gtk.ResponseType.ACCEPT
		)
		
		filter_json = Gtk.FileFilter()
		filter_json.set_name(lang.get_text('FILES', 'json_files'))
		filter_json.add_pattern("*.json")
		dialog.add_filter(filter_json)
		
		dialog.set_current_name(lang.get_text('FILES', 'export_filename'))
		
		dialog.connect("response", self.on_export_response)
		dialog.present()
	
			
		filter_json = Gtk.FileFilter()
		filter_json.set_name(lang.get_text('FILES', 'json_files'))
		filter_json.add_pattern("*.json")
		dialog.add_filter(filter_json)
			
	
			
		count = len(selected_items)
		plural_suffix = 's' if count > 1 else ''
		dialog = Adw.MessageDialog.new(self, lang.get_text('MESSAGES', 'delete_webapps_title'), 
											  lang.get_text('MESSAGES', 'delete_webapps_message', count, plural_suffix))
		dialog.add_response("cancel", lang.get_text('DIALOG', 'cancel'))
		dialog.add_response("delete", lang.get_text('MESSAGES', 'delete'))
		dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
		dialog.selected_items = selected_items
		dialog.connect("response", self.on_delete_selected_response)
		dialog.present()
	
	def on_delete_selected_response(self, dialog, response):
		if response == "delete":
			for webapp in dialog.selected_items:
				self.manager.delete_webapp(webapp)
			self.load_webapps()
			count = len(dialog.selected_items)
			plural_suffix = 's' if count > 1 else ''
			print(lang.get_text('MESSAGES', 'deleted_apps', count, plural_suffix))
		dialog.destroy()
	
	def on_card_right_click(self, gesture, n_press, x, y):
		widget = gesture.get_widget()
		
		# Find which item was clicked by getting the first selected item
		webapp = None
		if self.store.get_n_items() > 0:
			webapp = self.store.get_item(0)  # Use first item as fallback
		
		if not webapp:
			return
		
		# Create and show context menu
		popover = Gtk.Popover()
		popover.set_parent(widget)
		
		rect = Gdk.Rectangle()
		rect.x = int(x)
		rect.y = int(y)
		rect.width = 1
		rect.height = 1
		popover.set_pointing_to(rect)
		
		menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
		menu_box.set_margin_top(8)
		menu_box.set_margin_bottom(8)
		menu_box.set_margin_start(8)
		menu_box.set_margin_end(8)
		
	
	
	def show_delete_dialog(self, webapp):
		dialog = Adw.MessageDialog.new(self, lang.get_text('MESSAGES', 'delete_webapp_title'), 
											  lang.get_text('MESSAGES', 'delete_webapp_message', webapp.name))
		dialog.add_response("cancel", lang.get_text('DIALOG', 'cancel'))
		dialog.add_response("delete", lang.get_text('MESSAGES', 'delete'))
		dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
		dialog.webapp = webapp
		dialog.connect("response", self.on_single_delete_response)
		dialog.present()
	
	def on_single_delete_response(self, dialog, response):
		if response == "delete":
			self.manager.delete_webapp(dialog.webapp)
			self.load_webapps()
			print(lang.get_text('MESSAGES', 'deleted_app', dialog.webapp.name))
		dialog.destroy()
	
	def show_about(self):
		import warnings
		with warnings.catch_warnings():
			warnings.filterwarnings("ignore", category=DeprecationWarning)
			
			self.about_window = Adw.AboutWindow()
			self.about_window.set_transient_for(self)
			self.about_window.set_application_name(lang.get_text('MAIN', 'app_title'))
			self.about_window.set_version(lang.get_text('ABOUT', 'version'))
			self.about_window.set_developer_name(lang.get_text('ABOUT', 'comments'))
			
			# Easter Egg: Logo click counter
			if not hasattr(self, 'logo_click_count'):
				self.logo_click_count = 0
			
			# Uygulama ikonunu ayarla
			logo_path = get_logo_path()
			if logo_path:
				try:
					self.about_window.set_application_icon("webpinlo")
				except Exception as e:
					print(f"About: ikon ayarlama hatası: {e}")
			else:
				try:
					self.about_window.set_application_icon("application-x-executable")
				except:
					pass

			gesture = Gtk.GestureClick()
			gesture.connect("pressed", on_logo_clicked)
			self.about_window.add_controller(gesture)
			
			self.about_window.set_license_type(Gtk.License.MIT_X11)
			
			features_text = "\n\n" + lang.get_text('ABOUT', 'features_title') + ":\n" + "\n".join([
				lang.get_text('ABOUT', 'feature_1'),
				lang.get_text('ABOUT', 'feature_2'),
				lang.get_text('ABOUT', 'feature_3'),
				lang.get_text('ABOUT', 'feature_4'),
				lang.get_text('ABOUT', 'feature_5'),
				lang.get_text('ABOUT', 'feature_6')
			])
			self.about_window.set_comments(lang.get_text('ABOUT', 'comments') + features_text)
			self.about_window.set_website("https://github.com/cektor")
			self.about_window.set_issue_url("https://github.com/cektor/WebPin/issues")
			self.about_window.add_credit_section(lang.get_text('ABOUT', 'developers_title'), [
				"Fatih ÖNDER (CekToR)",
				lang.get_text('ABOUT', 'github_title'),
				"https://github.com/cektor"
			])
			self.about_window.add_credit_section(lang.get_text('ABOUT', 'company_title'), [
				"ALG Yazılım Inc.",
				lang.get_text('ABOUT', 'website_title'),
				"https://algyazilim.com",
				"info@algyazilim.com"
			])
			self.about_window.present()
	
	def show_easter_egg(self):
		dialog = Adw.Window()
		dialog.set_transient_for(self)
		dialog.set_modal(True)
		dialog.set_default_size(500, 550)
		dialog.set_resizable(False)
		dialog.set_title("CekToR has an Easter Egg for you")
		
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		dialog.set_content(main_box)
		
		header = Adw.HeaderBar()
		header.add_css_class("flat")
		main_box.append(header)
		
		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
		content_box.set_margin_top(20)
		content_box.set_margin_bottom(20)
		content_box.set_margin_start(20)
		content_box.set_margin_end(20)
		main_box.append(content_box)
		
		# tr.gif animasyonu
		tr_gif_path = "/usr/share/pixmaps/tr.gif"
		if os.path.exists(tr_gif_path):
			try:
				picture = Gtk.Picture()
				picture.set_filename(tr_gif_path)
				picture.set_content_fit(Gtk.ContentFit.CONTAIN)
				picture.set_size_request(300, 200)
				picture.set_halign(Gtk.Align.CENTER)
				content_box.append(picture)
			except:
				pass
		
		# Alıntı
		quote_label = Gtk.Label()
		quote_label.set_text(lang.get_text('ABOUT', 'easter_egg_quote'))
		quote_label.set_wrap(True)
		quote_label.set_justify(Gtk.Justification.CENTER)
		quote_label.add_css_class("title-4")
		quote_label.set_margin_top(10)
		content_box.append(quote_label)
		
		# Yazar
		author_label = Gtk.Label()
		author_label.set_text(lang.get_text('ABOUT', 'easter_egg_author'))
		author_label.set_halign(Gtk.Align.END)
		author_label.add_css_class("title-3")
		author_label.set_margin_top(10)
		content_box.append(author_label)
		
		# Şirket ve geliştirici bilgisi
		info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
		info_box.set_margin_top(20)
		
		company_label = Gtk.Label()
		company_label.set_text(lang.get_text('ABOUT', 'easter_egg_company'))
		company_label.add_css_class("caption")
		info_box.append(company_label)
		
		developer_label = Gtk.Label()
		developer_label.set_text(lang.get_text('ABOUT', 'easter_egg_developer'))
		developer_label.add_css_class("caption")
		info_box.append(developer_label)
		
		content_box.append(info_box)
		
		if hasattr(self, 'about_window'):
			self.about_window.close()
		dialog.present()

class WebAppDialog(Adw.Window):
	def __init__(self, parent, webapp=None):
		super().__init__()
		self.set_transient_for(parent)
		self.set_modal(True)
		self.set_default_size(420, 520)
		self.set_resizable(False)
		self.parent_window = parent
		self.webapp = webapp
		self.is_edit = webapp is not None
		
		title = lang.get_text('DIALOG', 'edit_webapp') if self.is_edit else lang.get_text('DIALOG', 'new_webapp')
		self.set_title(title)
		
		self.setup_ui()
		if self.is_edit:
			self.populate_fields()
	
	def setup_ui(self):
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.set_content(main_box)
		
		# Minimal header
		header = Adw.HeaderBar()
		title = lang.get_text('DIALOG', 'edit_webapp') if self.is_edit else lang.get_text('DIALOG', 'new_webapp')
		header.set_title_widget(Gtk.Label(label=title))
		header.add_css_class("flat")
		main_box.append(header)
		
		# Save button
		self.save_btn = Gtk.Button()
		self.save_btn.set_icon_name("object-select-symbolic")
		self.save_btn.add_css_class("circular")
		self.save_btn.add_css_class("suggested-action")
		self.save_btn.connect("clicked", self.on_save_clicked)
		header.pack_end(self.save_btn)
		
		# Content with minimal padding
		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
		content_box.set_margin_top(20)
		content_box.set_margin_bottom(20)
		content_box.set_margin_start(20)
		content_box.set_margin_end(20)
		main_box.append(content_box)
		
		# Name field
		name_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		name_label = Gtk.Label(label=lang.get_text('DIALOG', 'name'))
		name_label.set_halign(Gtk.Align.START)
		name_label.add_css_class("caption-heading")
		name_box.append(name_label)
		
		self.name_entry = Gtk.Entry()
		self.name_entry.set_placeholder_text(lang.get_text('PLACEHOLDERS', 'app_name'))
		self.name_entry.connect("changed", self.on_entry_changed)
		name_box.append(self.name_entry)
		content_box.append(name_box)
		
		# URL field
		url_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		url_label = Gtk.Label(label=lang.get_text('DIALOG', 'url'))
		url_label.set_halign(Gtk.Align.START)
		url_label.add_css_class("caption-heading")
		url_box.append(url_label)
		
		url_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		self.url_entry = Gtk.Entry()
		self.url_entry.set_placeholder_text(lang.get_text('PLACEHOLDERS', 'url_placeholder'))
		self.url_entry.set_hexpand(True)
		self.url_entry.connect("changed", self.on_entry_changed)
		self.url_entry.connect("changed", self.on_url_changed)
		url_entry_box.append(self.url_entry)
		
		favicon_btn = Gtk.Button()
		favicon_btn.set_icon_name("image-x-generic-symbolic")
		favicon_btn.set_tooltip_text(lang.get_text('DIALOG', 'get_icon'))
		favicon_btn.add_css_class("circular")
		favicon_btn.connect("clicked", self.on_favicon_clicked)
		url_entry_box.append(favicon_btn)
		
		url_box.append(url_entry_box)
		content_box.append(url_box)
		
		# Icon field with preview
		icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		icon_label = Gtk.Label(label=lang.get_text('DIALOG', 'icon'))
		icon_label.set_halign(Gtk.Align.START)
		icon_label.add_css_class("caption-heading")
		icon_box.append(icon_label)
		
		icon_main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
		
		# Icon preview
		self.icon_preview = Gtk.Image()
		self.icon_preview.set_from_icon_name("application-x-executable")
		self.icon_preview.set_pixel_size(48)
		self.icon_preview.add_css_class("card")
		self.icon_preview.set_margin_top(4)
		self.icon_preview.set_margin_bottom(4)
		self.icon_preview.set_margin_start(8)
		self.icon_preview.set_margin_end(8)
		icon_main_box.append(self.icon_preview)
		
		# Icon entry and buttons
		icon_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		self.icon_entry = Gtk.Entry()
		self.icon_entry.set_placeholder_text(lang.get_text('PLACEHOLDERS', 'icon_path'))
		self.icon_entry.set_hexpand(True)
		self.icon_entry.connect("changed", self.on_icon_entry_changed)
		icon_entry_box.append(self.icon_entry)
		
		icon_picker_btn = Gtk.Button()
		icon_picker_btn.set_icon_name("folder-symbolic")
		icon_picker_btn.set_tooltip_text(lang.get_text('DIALOG', 'browse_icons'))
		icon_picker_btn.add_css_class("circular")
		icon_picker_btn.connect("clicked", self.on_icon_picker_clicked)
		icon_entry_box.append(icon_picker_btn)
		
		icon_entry_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		icon_entry_container.set_vexpand(True)
		icon_entry_container.set_valign(Gtk.Align.CENTER)
		icon_entry_container.append(icon_entry_box)
		icon_main_box.append(icon_entry_container)
		
		icon_box.append(icon_main_box)
		content_box.append(icon_box)
		
		# Browser selection
		browser_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		browser_label = Gtk.Label(label=lang.get_text('DIALOG', 'browser'))
		browser_label.set_halign(Gtk.Align.START)
		browser_label.add_css_class("caption-heading")
		browser_box.append(browser_label)
		
		self.browser_dropdown = Gtk.DropDown()
		self.installed_browsers = self.parent_window.manager.get_installed_browsers()
		string_list = Gtk.StringList()
		for name, cmd in self.installed_browsers:
			string_list.append(name)
		self.browser_dropdown.set_model(string_list)
		
		# Auto-select default browser for new apps
		if not self.is_edit:
			default_browser = self.parent_window.manager.get_default_browser()
			for i, (name, cmd) in enumerate(self.installed_browsers):
				if cmd == default_browser:
					self.browser_dropdown.set_selected(i)
					break
		
		browser_box.append(self.browser_dropdown)
		content_box.append(browser_box)
		
		# Category selection
		category_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		category_label = Gtk.Label(label=lang.get_text('DIALOG', 'category'))
		category_label.set_halign(Gtk.Align.START)
		category_label.add_css_class("caption-heading")
		category_box.append(category_label)
		
		self.category_dropdown = Gtk.DropDown()
		categories = lang.get_categories()
		category_string_list = Gtk.StringList()
		for category in categories:
			category_string_list.append(category)
		self.category_dropdown.set_model(category_string_list)
		self.category_dropdown.set_selected(0)  # Default to WebApps
		
		category_box.append(self.category_dropdown)
		content_box.append(category_box)
		
		# Custom Variables
		vars_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vars_label = Gtk.Label(label=lang.get_text('DIALOG', 'custom_variables'))
		vars_label.set_halign(Gtk.Align.START)
		vars_label.add_css_class("caption-heading")
		vars_box.append(vars_label)
		
		self.vars_entry = Gtk.Entry()
		self.vars_entry.set_placeholder_text(lang.get_text('PLACEHOLDERS', 'custom_vars_placeholder'))
		vars_box.append(self.vars_entry)
		content_box.append(vars_box)
		
		# Options
		options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
		options_label = Gtk.Label(label=lang.get_text('DIALOG', 'options'))
		options_label.set_halign(Gtk.Align.START)
		options_label.add_css_class("caption-heading")
		options_box.append(options_label)
		
		# Isolated Profile
		self.isolated_check = Gtk.CheckButton()
		self.isolated_check.set_label(lang.get_text('DIALOG', 'isolated_profile'))
		options_box.append(self.isolated_check)
		
		# Private Window
		self.private_check = Gtk.CheckButton()
		self.private_check.set_label(lang.get_text('DIALOG', 'private_window'))
		options_box.append(self.private_check)
		
		content_box.append(options_box)
		
		# Advanced options
		advanced_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
		advanced_label = Gtk.Label(label=lang.get_text('DIALOG', 'advanced'))
		advanced_label.set_halign(Gtk.Align.START)
		advanced_label.add_css_class("caption-heading")
		advanced_box.append(advanced_label)
		
		# Favorite checkbox
		self.favorite_check = Gtk.CheckButton()
		self.favorite_check.set_label(lang.get_text('DIALOG', 'add_to_favorites'))
		advanced_box.append(self.favorite_check)
		
		# Startup checkbox
		self.startup_check = Gtk.CheckButton()
		self.startup_check.set_label(lang.get_text('DIALOG', 'launch_at_startup'))
		advanced_box.append(self.startup_check)
		
		# Window size
		size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
		size_label = Gtk.Label(label=lang.get_text('DIALOG', 'window_size') + ":")
		size_box.append(size_label)
		
		self.width_entry = Gtk.Entry()
		self.width_entry.set_text("1024")
		self.width_entry.set_width_chars(6)
		size_box.append(self.width_entry)
		
		x_label = Gtk.Label(label="×")
		size_box.append(x_label)
		
		self.height_entry = Gtk.Entry()
		self.height_entry.set_text("768")
		self.height_entry.set_width_chars(6)
		size_box.append(self.height_entry)
		
		advanced_box.append(size_box)
		
		# Tags entry
		self.tags_entry = Gtk.Entry()
		self.tags_entry.set_placeholder_text(lang.get_text('PLACEHOLDERS', 'tags_placeholder'))
		advanced_box.append(self.tags_entry)
		
		content_box.append(advanced_box)
		
		self.update_save_button()
	

	def on_save_clicked(self, button):
		name = self.name_entry.get_text().strip()
		url = self.url_entry.get_text().strip()
		icon = self.icon_entry.get_text().strip() or "application-x-executable"
		custom_vars = self.vars_entry.get_text().strip()
		isolated_profile = self.isolated_check.get_active()
		private_window = self.private_check.get_active()
		
		selected_index = self.browser_dropdown.get_selected()
		browser = self.installed_browsers[selected_index][1]
		
		if not url.startswith(('http://', 'https://')):
			url = 'https://' + url
		
		selected_category_index = self.category_dropdown.get_selected()
		categories = lang.get_categories()
		category = categories[selected_category_index]
		
		if self.is_edit:
			# Preserve existing webapp properties when editing
			old_webapp = self.webapp
			selected_position = None
			
			# Find current position in store
			for i in range(self.parent_window.store.get_n_items()):
				item = self.parent_window.store.get_item(i)
				if item.codename == old_webapp.codename:
					selected_position = i
					break
			
			self.parent_window.manager.delete_webapp(old_webapp)
			
			webapp = WebApp(name, url, icon, browser, category, custom_vars, isolated_profile, private_window)
			webapp.codename = old_webapp.codename

			webapp.favorite = getattr(old_webapp, 'favorite', False)
			webapp.startup = getattr(old_webapp, 'startup', False)
			webapp.last_used = getattr(old_webapp, 'last_used', 0)
			webapp.usage_count = getattr(old_webapp, 'usage_count', 0)
			webapp.window_width = getattr(old_webapp, 'window_width', 1024)
			webapp.window_height = getattr(old_webapp, 'window_height', 768)
			webapp.custom_css = getattr(old_webapp, 'custom_css', '')
			webapp.tags = getattr(old_webapp, 'tags', [])
			

		
		self.close()
		
	def on_favicon_clicked(self, button):
		url = self.url_entry.get_text().strip()
		if not url:
			return
		
		button.set_sensitive(False)
		button.set_icon_name("content-loading-symbolic")
		
		def download_complete(favicon_path):
			button.set_sensitive(True)
			button.set_icon_name("image-x-generic-symbolic")
			if favicon_path:
				self.icon_entry.set_text(favicon_path)
				self.update_icon_preview(favicon_path)
		
		import threading
		def download_thread():
			favicon_path = self.parent_window.manager.download_favicon(url)
			from gi.repository import GLib
			GLib.idle_add(download_complete, favicon_path)
		
		threading.Thread(target=download_thread, daemon=True).start()
	
	def on_url_changed(self, entry):
		url = entry.get_text().strip()
		if url and len(url) > 7 and ('.' in url or url.startswith(('http://', 'https://'))):
			# Auto-fetch title if name field is empty
			if not self.name_entry.get_text().strip():
				self.auto_fetch_title(url)
			# Auto-download favicon if URL looks valid
			if not self.icon_entry.get_text().strip():
				self.auto_download_favicon(url)
	
	def auto_download_favicon(self, url):
		import threading
		def download_thread():
			favicon_path = self.parent_window.manager.download_favicon(url)
			from gi.repository import GLib
			def update_icon(path):
				if path and not self.icon_entry.get_text().strip():
					self.icon_entry.set_text(path)
					self.update_icon_preview(path)
			GLib.idle_add(update_icon, favicon_path)
		
		threading.Thread(target=download_thread, daemon=True).start()
	
	def auto_fetch_title(self, url):
		import threading
		def fetch_thread():
			title = self.parent_window.manager.get_page_title(url)
			from gi.repository import GLib
			def update_title(page_title):
				if page_title and not self.name_entry.get_text().strip():
					self.name_entry.set_text(page_title)
			GLib.idle_add(update_title, title)
		
		threading.Thread(target=fetch_thread, daemon=True).start()
	
	def on_icon_picker_clicked(self, button):
		dialog = IconPickerDialog(self)
		dialog.present()
	
	def set_selected_icon(self, icon_name):
		self.icon_entry.set_text(icon_name)
		self.update_icon_preview(icon_name)
	
	def on_icon_entry_changed(self, entry):
		icon_path = entry.get_text().strip()
		self.update_icon_preview(icon_path)
	
	def update_icon_preview(self, icon_path):
		if not icon_path:
			self.icon_preview.set_from_icon_name("application-x-executable")
			return
		
		if os.path.exists(icon_path):
			try:
				pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_path, 48, 48, True)
				self.icon_preview.set_from_pixbuf(pixbuf)
			except:
				self.icon_preview.set_from_icon_name("application-x-executable")
		else:
			# Try as icon name
			try:
				self.icon_preview.set_from_icon_name(icon_path)
			except:
				self.icon_preview.set_from_icon_name("application-x-executable")

class StatsDialog(Adw.Window):
	def __init__(self, parent):
		super().__init__()
		self.set_transient_for(parent)
		self.set_modal(True)
		self.set_default_size(600, 500)
		self.set_title(lang.get_text('STATS', 'usage_analytics'))
		self.parent_window = parent
		
		self.setup_ui()
		self.load_stats()
	
	def setup_ui(self):
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.set_content(main_box)
		
		header = Adw.HeaderBar()
		header.set_title_widget(Gtk.Label(label=lang.get_text('STATS', 'usage_analytics')))
		header.add_css_class("flat")
		main_box.append(header)
		
		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
		content_box.set_margin_top(20)
		content_box.set_margin_bottom(20)
		content_box.set_margin_start(20)
		content_box.set_margin_end(20)
		main_box.append(content_box)
		
		# Summary cards
		summary_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
		summary_box.set_homogeneous(True)
		content_box.append(summary_box)
		
		self.total_apps_card = self.create_summary_card(lang.get_text('STATS', 'total_apps'), "0", "application-x-executable-symbolic")
		self.total_launches_card = self.create_summary_card(lang.get_text('STATS', 'total_launches'), "0", "media-playback-start-symbolic")
		self.most_used_card = self.create_summary_card(lang.get_text('STATS', 'most_used'), lang.get_text('STATS', 'none'), "starred-symbolic")
		
		summary_box.append(self.total_apps_card)
		summary_box.append(self.total_launches_card)
		summary_box.append(self.most_used_card)
		
		# Apps list
		list_label = Gtk.Label(label=lang.get_text('STATS', 'app_usage_details'))
		list_label.set_halign(Gtk.Align.START)
		list_label.add_css_class("title-3")
		content_box.append(list_label)
		
		scrolled = Gtk.ScrolledWindow()
		scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scrolled.set_vexpand(True)
		scrolled.add_css_class("card")
		content_box.append(scrolled)
		
		self.stats_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		scrolled.set_child(self.stats_box)
	
	def create_summary_card(self, title, value, icon_name):
		card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
		card.add_css_class("card")
		card.set_margin_top(8)
		card.set_margin_bottom(8)
		card.set_margin_start(8)
		card.set_margin_end(8)
		
		# Icon
		icon_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		icon_box.set_halign(Gtk.Align.CENTER)
		icon_box.set_margin_top(16)
		
		icon = Gtk.Image()
		icon.set_from_icon_name(icon_name)
		icon.set_pixel_size(32)
		icon.add_css_class("accent")
		icon_box.append(icon)
		card.append(icon_box)
		
		# Value
		value_label = Gtk.Label(label=value)
		value_label.add_css_class("title-1")
		value_label.set_halign(Gtk.Align.CENTER)
		card.append(value_label)
		
		# Title
		title_label = Gtk.Label(label=title)
		title_label.add_css_class("caption")
		title_label.add_css_class("dim-label")
		title_label.set_halign(Gtk.Align.CENTER)
		title_label.set_margin_bottom(16)
		card.append(title_label)
		
		# Store labels for updates
		card.value_label = value_label
		
		return card
	
	def load_stats(self):
		stats = self.parent_window.manager.get_usage_stats()
		
		# Update summary cards
		total_apps = len(stats)
		total_launches = sum(stat['usage_count'] for stat in stats)
		most_used = stats[0]['name'] if stats and stats[0]['usage_count'] > 0 else lang.get_text('STATS', 'none')
		
		self.total_apps_card.value_label.set_text(str(total_apps))
		self.total_launches_card.value_label.set_text(str(total_launches))
		self.most_used_card.value_label.set_text(most_used[:15] + "..." if len(most_used) > 15 else most_used)
		
		# Load app details
		for i, stat in enumerate(stats):
			row = Adw.ActionRow()
			row.set_title(stat["name"])
			
			# Usage info
			usage_count = stat['usage_count']
			if usage_count == 0:
				usage_text = lang.get_text('STATS', 'never_used')
			else:
				launch_text = lang.get_text('STATS', 'launch_plural') if usage_count != 1 else lang.get_text('STATS', 'launch_singular')
				usage_text = f"{usage_count} {launch_text}"
				
				if stat['last_used'] > 0:
					import datetime
					last_used = datetime.datetime.fromtimestamp(stat['last_used'])
					now = datetime.datetime.now()
					diff = now - last_used
					
					if diff.days == 0:
						if diff.seconds < 3600:
							time_ago = lang.get_text('STATS', 'min_ago', diff.seconds // 60)
						else:
							time_ago = lang.get_text('STATS', 'hours_ago', diff.seconds // 3600)
					elif diff.days == 1:
						time_ago = lang.get_text('STATS', 'yesterday')
					elif diff.days < 7:
						time_ago = lang.get_text('STATS', 'days_ago', diff.days)
					else:
						time_ago = last_used.strftime('%b %d')
					
					usage_text += f" • {time_ago}"
			
			row.set_subtitle(usage_text)
			
			# Rank badge
			if i < 3 and usage_count > 0:
				rank_icon = Gtk.Image()
				if i == 0:
					rank_icon.set_from_icon_name("trophy-gold-symbolic")
				elif i == 1:
					rank_icon.set_from_icon_name("trophy-silver-symbolic")
				else:
					rank_icon.set_from_icon_name("trophy-bronze-symbolic")
				rank_icon.set_pixel_size(16)
				row.add_suffix(rank_icon)
			
			# Usage bar
			if total_launches > 0:
				progress = usage_count / total_launches
				bar = Gtk.ProgressBar()
				bar.set_fraction(progress)
				bar.set_size_request(60, 4)
				bar.add_css_class("osd")
				row.add_suffix(bar)
			
			self.stats_box.append(row)

class IconPickerDialog(Adw.Window):
	def __init__(self, parent):
		super().__init__()
		self.set_transient_for(parent)
		self.set_modal(True)
		self.set_default_size(500, 400)
		self.set_title(lang.get_text('DIALOG', 'select_icon'))
		self.parent_dialog = parent
		
		self.setup_ui()
		self.load_icons()
	
	def setup_ui(self):
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.set_content(main_box)
		
		# Header
		header = Adw.HeaderBar()
		header.set_title_widget(Gtk.Label(label=lang.get_text('DIALOG', 'select_icon')))
		main_box.append(header)
		
		# Content
		content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
		content_box.set_margin_top(16)
		content_box.set_margin_bottom(16)
		content_box.set_margin_start(16)
		content_box.set_margin_end(16)
		main_box.append(content_box)
		
		# Search
		search_entry = Gtk.SearchEntry()
		search_entry.connect("search-changed", self.on_search_changed)
		content_box.append(search_entry)
		
		# Icons grid
		scrolled = Gtk.ScrolledWindow()
		scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scrolled.set_vexpand(True)
		content_box.append(scrolled)
		
		self.flow_box = Gtk.FlowBox()
		self.flow_box.set_max_children_per_line(8)
		self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
		self.flow_box.connect("child-activated", self.on_icon_selected)
		scrolled.set_child(self.flow_box)
	
	def load_icons(self):
		self.all_icons = []
		
		# Scan system icon directories
		icon_dirs = [
			"/usr/share/icons",
			"/usr/share/pixmaps",
			Path.home() / ".local/share/icons",
			Path.home() / ".icons"
		]
		
		icon_names = set()
		
		for icon_dir in icon_dirs:
			if os.path.exists(icon_dir):
				try:
					# Look for common icon theme directories
					for theme_dir in os.listdir(icon_dir):
						theme_path = os.path.join(icon_dir, theme_dir)
						if os.path.isdir(theme_path):
							self._scan_theme_directory(theme_path, icon_names)
				except:
					continue
			
		# Convert to sorted list
		self.all_icons = sorted(list(icon_names))
		
		# Load first 200 icons for performance
		for icon_name in self.all_icons[:200]:
			self.add_icon_to_grid(icon_name)
	
	def _scan_theme_directory(self, theme_path, icon_names):
		try:
			for root, dirs, files in os.walk(theme_path):
				# Skip very deep directories for performance
				if root.count(os.sep) - theme_path.count(os.sep) > 3:
					continue
						
				for file in files:
					if file.endswith(('.png', '.svg', '.xpm')):
						# Extract icon name without extension
						icon_name = os.path.splitext(file)[0]
						# Remove size suffixes like -16, -24, -48
						icon_name = self._clean_icon_name(icon_name)
						if icon_name and len(icon_name) > 2:
							icon_names.add(icon_name)
							
				# Limit total icons for performance
				if len(icon_names) > 1000:
					break
		except:
			pass
	
	def _clean_icon_name(self, name):
		# Remove common size suffixes
		import re
		name = re.sub(r'-\d+$', '', name)  # Remove -16, -24, etc.
		name = re.sub(r'_\d+$', '', name)  # Remove _16, _24, etc.
		return name
	
	def add_icon_to_grid(self, icon_name):
		button = Gtk.Button()
		button.set_size_request(64, 64)
		button.add_css_class("flat")
		
		icon = Gtk.Image()
		icon.set_from_icon_name(icon_name)
		icon.set_pixel_size(32)
		button.set_child(icon)
		
		button.icon_name = icon_name
		button.connect("clicked", lambda btn: self.select_icon(btn.icon_name))
		
		self.flow_box.append(button)
	
	def on_search_changed(self, search_entry):
		search_text = search_entry.get_text().lower()
		

	
	def on_icon_selected(self, flow_box, child):
		button = child.get_child()
		if hasattr(button, 'icon_name'):
			self.select_icon(button.icon_name)
	
	def select_icon(self, icon_name):
		self.parent_dialog.set_selected_icon(icon_name)
		self.close()

class WebPinApp(Adw.Application):
	def __init__(self):
		dbg("WebPinApp.__init__ başlıyor")
		super().__init__(application_id="io.github.cektor.WebPin",
						 flags=Gio.ApplicationFlags.NON_UNIQUE)
		# Uygulama adını ayarla
		GLib.set_prgname("WebPin")
		GLib.set_application_name("WebPin")
		# pencere referansını uygulama
		self.window = None
		self.connect("activate", self.on_activate)
		dbg("WebPinApp.__init__ tamam")
	
	def on_activate(self, app):
		dbg("WebPinApp.on_activate çağrıldı")
		try:
			if not self.window:
				self.window = WebPinWindow(self)
			self.window.present()
			dbg("Pencere oluşturuldu ve present edildi")
		except Exception as e:
			print(f"on_activate hata: {e}")
			import traceback
			traceback.print_exc()

if __name__ == "__main__":
	try:
		dbg("Uygulama başlatılıyor")
		app = WebPinApp()
		ret = app.run(sys.argv)
		dbg(f"app.run döndü: {ret}")
		sys.exit(ret)
	except Exception as e:
		print(f"HATA: {e}")
		import traceback
		traceback.print_exc()
