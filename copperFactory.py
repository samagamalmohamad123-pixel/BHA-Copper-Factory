import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==========================================
# BHA | المؤسسة الهندسية
# نظام إدارة مصنع النحاس
# ==========================================

# الألوان
BG = "#050505"
CARD = "#111111"
CARD2 = "#191919"
COPPER = "#C9824B"
WHITE = "#FFFFFF"
GRAY = "#A0A0A0"
GREEN = "#42B883"
RED = "#D96C64"

FONT = "Arial"

# قاعدة البيانات
db = sqlite3.connect("BHA_factory.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
""")
db.commit()

# النافذة الرئيسية
root = tk.Tk()
root.title("BHA | المؤسسة الهندسية")
root.geometry("1150x720")
root.minsize(1000, 650)
root.configure(bg=BG)

# تنسيق الجدول
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD,
    foreground=WHITE,
    fieldbackground=CARD,
    rowheight=38,
    font=(FONT, 11),
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background="#242424",
    foreground=COPPER,
    font=(FONT, 11, "bold"),
    padding=10
)

style.map(
    "Treeview",
    background=[("selected", "#493426")],
    foreground=[("selected", WHITE)]
)

# ==========================================
# الهيدر
# ==========================================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=28, pady=20)

brand = tk.Frame(header, bg=BG)
brand.pack(side="left")

tk.Label(
    brand,
    text="BHA",
    font=(FONT, 32, "bold"),
    fg=COPPER,
    bg=BG
).pack(side="left")

tk.Label(
    brand,
    text="المؤسسة الهندسية",
    font=(FONT, 16, "bold"),
    fg=WHITE,
    bg=BG
).pack(side="left", padx=12, pady=10)

tk.Label(
    header,
    text="COPPER FACTORY\nMANAGEMENT SYSTEM",
    font=(FONT, 10, "bold"),
    fg=GRAY,
    bg=BG,
    justify="right"
).pack(side="right", pady=10)

tk.Frame(root, bg=COPPER, height=2).pack(fill="x", padx=28)

# ==========================================
# بطاقات الإحصائيات
# ==========================================

stats = tk.Frame(root, bg=BG)
stats.pack(fill="x", padx=28, pady=20)


def create_card(title, value, color):
    card = tk.Frame(
        stats,
        bg=CARD,
        highlightbackground="#292929",
        highlightthickness=1
    )

    card.pack(side="left", fill="x", expand=True, padx=7, ipady=10)

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=GRAY,
        font=(FONT, 10)
    ).pack(pady=(12, 5))

    value_label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=(FONT, 20, "bold")
    )

    value_label.pack(pady=(0, 10))

    return value_label


products_stat = create_card("عدد المنتجات", "0", COPPER)
quantity_stat = create_card("إجمالي المخزون", "0", GREEN)
value_stat = create_card("قيمة المخزون", "0 ج.م", COPPER)
low_stat = create_card("منتجات منخفضة", "0", RED)

# ==========================================
# المحتوى الرئيسي
# ==========================================

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=28, pady=5)

# لوحة إدخال البيانات
form = tk.Frame(
    main,
    bg=CARD,
    width=290,
    highlightbackground="#292929",
    highlightthickness=1
)

form.pack(side="left", fill="y", padx=(0, 16))
form.pack_propagate(False)

tk.Label(
    form,
    text="إدارة المنتجات",
    font=(FONT, 16, "bold"),
    bg=CARD,
    fg=COPPER
).pack(pady=(20, 5))

tk.Label(
    form,
    text="بيانات المنتج والعمليات",
    font=(FONT, 10),
    bg=CARD,
    fg=GRAY
).pack(pady=(0, 12))


def create_entry(label):
    tk.Label(
        form,
        text=label,
        bg=CARD,
        fg=GRAY,
        font=(FONT, 10)
    ).pack(anchor="e", padx=20, pady=(10, 5))

    entry = tk.Entry(
        form,
        bg="#080808",
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=(FONT, 12),
        justify="right",
        highlightthickness=1,
        highlightbackground="#333333",
        highlightcolor=COPPER
    )

    entry.pack(fill="x", padx=20, ipady=9)

    return entry


name_entry = create_entry("اسم المنتج")
price_entry = create_entry("سعر الوحدة بالجنيه")
qty_entry = create_entry("الكمية")

# ==========================================
# جدول المخزون
# ==========================================

table_frame = tk.Frame(
    main,
    bg=CARD,
    highlightbackground="#292929",
    highlightthickness=1
)

table_frame.pack(side="left", fill="both", expand=True)

table_header = tk.Frame(table_frame, bg=CARD)
table_header.pack(fill="x", padx=18, pady=15)

tk.Label(
    table_header,
    text="سجل المخزون",
    bg=CARD,
    fg=WHITE,
    font=(FONT, 16, "bold")
).pack(side="right")

tk.Label(
    table_header,
    text="INVENTORY",
    bg=CARD,
    fg=COPPER,
    font=(FONT, 9, "bold")
).pack(side="left")

columns = ("id", "name", "price", "quantity", "total")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

table.heading("id", text="الكود")
table.heading("name", text="المنتج")
table.heading("price", text="سعر الوحدة")
table.heading("quantity", text="الكمية")
table.heading("total", text="قيمة المخزون")

table.column("id", width=60, anchor="center")
table.column("name", width=180, anchor="center")
table.column("price", width=125, anchor="center")
table.column("quantity", width=90, anchor="center")
table.column("total", width=140, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=10)
scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 8))

# ==========================================
# تحديث الجدول والإحصائيات
# ==========================================

def refresh():
    for item in table.get_children():
        table.delete(item)

    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()

    total_quantity = 0
    total_value = 0
    low_count = 0

    for pid, name, price, quantity in rows:
        product_value = price * quantity

        table.insert(
            "",
            "end",
            values=(
                pid,
                name,
                f"{price:,.2f} ج.م",
                quantity,
                f"{product_value:,.2f} ج.م"
            )
        )

        total_quantity += quantity
        total_value += product_value

        if quantity <= 5:
            low_count += 1

    products_stat.config(text=str(len(rows)))
    quantity_stat.config(text=str(total_quantity))
    value_stat.config(text=f"{total_value:,.0f} ج.م")
    low_stat.config(text=str(low_count))


# ==========================================
# إضافة منتج
# ==========================================

def add_product():
    name = name_entry.get().strip()

    try:
        price = float(price_entry.get())
        quantity = int(qty_entry.get())

        if not name or price < 0 or quantity < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "خطأ",
            "اكتبي اسم المنتج وسعرًا وكمية صحيحة."
        )
        return

    try:
        cur.execute(
            """
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
            """,
            (name, price, quantity)
        )

        db.commit()
        refresh()
        clear_fields()

        messagebox.showinfo(
            "BHA",
            "تمت إضافة المنتج بنجاح."
        )

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "تنبيه",
            "المنتج موجود بالفعل في قاعدة البيانات."
        )


# ==========================================
# تحديد المنتج من الجدول
# ==========================================

def get_selected():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "تنبيه",
            "اختاري المنتج من الجدول أولًا."
        )
        return None

    return table.item(selected[0])["values"]


# ==========================================
# تسجيل الإنتاج
# ==========================================

def production():
    product = get_selected()

    if product is None:
        return

    try:
        amount = int(qty_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "خطأ",
            "اكتبي كمية إنتاج صحيحة."
        )
        return

    product_id = product[0]

    cur.execute(
        """
        UPDATE products
        SET quantity = quantity + ?
        WHERE id = ?
        """,
        (amount, product_id)
    )

    db.commit()
    refresh()
    clear_fields()

    messagebox.showinfo(
        "BHA | الإنتاج",
        f"تم تسجيل إنتاج {amount} وحدة."
    )


# ==========================================
# تسجيل البيع
# ==========================================

def sale():
    product = get_selected()

    if product is None:
        return

    try:
        amount = int(qty_entry.get())

        if amount <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "خطأ",
            "اكتبي كمية بيع صحيحة."
        )
        return

    product_id = product[0]

    cur.execute(
        """
        SELECT name, price, quantity
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    name, price, quantity = cur.fetchone()

    if amount > quantity:
        messagebox.showerror(
            "المخزون غير كافٍ",
            f"الكمية المتاحة: {quantity}"
        )
        return

    cur.execute(
        """
        UPDATE products
        SET quantity = quantity - ?
        WHERE id = ?
        """,
        (amount, product_id)
    )

    db.commit()
    refresh()
    clear_fields()

    total = amount * price

    messagebox.showinfo(
        "BHA | فاتورة البيع",
        f"المنتج: {name}\n"
        f"الكمية: {amount}\n"
        f"سعر الوحدة: {price:,.2f} جنيه\n"
        f"الإجمالي: {total:,.2f} جنيه"
    )


# ==========================================
# تحديث سعر المنتج المحدد
# ==========================================

def update_price():
    product = get_selected()

    if product is None:
        return

    try:
        price = float(price_entry.get())

        if price < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "خطأ",
            "اكتبي سعرًا صحيحًا."
        )
        return

    cur.execute(
        "UPDATE products SET price = ? WHERE id = ?",
        (price, product[0])
    )

    db.commit()
    refresh()

    messagebox.showinfo(
        "BHA",
        "تم تحديث سعر المنتج."
    )


