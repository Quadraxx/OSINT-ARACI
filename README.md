<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OSINT-Aracı-orange?style=for-the-badge" alt="OSINT">
  <img src="https://img.shields.io/github/license/Quadraxx/OSINT-ARACI?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/Quadraxx/OSINT-ARACI?style=for-the-badge" alt="Stars">
</p>

<br>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=OSINT%20ARACI&fontSize=60&fontAlignY=35&animation=fadeIn" />
</p>

<p align="center">
  <b>🔍 Her Şeyi Kapsayan Açık Kaynak İstihbarat Aracı</b><br>
  <i>Sosyal Medya · E-posta · Telefon · IP/Domain · Daha Fazlası</i>
</p>

<br>

---

## 📋 İçindekiler

- [🎯 Hedef](#-hedef)
- [🚀 Özellikler](#-özellikler)
- [📂 Proje Yapısı](#-proje-yapısı)
- [⚙️ Kurulum](#️-kurulum)
- [💻 Kullanım](#-kullanım)
- [🧩 Modüller](#-modüller)
- [🛠️ Kullanılan Teknolojiler](#️-kullanılan-teknolojiler)
- [📌 Yol Haritası](#-yol-haritası)
- [📄 Lisans](#-lisans)

---

## 🎯 Hedef

Bu proje; **sosyal medya**, **e-posta**, **telefon numarası**, **IP adresi**, **domain** ve daha birçok kaynaktan veri toplamayı hedefleyen, **her şeyi kapsayan** bir OSINT aracı olmayı amaçlamaktadır.

> 💡 *"Bilgi güçtür. Açık kaynak istihbaratı, bu gücü herkes için erişilebilir kılar."*

---

## 🚀 Özellikler

| Modül | Açıklama | Durum |
|-------|----------|-------|
| 🔍 **Sosyal Medya** | 13 platformda kullanıcı adı taraması | ✅ Çalışıyor |
| 📧 **E-posta OSINT** | Doğrulama + MX kaydı + veri ihlali kontrolü | ✅ Çalışıyor |
| 📞 **Telefon OSINT** | Ülke, operatör, zaman dilimi tespiti | ✅ Çalışıyor |
| 🌐 **IP/Domain OSINT** | WHOIS, DNS, IP konum, alt domain keşfi | ✅ Çalışıyor |

---

## 📂 Proje Yapısı

```
OSINT-ARACI/
├── 🚀 app.py                     # Ana uygulama (GUI)
├── 🖥️ main.py                    # CLI versiyonu
├── 📦 requirements.txt           # Bağımlılıklar
├── 🔒 .gitignore                 # Git için
├── 📖 README.md                  # Proje dokümantasyonu
├── 📁 src/
│   ├── 📁 modules/
│   │   ├── 📄 social_media.py    # Sosyal medya OSINT
│   │   ├── 📄 email.py           # E-posta OSINT
│   │   ├── 📄 phone.py           # Telefon OSINT
│   │   └── 📄 ip_domain.py       # IP/Domain OSINT
│   └── 📁 utils/
│       └── 📄 helpers.py         # Yardımcı fonksiyonlar
├── 📁 config/                    # Yapılandırma dosyaları
└── 📁 Günlük Yapılan İşler/      # Günlük geliştirme kayıtları
```

---

## ⚙️ Kurulum

```bash
# 1. Projeyi klonla
git clone https://github.com/Quadraxx/OSINT-ARACI.git
cd OSINT-ARACI

# 2. Sanal ortam oluştur (opsiyonel)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## 💻 Kullanım

### 🖥️ GUI (Önerilen)

```bash
python app.py
```

### 💻 CLI

```bash
# Modülleri listele
python main.py --list-modules

# Sosyal medya taraması
python main.py -m social -t <kullanici_adi>

# E-posta sorgulama
python main.py -m email -t <eposta@adresi.com>

# Telefon sorgulama
python main.py -m phone -t <telefon_numarasi>

# IP/Domain sorgulama
python main.py -m ip -t <ornek.com>

# Tüm modülleri çalıştır
python main.py -m all -t <hedef>
```

---

## 🧩 Modüller

<details>
<summary><b>🔍 Sosyal Medya</b></summary>
<br>

- Kullanıcı adı ile platformlarda arama
- Profil bilgilerini toplama
- Platform desteği: (planlanan)
  - Twitter / X
  - Instagram
  - LinkedIn
  - GitHub
  - Reddit
  - Telegram

</details>

<details>
<summary><b>📧 E-posta OSINT</b></summary>
<br>

- E-posta formatı doğrulama
- MX kaydı sorgulama
- Veri sızıntısı kontrolü
- Domain bazlı e-posta analizi

</details>

<details>
<summary><b>📞 Telefon OSINT</b></summary>
<br>

- Ülke ve operatör tespiti
- Numara formatı doğrulama
- Numara bilgi sorgulama

</details>

<details>
<summary><b>🌐 IP/Domain OSINT</b></summary>
<br>

- WHOIS sorgulama
- DNS kayıtları (A, MX, NS, TXT)
- IP konum bilgisi
- Reverse DNS
- Alt domain keşfi

</details>

---

## 🛠️ Kullanılan Teknolojiler

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Requests-FF6F00?style=for-the-badge&logo=python&logoColor=white" />
</p>

| Kütüphane | Kullanım Amacı |
|-----------|---------------|
| `requests` | HTTP istekleri |
| `beautifulsoup4` | HTML ayrıştırma |
| `lxml` | Hızlı XML/HTML işleme |
| `dnspython` | DNS sorguları |
| `python-whois` | WHOIS sorguları |
| `colorama` | Renkli terminal çıktısı |
| `customtkinter` | Modern GUI arayüzü |
| `phonenumbers` | Telefon numarası doğrulama ve bilgi çekme |
| `email-validator` | E-posta formatı doğrulama |

---

## 📌 Yol Haritası

- [x] Proje yapısı oluşturma
- [x] GitHub repo kurulumu
- [x] GUI uygulaması (CustomTkinter)
- [x] Sosyal medya modülü geliştirme
- [x] E-posta OSINT modülü geliştirme
- [x] Telefon OSINT modülü geliştirme
- [x] IP/Domain OSINT modülü geliştirme
- [ ] Çoklu hedef desteği
- [ ] Rapor çıktısı (HTML/JSON/PDF)
- [ ] Web arayüzü (opsiyonel)

---

## 📄 Lisans

Bu proje **MIT lisansı** ile lisanslanmıştır. Detaylı bilgi için `LICENSE` dosyasına bakınız.

<br>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" />
</p>

<p align="center">
  ⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
</p>
