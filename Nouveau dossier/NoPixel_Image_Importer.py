# -*- coding: utf-8 -*-
"""
NoPixel Store - Image Importer
اختر مجلد الصور ومجلد الموقع، وسيتم نسخ الصور وإنشاء المنتجات تلقائياً.
"""
import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def js_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'

class App:
    def __init__(self, root):
        self.root = root
        root.title("NoPixel Store - Image Importer")
        root.geometry("690x590")
        root.minsize(630, 540)
        root.configure(bg="#0b0b0b")
        self.images_dir = tk.StringVar()
        self.store_dir = tk.StringVar()
        self.category = tk.StringVar(value="buildings")
        self.price = tk.StringVar(value="5000 دج")
        self.description = tk.StringVar(value="منتج مميز داخل NoPixel Store")
        self.prefix = tk.StringVar(value="")
        self.status = tk.StringVar(value="اختر مجلد الصور ومجلد المتجر للبدء.")
        self.build_ui()

    def build_ui(self):
        gold = "#e0b04f"
        tk.Label(self.root, text="NoPixel Store", bg="#0b0b0b", fg=gold,
                 font=("Segoe UI", 22, "bold")).pack(pady=(18, 2))
        tk.Label(self.root, text="أداة إضافة الصور والمنتجات تلقائياً",
                 bg="#0b0b0b", fg="#c9c1b2", font=("Segoe UI", 11)).pack(pady=(0, 16))
        body = tk.Frame(self.root, bg="#151515", padx=18, pady=16,
                        highlightbackground="#574522", highlightthickness=1)
        body.pack(fill="both", expand=True, padx=20, pady=5)

        self.folder_row(body, "1) مجلد الصور:", self.images_dir, self.choose_images)
        self.folder_row(body, "2) مجلد المتجر (المجلد الذي يحتوي data):",
                        self.store_dir, self.choose_store)

        tk.Label(body, text="3) نوع المنتجات:", bg="#151515", fg="#eee",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(13, 4))
        ttk.Style().configure("TCombobox", fieldbackground="#242424",
                              background="#242424", foreground="#111")
        combo = ttk.Combobox(body, textvariable=self.category, state="readonly",
                             values=["buildings", "houses", "cars", "memberships", "other"],
                             font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=5)

        self.entry(body, "السعر الافتراضي لكل صورة:", self.price)
        self.entry(body, "وصف افتراضي:", self.description)
        self.entry(body, "بادئة الاسم (اختياري):", self.prefix)

        tk.Label(body, text="مثال: إذا كانت الصور building1.jpg و building2.png،"
                 " ستضاف تلقائياً كمنتجين بنفس أسماء الملفات.",
                 bg="#151515", fg="#aaa18f", wraplength=610,
                 justify="left").pack(anchor="w", pady=(10, 8))

        tk.Button(body, text="إضافة الصور إلى المتجر تلقائياً",
                  command=self.import_images, bg=gold, fg="#111",
                  activebackground="#f3ca75", relief="flat",
                  font=("Segoe UI", 12, "bold"), cursor="hand2",
                  padx=12, pady=11).pack(fill="x", pady=(8, 8))
        tk.Label(body, textvariable=self.status, bg="#151515", fg="#e6c77f",
                 wraplength=610, justify="left").pack(anchor="w", pady=(5, 0))
        tk.Label(self.root, text="يتم إنشاء نسخة احتياطية من products.js قبل التعديل.",
                 bg="#0b0b0b", fg="#8c8579", font=("Segoe UI", 9)).pack(pady=10)

    def folder_row(self, parent, label, var, command):
        tk.Label(parent, text=label, bg="#151515", fg="#eee",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(4, 4))
        row = tk.Frame(parent, bg="#151515")
        row.pack(fill="x")
        tk.Entry(row, textvariable=var, bg="#242424", fg="#fff",
                 insertbackground="white", relief="flat").pack(side="left", fill="x",
                                                                expand=True, ipady=8)
        tk.Button(row, text="استعراض", command=command, bg="#333",
                  fg="white", relief="flat", padx=12).pack(side="left", padx=(8, 0))

    def entry(self, parent, label, var):
        tk.Label(parent, text=label, bg="#151515", fg="#eee",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
        tk.Entry(parent, textvariable=var, bg="#242424", fg="#fff",
                 insertbackground="white", relief="flat").pack(fill="x", ipady=8)

    def choose_images(self):
        p = filedialog.askdirectory(title="اختر المجلد الذي يحتوي صور المنتجات")
        if p:
            self.images_dir.set(p)

    def choose_store(self):
        p = filedialog.askdirectory(title="اختر مجلد المتجر الذي يحتوي ملف data/products.js")
        if p:
            self.store_dir.set(p)

    def import_images(self):
        src = Path(self.images_dir.get())
        site = Path(self.store_dir.get())
        category = self.category.get()
        if not src.is_dir():
            messagebox.showerror("خطأ", "اختر مجلد صور صحيحاً.")
            return
        products_file = site / "data" / "products.js"
        if not products_file.is_file():
            messagebox.showerror("لم يتم العثور على الملف",
                "لم أجد data/products.js داخل مجلد المتجر.\n"
                "اختر المجلد الرئيسي للموقع، وليس مجلد data نفسه.")
            return

        images = sorted([p for p in src.iterdir()
                         if p.is_file() and p.suffix.lower() in IMAGE_EXTS])
        if not images:
            messagebox.showwarning("لا توجد صور", "لم أجد صوراً مباشرة داخل المجلد المختار.")
            return

        target_dir = site / "assets" / "products" / category
        target_dir.mkdir(parents=True, exist_ok=True)
        try:
            original = products_file.read_text(encoding="utf-8-sig")
            # Make a one-time backup for this run.
            backup = products_file.with_name("products.js.backup")
            if not backup.exists():
                shutil.copy2(products_file, backup)

            # Locate the products array's closing bracket.
            match = re.search(r"(const\s+products\s*=\s*\[)(.*?)(\]\s*;)", original, re.S)
            if not match:
                messagebox.showerror("تنسيق غير مدعوم",
                    "لم أستطع العثور على const products = [ ... ]; داخل products.js.")
                return

            existing = match.group(2)
            added = []
            skipped = []
            for image_path in images:
                dest = target_dir / image_path.name
                rel = f"assets/products/{category}/{image_path.name}"
                if rel.replace("\\", "/") in existing:
                    skipped.append(image_path.name)
                    continue
                # Avoid overwriting a different image with the same name.
                if dest.exists():
                    if image_path.resolve() != dest.resolve():
                        stem, suffix, n = dest.stem, dest.suffix, 2
                        while (target_dir / f"{stem}_{n}{suffix}").exists():
                            n += 1
                        dest = target_dir / f"{stem}_{n}{suffix}"
                        rel = f"assets/products/{category}/{dest.name}"
                if image_path.resolve() != dest.resolve():
                    shutil.copy2(image_path, dest)
                raw_name = image_path.stem.replace("_", " ").replace("-", " ").strip()
                name = (self.prefix.get().strip() + " " + raw_name).strip()
                if not name:
                    name = raw_name or "منتج جديد"
                added.append(
                    "  {\n"
                    f"    name: {js_string(name)},\n"
                    f"    category: {js_string(category)},\n"
                    f"    price: {js_string(self.price.get().strip())},\n"
                    f"    image: {js_string(rel)},\n"
                    f"    description: {js_string(self.description.get().strip())}\n"
                    "  }"
                )

            if added:
                new_body = existing.rstrip()
                if new_body.strip():
                    new_body += ",\n"
                new_body += ",\n".join(added) + "\n"
                updated = original[:match.start(2)] + new_body + original[match.end(2):]
                products_file.write_text(updated, encoding="utf-8")
            msg = f"تمت إضافة {len(added)} منتج/منتجات."
            if skipped:
                msg += f"\nتم تخطي {len(skipped)} صور موجودة مسبقاً."
            msg += f"\nمكان الصور: assets/products/{category}/"
            msg += "\nأعد تحميل صفحة المتجر لرؤية التغييرات."
            self.status.set(msg.replace("\n", "  "))
            messagebox.showinfo("اكتمل الاستيراد", msg)
        except Exception as e:
            messagebox.showerror("حدث خطأ", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
