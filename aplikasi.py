import json
import os
import getpass
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress
from rich import box
from rich.layout import Layout
from rich.text import Text

console = Console()

class Product:
    def __init__(self, id, name, price, stock, category="Electronics"):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'category': self.category
        }

class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, product, quantity=1):
        if product.id in self.items:
            self.items[product.id]['quantity'] += quantity
        else:
            self.items[product.id] = {
                'product': product,
                'quantity': quantity
            }
    
    def remove_item(self, product_id, quantity=1):
        if product_id in self.items:
            if self.items[product_id]['quantity'] <= quantity:
                del self.items[product_id]
            else:
                self.items[product_id]['quantity'] -= quantity
    
    def get_total(self):
        total = 0
        for item in self.items.values():
            total += item['product'].price * item['quantity']
        return total
    
    def display_cart(self):
        table = Table(title="🛒 Keranjang Belanja", box=box.ROUNDED)
        table.add_column("Produk", style="cyan", no_wrap=True)
        table.add_column("Harga", style="green")
        table.add_column("Jumlah", style="yellow")
        table.add_column("Subtotal", style="magenta")
        
        for item in self.items.values():
            product = item['product']
            subtotal = product.price * item['quantity']
            table.add_row(
                product.name,
                f"Rp {product.price:,}",
                str(item['quantity']),
                f"Rp {subtotal:,}"
            )
        
        table.add_row("", "", "Total:", f"Rp {self.get_total():,}", style="bold green")
        console.print(table)