# ==========================================
# حذف منتج
# ==========================================

def delete_product():
    product = get_selected()

    if product is None:
        return

    confirm = messagebox.askyesno(
        "تأكيد الحذف",
        f"هل تريدين حذف المنتج {product[1]}؟"
    )

    if confirm:
        cur.execute(
            "DELETE FROM products WHERE id = ?",
            (product[0],)
        )

        db.commit()
        refresh()
        clear_fields()


# ==========================================
# مسح الحقول
# ==========================================

def clear_fields():
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)


# ==========================================
# تصميم الأزرار
# ==========================================

def make_button(text, command, color, fg=WHITE):
    return tk.Button(
        form,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=COPPER,
        activeforeground=BG,
        font=(FONT, 11, "bold"),
        relief="flat",
        cursor="hand2",
        pady=10
    )


make_button(
    "＋ إضافة منتج",
    add_product,
    COPPER,
    BG
).pack(fill="x", padx=20, pady=(20, 6))

make_button(
    "⬆ تسجيل الإنتاج",
    production,
    "#242424"
).pack(fill="x", padx=20, pady=6)

make_button(
    "↘ تسجيل البيع",
    sale,
    "#242424"
).pack(fill="x", padx=20, pady=6)

make_button(
    "تحديث سعر المنتج",
    update_price,
    "#242424"
).pack(fill="x", padx=20, pady=6)

make_button(
    "✕ حذف المنتج",
    delete_product,
    "#402020"
).pack(fill="x", padx=20, pady=6)

make_button(
    "مسح الحقول",
    clear_fields,
    "#242424",
    GRAY
).pack(fill="x", padx=20, pady=6)

# ==========================================
# الشريط السفلي
# ==========================================

footer = tk.Frame(root, bg="#080808")
footer.pack(fill="x", side="bottom")

tk.Label(
    footer,
    text="BHA | المؤسسة الهندسية     •     نظام إدارة مصنع النحاس",
    bg="#080808",
    fg=GRAY,
    font=(FONT, 9)
).pack(pady=10)

# تشغيل البرنامج
refresh()
root.mainloop()

db.close()