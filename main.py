import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("700x600")
        
        self.data_file = "quotes_data.json"
        self.load_data()
        self.setup_ui()
        self.update_filter_lists()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get("quotes", self.get_default_quotes())
                    self.history = data.get("history", [])
            except (json.JSONDecodeError, FileNotFoundError):
                self.quotes = self.get_default_quotes()
                self.history = []
        else:
            self.quotes = self.get_default_quotes()
            self.history = []
    
    def get_default_quotes(self):
        return [
            {"text": "Будьте сами собой, все остальные роли уже заняты.", "author": "Оскар Уайльд", "theme": "жизнь"},
            {"text": "Единственный способ делать великую работу — любить то, что вы делаете.", "author": "Стив Джобс", "theme": "работа"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "theme": "творчество"},
            {"text": "Будь переменой, которую ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "жизнь"},
            {"text": "Успех — это способность идти от поражения к поражению, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "успех"},
            {"text": "Лучшее время посадить дерево было 20 лет назад. Второе лучшее время — сейчас.", "author": "Китайская пословица", "theme": "мотивация"},
            {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "theme": "образование"},
            {"text": "Вдохновение существует, но оно должно застать вас за работой.", "author": "Пабло Пикассо", "theme": "творчество"},
            {"text": "Сложнее всего начать действовать, все остальное зависит только от упорства.", "author": "Амелия Эрхарт", "theme": "мотивация"},
            {"text": "Не важно, как медленно вы идете, пока вы не останавливаетесь.", "author": "Конфуций", "theme": "мотивация"},
            {"text": "Каждая мечта начинается с мечтателя.", "author": "Гарриет Табмен", "theme": "мечты"}
        ]
    
    def save_data(self):
        data = {
            "quotes": self.quotes,
            "history": self.history
        }
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Блок генерации
        generate_frame = ttk.LabelFrame(main_frame, text="Генерация цитаты", padding=10)
        generate_frame.pack(fill="x", pady=5)
        
        self.generate_btn = ttk.Button(
            generate_frame, 
            text="🎲 Сгенерировать случайную цитату", 
            command=self.generate_quote
        )
        self.generate_btn.pack(pady=5)
        
        self.quote_display = ttk.Label(
            generate_frame, 
            text='Нажмите кнопку "Сгенерировать" для получения цитаты',
            wraplength=600,
            font=("Arial", 11),
            justify="center"
        )
        self.quote_display.pack(pady=10)
        
        # Блок добавления цитаты
        add_frame = ttk.LabelFrame(main_frame, text="Добавить новую цитату", padding=10)
        add_frame.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="Цитата:").grid(row=0, column=0, sticky="w", pady=2)
        self.new_quote_text = tk.Text(add_frame, height=3, width=60)
        self.new_quote_text.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="w", pady=2)
        self.new_author = ttk.Entry(add_frame, width=62)
        self.new_author.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky="w", pady=2)
        self.new_theme = ttk.Entry(add_frame, width=62)
        self.new_theme.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Button(add_frame, text="Добавить цитату", command=self.add_quote).grid(
            row=3, column=1, pady=10, sticky="e"
        )
        
        # Блок фильтрации
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", pady=5)
        
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky="w", padx=5)
        self.author_filter = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.author_filter.grid(row=0, column=1, padx=5)
        self.author_filter.bind("<<ComboboxSelected>>", lambda e: self.show_history())
        
        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky="w", padx=5)
        self.theme_filter = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.theme_filter.grid(row=0, column=3, padx=5)
        self.theme_filter.bind("<<ComboboxSelected>>", lambda e: self.show_history())
        
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.clear_filters).grid(
            row=0, column=4, padx=10
        )
        
        # Блок истории
        history_frame = ttk.LabelFrame(main_frame, text="История сгенерированных цитат", padding=10)
        history_frame.pack(fill="both", expand=True, pady=5)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame, 
            height=8, 
            wrap=tk.WORD,
            font=("Arial", 9)
        )
        self.history_text.pack(fill="both", expand=True)
        self.history_text.config(state="disabled")
        
        btn_frame = ttk.Frame(history_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.show_history).pack(side="left", padx=5)
    
    def validate_quote_input(self, text, author, theme):
        errors = []
        
        if not text.strip():
            errors.append("Текст цитаты не может быть пустым")
        elif len(text) > 500:
            errors.append("Текст цитаты слишком длинный (максимум 500 символов)")
        
        if not author.strip():
            errors.append("Поле 'Автор' не может быть пустым")
        elif len(author) > 100:
            errors.append("Имя автора слишком длинное (максимум 100 символов)")
        
        if not theme.strip():
            errors.append("Поле 'Тема' не может быть пустым")
        elif len(theme) > 50:
            errors.append("Тема слишком длинная (максимум 50 символов)")
        
        return errors
    
    def add_quote(self):
        text = self.new_quote_text.get("1.0", tk.END).strip()
        author = self.new_author.get().strip()
        theme = self.new_theme.get().strip()
        
        errors = self.validate_quote_input(text, author, theme)
        
        if errors:
            messagebox.showerror("Ошибка валидации", "\n".join(errors))
            return
        
        new_quote = {
            "text": text,
            "author": author,
            "theme": theme.lower()
        }
        
        self.quotes.append(new_quote)
        self.save_data()
        
        self.new_quote_text.delete("1.0", tk.END)
        self.new_author.delete(0, tk.END)
        self.new_theme.delete(0, tk.END)
        
        self.update_filter_lists()
        
        messagebox.showinfo("Успех", "Цитата добавлена!")
    
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Нет доступных цитат")
            return
        
        quote = random.choice(self.quotes)
        
        display_text = f'"{quote["text"]}"\n\n— {quote["author"]} | Тема: {quote["theme"]}'
        self.quote_display.config(text=display_text)
        
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        }
        self.history.append(history_entry)
        
        self.save_data()
        self.show_history()
    
    def show_history(self):
        author_filter = self.author_filter.get()
        theme_filter = self.theme_filter.get()
        
        filtered_history = self.history.copy()
        
        if author_filter and author_filter != "Все авторы":
            filtered_history = [h for h in filtered_history if h["author"] == author_filter]
        
        if theme_filter and theme_filter != "Все темы":
            filtered_history = [h for h in filtered_history if h["theme"] == theme_filter.lower()]
        
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        if not filtered_history:
            self.history_text.insert("1.0", "История пуста. Сгенерируйте несколько цитат!")
        else:
            for entry in reversed(filtered_history):
                self.history_text.insert(
                    "1.0",
                    f"[{entry['timestamp']}] \"{entry['text']}\" — {entry['author']} (Тема: {entry['theme']})\n\n"
                )
        
        self.history_text.config(state="disabled")
    
    def update_filter_lists(self):
        all_authors = ["Все авторы"] + sorted(list(set(q["author"] for q in self.quotes)))
        all_themes = ["Все темы"] + sorted(list(set(q["theme"] for q in self.quotes)))
        
        self.author_filter['values'] = all_authors
        self.theme_filter['values'] = all_themes
        
        self.author_filter.set("Все авторы")
        self.theme_filter.set("Все темы")
    
    def clear_filters(self):
        self.author_filter.set("Все авторы")
        self.theme_filter.set("Все темы")
        self.show_history()
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_data()
            self.show_history()
            messagebox.showinfo("Успех", "История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