class ShoppingApp:
    def __init__(self):
        self.products = []
        self.cart = ShoppingCart()
        self.load_products()
    
    def load_products(self):
        # Data produk default dengan kategori
        default_products = [
            Product(1, "Laptop Gaming", 12000000, 10, "Electronics"),
            Product(2, "Smartphone Flagship", 8000000, 15, "Electronics"),
            Product(3, "Headphone Wireless", 1500000, 20, "Audio"),
            Product(4, "Mouse Gaming", 500000, 30, "Computer"),
            Product(5, "Mechanical Keyboard", 1200000, 25, "Computer"),
            Product(6, "Monitor 4K", 3500000, 8, "Computer"),
            Product(7, "Printer Laser", 2500000, 12, "Office"),
            Product(8, "Webcam HD", 750000, 18, "Computer"),
            Product(9, "SSD 1TB", 1500000, 20, "Computer"),
            Product(10, "Power Bank", 500000, 25, "Accessories")
        ]
        self.products = default_products
    
    def display_products(self, category_filter=None):
        table = Table(title="📦 Daftar Produk", box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nama", style="green")
        table.add_column("Kategori")
        table.add_column("Harga", style="yellow")
        table.add_column("Stok", style="red")
        
        filtered_products = self.products
        if category_filter and category_filter != "Semua":
            filtered_products = [p for p in self.products if p.category == category_filter]
        
        for product in filtered_products:
            stock_style = "green" if product.stock > 5 else "yellow" if product.stock > 0 else "red"
            table.add_row(
                str(product.id),
                product.name,
                product.category,
                f"Rp {product.price:,}",
                Text(str(product.stock), style=stock_style)
            )
        
        console.print(table)
    
    def get_categories(self):
        categories = set(product.category for product in self.products)
        return ["Semua"] + sorted(list(categories))
    
    def find_product(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None
    
    def add_to_cart(self):
        categories = self.get_categories()
        
        # Tampilkan pilihan kategori
        category_table = Table(title="Pilih Kategori", box=box.SIMPLE)
        for i, category in enumerate(categories):
            category_table.add_row(f"{i+1}. {category}")
        
        console.print(category_table)
        
        try:
            category_choice = IntPrompt.ask("Pilih kategori", choices=[str(i+1) for i in range(len(categories))])
            selected_category = categories[category_choice-1]
            
            self.display_products(selected_category)
            
            product_id = IntPrompt.ask("Masukkan ID produk yang ingin dibeli")
            quantity = IntPrompt.ask("Masukkan jumlah", default=1)
            
            product = self.find_product(product_id)
            if product:
                if product.stock >= quantity:
                    self.cart.add_item(product, quantity)
                    product.stock -= quantity
                    console.print(f"✅ [green]{quantity} {product.name}[/green] ditambahkan ke keranjang!")
                else:
                    console.print("❌ [red]Stok tidak mencukupi![/red]")
            else:
                console.print("❌ [red]Produk tidak ditemukan![/red]")
        except Exception as e:
            console.print(f"❌ [red]Terjadi kesalahan: {str(e)}[/red]")
    
    def checkout(self):
        if not self.cart.items:
            console.print("❌ [red]Keranjang kosong![/red]")
            return
        
        self.cart.display_cart()
        
        if Confirm.ask("\n💳 Apakah Anda ingin melanjutkan pembayaran?"):
            total = self.cart.get_total()
            
            # Simulasi proses pembayaran dengan progress bar
            with Progress() as progress:
                task = progress.add_task("[green]Memproses pembayaran...", total=100)
                
                for i in range(100):
                    progress.update(task, advance=1)
                    # Simulasi delay
                    import time
                    time.sleep(0.02)
            
            console.print(Panel.fit(
                f"✅ [bold green]Pembayaran berhasil![/bold green]\n\n"
                f"Total: [cyan]Rp {total:,}[/cyan]\n"
                f"Terima kasih telah berbelanja!",
                title="🎉 Transaksi Selesai",
                border_style="green"
            ))
            
            # Simpan riwayat transaksi
            order = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'items': {id: {'name': item['product'].name, 
                              'quantity': item['quantity'], 
                              'price': item['product'].price} 
                         for id, item in self.cart.items.items()},
                'total': total
            }
            
            try:
                with open('orders.json', 'a') as f:
                    json.dump(order, f)
                    f.write('\n')
            except:
                pass
                
            self.cart = ShoppingCart()  # Reset keranjang
        else:
            console.print("❌ [yellow]Checkout dibatalkan![/yellow]")
    
    def show_main_menu(self):
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        header_text = Text("🏪 TOKO ELEKTRONIK XYZ", style="bold blue on white", justify="center")
        layout["header"].update(Panel(header_text, style="white on blue"))
        
        # Main content
        menu_table = Table.grid(padding=(1, 2))
        menu_table.add_row("1. Lihat Produk")
        menu_table.add_row("2. Tambah ke Keranjang")
        menu_table.add_row("3. Lihat Keranjang")
        menu_table.add_row("4. Checkout")
        menu_table.add_row("5. Keluar")
        
        layout["main"].update(Panel(menu_table, title="Menu Utama", border_style="green"))
        
        # Footer
        footer_text = Text("Selamat berbelanja! 🛍️", style="italic yellow", justify="center")
        layout["footer"].update(Panel(footer_text))
        
        console.print(layout)
    
    def run(self):
        while True:
            console.clear()
            self.show_main_menu()
            
            choice = Prompt.ask("Pilih menu", choices=["1", "2", "3", "4", "5"])
            
            if choice == '1':
                console.clear()
                self.display_products()
                Prompt.ask("\nTekan Enter untuk kembali ke menu utama")
            elif choice == '2':
                console.clear()
                self.add_to_cart()
                Prompt.ask("\nTekan Enter untuk kembali ke menu utama")
            elif choice == '3':
                console.clear()
                if self.cart.items:
                    self.cart.display_cart()
                else:
                    console.print("🛒 Keranjang Anda masih kosong!")
                Prompt.ask("\nTekan Enter untuk kembali ke menu utama")
            elif choice == '4':
                console.clear()
                self.checkout()
                Prompt.ask("\nTekan Enter untuk kembali ke menu utama")
            elif choice == '5':
                console.print("👋 [blue]Terima kasih telah menggunakan aplikasi kami![/blue]")
                break

# Menjalankan aplikasi
if __name__ == "__main__":
    app = ShoppingApp()
    app.run()
