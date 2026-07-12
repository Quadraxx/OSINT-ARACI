import customtkinter as ctk
from tkinter import messagebox
import threading
from src.modules.social_media import SocialMedia
from src.modules.email import EmailLookup
from src.modules.phone import PhoneLookup
from src.modules.ip_domain import IPDomainLookup
from src.utils.helpers import validate_email, validate_phone, validate_ip, validate_domain

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class OSINTApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OSINT ARACI - Kapsamlı Açık Kaynak İstihbarat Aracı")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_area()

        self.modules = {
            "Sosyal Medya": SocialMedia(),
            "E-posta": EmailLookup(),
            "Telefon": PhoneLookup(),
            "IP/Domain": IPDomainLookup(),
        }

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(6, weight=1)

        logo = ctk.CTkLabel(sidebar, text="🔍 OSINT ARACI", font=ctk.CTkFont(size=18, weight="bold"))
        logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        desc = ctk.CTkLabel(sidebar, text="Her Şeyi Kapsayan\nOSINT Aracı", font=ctk.CTkFont(size=12))
        desc.grid(row=1, column=0, padx=20, pady=(0, 20))

        sep = ctk.CTkFrame(sidebar, height=2)
        sep.grid(row=2, column=0, padx=20, sticky="ew")

        modules_label = ctk.CTkLabel(sidebar, text="MODÜLLER", font=ctk.CTkFont(size=13, weight="bold"))
        modules_label.grid(row=3, column=0, padx=20, pady=(15, 5))

        self.module_buttons = {}
        module_names = ["Sosyal Medya", "E-posta", "Telefon", "IP/Domain"]
        icons = ["🔍", "📧", "📞", "🌐"]
        for i, (name, icon) in enumerate(zip(module_names, icons)):
            btn = ctk.CTkButton(sidebar, text=f"{icon} {name}", anchor="w",
                                command=lambda n=name: self._select_module(n))
            btn.grid(row=4 + i, column=0, padx=20, pady=4, sticky="ew")
            self.module_buttons[name] = btn

        sep2 = ctk.CTkFrame(sidebar, height=2)
        sep2.grid(row=8, column=0, padx=20, pady=(10, 10), sticky="ew")

        about_btn = ctk.CTkButton(sidebar, text="ℹ️ Hakkında", anchor="w", command=self._show_about)
        about_btn.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.status_label = ctk.CTkLabel(sidebar, text="✅ Hazır", font=ctk.CTkFont(size=11))
        self.status_label.grid(row=10, column=0, padx=20, pady=(0, 15))

    def _create_main_area(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.header_label = ctk.CTkLabel(self.main_frame, text="Hoş Geldiniz",
                                         font=ctk.CTkFont(size=22, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.desc_label = ctk.CTkLabel(self.main_frame, text="Soldaki menüden bir modül seçin ve hedef belirleyin.",
                                       font=ctk.CTkFont(size=13))
        self.desc_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.target_label = ctk.CTkLabel(self.input_frame, text="Hedef:", font=ctk.CTkFont(size=14))
        self.target_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.target_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Kullanıcı adı, e-posta, telefon veya IP/domain girin")
        self.target_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        self.run_button = ctk.CTkButton(self.input_frame, text="▶ Başlat", width=100, command=self._run_module)
        self.run_button.grid(row=0, column=2, padx=(0, 10), pady=10)

        self.progress = ctk.CTkProgressBar(self.main_frame, mode="indeterminate")
        self.progress.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress.grid_remove()

        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)

        self.results_header = ctk.CTkLabel(self.results_frame, text="Sonuçlar",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.results_header.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        self.results_text = ctk.CTkTextbox(self.results_frame, wrap="word", state="disabled")
        self.results_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.main_frame.grid_rowconfigure(4, weight=1)
        self.current_module = None

    def _select_module(self, name):
        self.current_module = name
        self.header_label.configure(text=f"{['🔍','📧','📞','🌐'][['Sosyal Medya','E-posta','Telefon','IP/Domain'].index(name)]} {name}")
        self.desc_label.configure(text=f"{self.modules[name].__class__.__name__} modülü seçildi. Hedef girin ve Başlat'a tıklayın.")
        self.target_entry.delete(0, "end")
        self.target_entry.configure(placeholder_text=self._get_placeholder(name))
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.configure(state="disabled")

    def _get_placeholder(self, name):
        placeholders = {
            "Sosyal Medya": "Kullanıcı adı girin (ornek_kullanici)",
            "E-posta": "E-posta adresi girin (ornek@mail.com)",
            "Telefon": "Telefon numarası girin (+905551234567)",
            "IP/Domain": "IP veya domain girin (ornek.com / 8.8.8.8)",
        }
        return placeholders.get(name, "Hedef girin")

    def _run_module(self):
        if not self.current_module:
            messagebox.showwarning("Uyarı", "Lütfen önce bir modül seçin!")
            return

        target = self.target_entry.get().strip()
        if not target:
            messagebox.showwarning("Uyarı", "Lütfen bir hedef girin!")
            return

        module = self.modules[self.current_module]
        self.run_button.configure(state="disabled", text="⏳ Çalışıyor...")
        self.progress.grid()
        self.progress.start()
        self.status_label.configure(text="⏳ Çalışıyor...")

        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", f"🔍 {self.current_module} modülü çalıştırılıyor...\n")
        self.results_text.insert("end", f"📌 Hedef: {target}\n")
        self.results_text.insert("end", "━" * 50 + "\n\n")
        self.results_text.configure(state="disabled")

        thread = threading.Thread(target=self._run_async, args=(module, target), daemon=True)
        thread.start()

    def _run_async(self, module, target):
        try:
            module.run(target, callback=self._update_results)
        except Exception as e:
            self._update_results([("Hata", f"❌ Hata oluştu: {str(e)}")])

    def _update_results(self, results):
        self.results_text.configure(state="normal")
        for result_type, message in results:
            if result_type == "Başarılı":
                tag = "success"
            elif result_type == "Hata":
                tag = "error"
            elif result_type == "Uyarı":
                tag = "warning"
            else:
                tag = "info"
            self.results_text.insert("end", message + "\n", tag)
        self.results_text.insert("end", "\n" + "━" * 50 + "\n")
        self.results_text.see("end")

        self.results_text.tag_config("success", foreground="#4CAF50")
        self.results_text.tag_config("error", foreground="#F44336")
        self.results_text.tag_config("warning", foreground="#FF9800")
        self.results_text.tag_config("info", foreground="#2196F3")

        self.results_text.configure(state="disabled")

        self.progress.stop()
        self.progress.grid_remove()
        self.run_button.configure(state="normal", text="▶ Başlat")
        self.status_label.configure(text="✅ Tamamlandı")

    def _show_about(self):
        about = ctk.CTkToplevel(self)
        about.title("Hakkında")
        about.geometry("400x300")
        about.resizable(False, False)

        label = ctk.CTkLabel(about, text="🔍 OSINT ARACI", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=(20, 10))

        label2 = ctk.CTkLabel(about, text="Kapsamlı Açık Kaynak İstihbarat Aracı\n\nGeliştirici: Quadraxx\nSürüm: 1.0.0\n\nPython & CustomTkinter ile geliştirilmiştir.\n\n© 2026 Tüm hakları saklıdır.", justify="center")
        label2.pack(pady=10)

        close_btn = ctk.CTkButton(about, text="Kapat", command=about.destroy)
        close_btn.pack(pady=20)

if __name__ == "__main__":
    app = OSINTApp()
    app.mainloop()
