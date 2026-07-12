import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class SocialMedia:
    def __init__(self):
        self.name = "Sosyal Medya OSINT"
        self.platforms = {
            "Twitter / X": "https://twitter.com/{}",
            "Instagram": "https://instagram.com/{}",
            "GitHub": "https://github.com/{}",
            "Reddit": "https://reddit.com/user/{}",
            "Medium": "https://medium.com/@{}",
            "Pinterest": "https://pinterest.com/{}",
            "YouTube": "https://youtube.com/@{}",
            "TikTok": "https://tiktok.com/@{}",
            "Twitch": "https://twitch.tv/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "Telegram": "https://t.me/{}",
            "Dev.to": "https://dev.to/{}",
            "Replit": "https://replit.com/@{}",
        }

    def run(self, target, callback=None):
        results = []
        results.append(("Bilgi", f"🔍 {self.name} - Hedef: {target}"))
        results.append(("Bilgi", f"📡 {len(self.platforms)} platform taranıyor..."))

        found = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self._check_platform, name, url, target): name for name, url in self.platforms.items()}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                    found += 1

        results.append(("Bilgi", f"✅ {found} platformda profil bulundu"))
        if callback:
            callback(results)
        return results

    def _check_platform(self, name, url, username):
        try:
            resp = requests.get(url.format(username), timeout=5, allow_redirects=True)
            if resp.status_code == 200:
                return ("Başarılı", f"✅ {name}: {url.format(username)}")
            elif resp.status_code == 404:
                return ("Hata", f"❌ {name}: Profil bulunamadı")
            else:
                return ("Uyarı", f"⚠️ {name}: {resp.status_code}")
        except:
            return ("Hata", f"❌ {name}: Bağlantı hatası")
