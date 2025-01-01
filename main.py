import pandas as pd
import os
import sys
import csv
from tabulate import tabulate

# Variabel global untuk melacak status login, peran pengguna dan menyimpan username pengguna yang login
login_status = False  
current_user_role = None
current_user_username = None  

def clear_alert(n=1):
    for _ in range(n):
        print("\033[F\033[K", end='')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# DATA HANDLING

def cek_file(file):
    try:
        data = pd.read_csv(file)
        required_columns = {'username', 'password', 'nama', 'role'}
        if not required_columns.issubset(data.columns):
            print(f"Kolom pada file '{file}' tidak sesuai.")
            sys.exit()
        return data
    except FileNotFoundError:
        print(f"File '{file}' tidak ditemukan.")
        sys.exit()

def cek_item():
    try:
        items = pd.read_csv("items.csv")
        return items
    except FileNotFoundError:
        print("File 'items.csv' tidak ditemukan. Membuat file baru.")
        items = pd.DataFrame(columns=['index', 'item_name','jumlah', 'price', 'game'])
        items.to_csv("items.csv", index=False)
        return items

def cek_stokdiamond():
    clear_terminal()
    try:
        diamonds = pd.read_csv("diamond_stock.csv")
        return diamonds
    except FileNotFoundError:
        print("File 'diamond_stock.csv' tidak ditemukan. Membuat file baru.")
        diamonds = pd.DataFrame(columns=['diamond_type', 'stock'])
        diamonds.to_csv("diamond_stock.csv", index=False)
        return diamonds

def cek_kupon():
    try:
        coupons = pd.read_csv("kupon.csv")
        return coupons
    except FileNotFoundError:
        print("File 'coupons.csv' tidak ditemukan. Membuat file baru.")
        coupons = pd.DataFrame(columns=['code', 'discount'])
        coupons.to_csv("kupon.csv", index=False)
        return coupons

def cek_riwayat_pembelian():
    try:
        riwayat = pd.read_csv("riwayat_pembelian.csv")
    except FileNotFoundError:
        print("File 'riwayat_pembelian.csv' tidak ditemukan. Membuat file baru.")
        riwayat = pd.DataFrame(columns=['username', 'game', 'item_name', 'jumlah', 'price', 'game_id', 'nickname'])
        riwayat.to_csv("riwayat_pembelian.csv", index=False)
    except pd.errors.EmptyDataError:
        # Jika file ada tetapi kosong
        riwayat = pd.DataFrame(columns=['username', 'game', 'item_name', 'jumlah', 'price', 'game_id', 'nickname'])
    return riwayat

def simpan_item(items):
    items.to_csv("items.csv", index=False)

def simpan_diamond_stock(diamonds):
    diamonds.to_csv("diamond_stock.csv", index=False)


def simpan_riwayat_pembelian(riwayat):
    riwayat.to_csv("riwayat_pembelian.csv", index=False)

# LOGIN & REGISTRASI
def login():
    global login_status, current_user_role, current_user_username
    data = cek_file("users.csv")
    while True:
        clear_terminal()
        print("==== LOGIN ====")
        username = input("Masukkan Username: ").strip()
        password = input("Masukkan Password: ").strip()     
        user = data[(data['username'] == username) & (data['password'] == password)]
        if len(user) > 0:
            nama = user.iloc[0]['nama']
            role = user.iloc[0]['role']
            login_status, current_user_role, current_user_username = True, role, username
            clear_terminal()
            print(f"LOGIN BERHASIL..!!✅")
            print(f"Selamat datang di Algopedia, {nama} sebagai ({role})")
            input("Tekan Enter untuk melanjutkan.")
            return role      
        print("\nUsername atau Password salah.")
        input("Tekan Enter untuk mencoba lagi.")
        clear_alert(3)

def register():
    data = cek_file("users.csv")
    clear_terminal()
    print("==== REGISTRASI ====")
    username = input("Masukkan Username: ").strip()
    password = input("Masukkan Password: ").strip()
    nama = input("Masukkan Nama Lengkap: ").strip()
    # Menetapkan role sebagai 'user' secara default
    role = 'user'
    # Memeriksa apakah username sudah ada
    if username in data['username'].values:
        print("Username sudah ada. Silakan pilih username lain.")
        return
    # Menambahkan pengguna baru ke DataFrame
    new_user = pd.DataFrame([{
        'username': username,
        'password': password,
        'nama': nama,
        'role': role
    }])
    data = pd.concat([data, new_user], ignore_index=True)
    data.to_csv("users.csv", index=False)
    print("REGISTRASI BERHASIL..!!✅")

# MENU ADMIN
def menu_admin():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║            MENU ADMIN             ║
║┌─────────────────────────────────┐║
║│  1. Kelola Stok Diamond         │║
║│  2. Kelola Item                 │║
║│  3. Kelola Kupon                │║
║│  4. Lihat Riwayat Pembelian     │║
║│  5. Kembali ke Menu Utama       │║
║├─────────────────────────────────┤║
║│            ALGOPEDIA            │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            submenu_kelola_stok_diamond()
        elif pilihan == '2':
            submenu_kelola_item()
        elif pilihan == '3':
            submenu_kelola_kupon()
        elif pilihan == '4':
            riwayat_pembelian()
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak ada minn.")
        input("Tekan Enter untuk melanjutkan.")

# KELOLA ITEM
def submenu_kelola_item():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║           KELOLA ITEM             ║
║┌─────────────────────────────────┐║
║│  1. Tambah Item                 │║
║│  2. Edit Item                   │║
║│  3. Hapus Item                  │║
║│  4. Kembali                     │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            tambah_item()
        elif pilihan == '2':
            edit_item()
        elif pilihan == '3':
            hapus_item()
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak ada minn.")
        input("Tekan Enter untuk melanjutkan.")

def tambah_item():
    items = cek_item()
    clear_terminal()
    print("Tambah Item")
    if not items.empty:
        print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("Tidak ada item yang tersedia.")
        return
    index = len(items) + 1
    item_name = input("Nama item: ").strip()
    jumlah = float(input("jumlah diamond/UC: ").strip())
    price = float(input("Harga item: ").strip())
    game = input("Game (Mobile Legends, PUBG, Free Fire): ").strip()
    # Tambahkan item baru
    new_item = pd.DataFrame([{
        'index': index,
        'item_name': item_name,
        'jumlah': jumlah,
        'price': price,
        'game': game
    }])
    items = pd.concat([items, new_item], ignore_index=True)
    simpan_item(items)
    print("Item berhasil ditambahkan.")
    clear_terminal()
    print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))

def edit_item():
    items = cek_item()
    clear_terminal()
    # Menampilkan daftar item yang tersedia
    print("=== EDIT ITEM ===")
    if not items.empty:
        print("Item yang tersedia untuk diubah:")
        print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("Tidak ada item yang tersedia.")
        return

    try:
        index = int(input("Masukkan index item yang ingin diedit: ").strip())
        item = items[items['index'] == index]

        if not item.empty:
            # Menampilkan nilai item yang akan diedit
            print(f"\nItem yang akan diedit: {item.iloc[0]['item_name']}")
            item_name = input(f"Nama item ({item.iloc[0]['item_name']}): ").strip()
            jumlah = float(input(f"Jumlah diamond/UC ({item.iloc[0]['jumlah']}): ").strip())
            price = float(input(f"Harga item ({item.iloc[0]['price']}): ").strip())
            game = input(f"Game ({item.iloc[0]['game']}): ").strip()
            
            # Update item dengan nilai baru
            items.loc[items['index'] == index, ['item_name','jumlah','price', 'game']] = [item_name, jumlah, price, game]
            simpan_item(items)
            print("Item berhasil diperbarui.")
        else:
            print("Item tidak ditemukan.")
    except ValueError:
        print("Input tidak valid. Pastikan Anda memasukkan nilai yang benar.")

    clear_terminal()
    print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))

def hapus_item():
    clear_terminal()
    items = cek_item()   
    # Menampilkan daftar item yang ada untuk admin
    print("Daftar item yang tersedia:")
    print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))   
    try:
        index = int(input("Masukkan index item yang ingin dihapus: ").strip())
        item = items[items['index'] == index]      
        if not item.empty:
            # Konfirmasi penghapusan item
            confirm = input(f"Apakah Anda yakin ingin menghapus item '{item.iloc[0]['item_name']}' (iya/tidak)? ").strip().lower()            
            if confirm == 'iya':
                # Menghapus item berdasarkan index
                items = items[items['index'] != index]
                simpan_item(items)
                print(f"Item '{item.iloc[0]['item_name']}' berhasil dihapus.")
            else:
                print("Penghapusan gagal.")
        else:
            print("Item tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.") 
    clear_terminal()
    print(tabulate(items, headers='keys', tablefmt='pretty', showindex=False))

# KELOLA STOK DIAMOND
def submenu_kelola_stok_diamond():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║         KELOLA STOK DIAMOND       ║
║┌─────────────────────────────────┐║
║│  1. Lihat Stok Diamond          │║
║│  2. Edit Stok Diamond           │║
║│  3. Kembali                     │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            lihat_stok_diamond()
        elif pilihan == '2':
            edit_stok_diamond()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak ada minn.")
        input("Tekan Enter untuk melanjutkan.")

def lihat_stok_diamond():
    diamonds = cek_stokdiamond()
    if diamonds.empty:
        print("Stok diamond kosong.")
    else:
        print(tabulate(diamonds, headers='keys', tablefmt='pretty', showindex=False ))

def edit_stok_diamond():
    diamonds = cek_stokdiamond()
    clear_terminal()
    print("Edit Stok")
    if not diamonds.empty:
        print(tabulate(diamonds, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("Tidak ada stok yang tersedia.")
        return
    diamond_type = input("Masukkan jenis diamond/UC (Diamond Mobile Legend, UC PUBG Mobile, Diamond Free Fire): ").strip()
    # Mengecek apakah jenis diamond/UC ada di stok
    if diamond_type not in diamonds['diamond_type'].values:
        print(f"{diamond_type} tidak ditemukan.")
        return
    # Tampilkan stok saat ini
    current_stock = diamonds.loc[diamonds['diamond_type'] == diamond_type, 'stock'].values[0]
    print(f"Stok {diamond_type} adalah {current_stock}")
    try:
        new_stock = float(input(f"Masukkan jumlah stok baru untuk {diamond_type}: ").strip())
        diamonds.loc[diamonds['diamond_type'] == diamond_type, 'stock'] = new_stock
        simpan_diamond_stock(diamonds)
        print(f"Stok {diamond_type} berhasil diperbarui menjadi {new_stock}.")
    except ValueError:
        print("Input tidak valid. Harap masukkan angka untuk jumlah stok.")
    clear_terminal()
    print(tabulate(diamonds, headers='keys', tablefmt='pretty', showindex=False))

# KELOLA KUPON
def submenu_kelola_kupon():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║           KELOLA KUPON            ║
║┌─────────────────────────────────┐║
║│  1. Tambah Kupon                │║
║│  2. Edit Kupon                  │║
║│  3. Hapus Kupon                 │║
║│  4. Kembali                     │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            tambah_kupon("kupon.csv")
        elif pilihan == '2':
            edit_kupon("kupon.csv")
        elif pilihan == '3':
            hapus_kupon("kupon.csv")
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak ada minn.")
        input("Tekan Enter untuk melanjutkan.")

def tampilkan_kupon(kupon_list):
    print("\nDaftar Kupon:")
    print(tabulate(kupon_list, headers='keys', tablefmt='pretty',showindex=False))

def tambah_kupon(file):
    clear_terminal()
    print("Tambah Kupon")
    
    # Membaca data dari kupon.csv
    kupon_list = cek_kupon()
    
    # Menampilkan kupon sebelum ditambah
    tampilkan_kupon(kupon_list)

    code = input("Masukkan kode kupon: ").strip()
    discount = float(input("Masukkan diskon kupon (%): ").strip())

    # Menambahkan kupon baru
    new_coupon = pd.DataFrame([{
        'code': code,
        'discount': discount
    }])
    kupon_list = pd.concat([kupon_list, new_coupon], ignore_index=True)
    simpan_kupon(kupon_list)
    print("Kupon berhasil ditambahkan.")
    
    # Menampilkan kupon setelah ditambah
    clear_terminal()
    tampilkan_kupon(kupon_list)

def simpan_kupon(kupon_list):
    kupon_list.to_csv("kupon.csv", index=False)

def edit_kupon(file):
    clear_terminal()
    print("Edit Kupon")
    # Membaca data dari kupon.csv
    kupon_list = cek_kupon()
    # Menampilkan kupon sebelum diedit
    tampilkan_kupon(kupon_list) 
    code = input("Masukkan kode kupon yang ingin diedit: ").strip()
    # Memeriksa apakah kupon ada
    if code in kupon_list['code'].values:
        new_discount = float(input("Masukkan diskon baru kupon (%): ").strip())
        kupon_list.loc[kupon_list['code'] == code, 'discount'] = new_discount
        simpan_kupon(kupon_list)
        print("Kupon berhasil diperbarui.")
    else:
        print("Kupon tidak ditemukan.")
    # Menampilkan kupon setelah diedit
    clear_terminal()
    tampilkan_kupon(kupon_list)

def hapus_kupon(file):
    clear_terminal()
    print("Hapus Kupon")
    # Membaca data dari kupon.csv
    kupon_list = cek_kupon()
    # Menampilkan kupon sebelum dihapus
    tampilkan_kupon(kupon_list)
    code = input("Masukkan kode kupon yang ingin dihapus: ").strip() 
    # Memeriksa apakah kupon ada
    if code in kupon_list['code'].values:
        kupon_list = kupon_list[kupon_list['code'] != code]
        simpan_kupon(kupon_list)
        print("Kupon berhasil dihapus.")
    else:
        print("Kupon tidak ditemukan.")
    # Menampilkan kupon setelah dihapus
    clear_terminal()
    tampilkan_kupon(kupon_list)

# RIWAYAT PEMBELIAN
def riwayat_pembelian():
    clear_terminal()
    if current_user_role != 'admin':
        print("Anda tidak memiliki akses untuk melihat riwayat pembelian.")
        return
    print("=== RIWAYAT PEMBELIAN ===")
    riwayat = cek_riwayat_pembelian()
    if riwayat.empty:
        print("Belum ada riwayat pembelian.")
    else:
        print(tabulate(riwayat, headers='keys', tablefmt='pretty', showindex=False))

# MENU USER
def menu_user():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║    SELAMAT DATANG DI ALGOPEDIA    ║
║┌─────────────────────────────────┐║
║│  1. Topup Diamond               │║
║│  2. Skin Mobile Legends         │║
║│  3. Kembali ke Menu Utama       │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            topup_diamond()
        elif pilihan == '2':
            skin_ML()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak ada kakakk🙏🏻")
        input("Tekan Enter untuk melanjutkan.")

def topup_diamond():
    clear_terminal()
    print("""
╔═══════════════════════════════════╗
║           TOP UP DIAMOND          ║
║┌─────────────────────────────────┐║
║│  1. Mobile Legend (ML)          │║
║│  2. PUBG Mobile                 │║
║│  3. Free Fire (FF)              │║
╚═══════════════════════════════════╝
"""
    )
    pilihan_game = input("Silahkan mau game apa kakk(1/2/3): ").strip()
    
    if pilihan_game == '1':
        game_name = "Mobile Legends"
        diamond_type = "Diamond Mobile Legend"
    elif pilihan_game == '2':
        game_name = "PUBG"
        diamond_type = "UC PUBG Mobile"
    elif pilihan_game == '3':
        game_name = "Free Fire"
        diamond_type = "Diamond Free Fire"
    else:
        print("Pilihan game tidak valid.")
        return
    
    print(f"Game yang dipilih: {game_name}")
    
    # Filter item berdasarkan game yang dipilih
    clear_terminal()
    items = cek_item()
    filtered_items = items[items['game'] == game_name]
    
    if not filtered_items.empty:
        print(f"Items untuk game {game_name}:")
        print(tabulate(filtered_items, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print(f"Tidak ada item yang tersedia untuk game {game_name}.")
        return

    try:
        item_index = int(input("Masukkan index item yang ingin di-top up: ").strip())
        item = filtered_items[filtered_items['index'] == item_index]
        if not item.empty:
            # Ambil harga dari item yang dipilih
            price_per_item = item.iloc[0]['price']
            total_price = price_per_item  # Total harga diambil dari harga item

            # Input ID dan nickname
            game_id = int(input(f"Masukkan ID {game_name}: ").strip())
            nickname = input(f"Masukkan Nickname {game_name}: ").strip()

            # Input kupon
            coupon_code = input("Masukkan kode kupon (jika ada, tekan Enter jika tidak): ").strip()
            discount = 0
            
            # Cek kupon dan hitung diskon
            coupons = cek_kupon()
            if coupon_code in coupons['code'].values:
                discount = total_price * (coupons[coupons['code'] == coupon_code]['discount'].values[0] / 100)
                print(f"Kupon '{coupon_code}' diterapkan. Diskon: {discount}")
            else:
                print("Kupon tidak valid.")

            final_price = total_price - discount

            # Konfirmasi sebelum melanjutkan transaksi
            print("\n==== Konfirmasi ====")
            print(f"ID {game_name}: {game_id}")
            print(f"Nickname {game_name}: {nickname}")
            print(f"Item yang dipilih: {item.iloc[0]['item_name']}")
            print(f"Total harga: {final_price}")
            konfirmasi = input("Apakah informasi di atas sudah benar? (iya/tidak): ").strip().lower()

            if konfirmasi != 'iya':
                print("Transaksi dibatalkan.")
                return

            print("\nSilakan lakukan transfer ke rekening berikut:")
            print("Rekening BCA: 1234567890")
            print("Rekening Mandiri: 9876543210")
            print("Pastikan jumlah transfer sesuai dengan harga item yang dipilih.")

            # Verifikasi transfer
            transfer_verifikasi = input("Sudah melakukan transfer? (iya/tidak): ").strip().lower()
            if transfer_verifikasi != 'iya':
                print("Transaksi dibatalkan. Silakan transfer terlebih dahulu.")
                return

            # Cek dan kurangi stok diamond/UC
            diamonds = cek_stokdiamond()
            stok = diamonds.loc[diamonds['diamond_type'] == diamond_type, 'stock'].values
            jumlah_diamond = item.iloc[0]['jumlah']
            if stok and stok[0] >= jumlah_diamond:  
                diamonds.loc[diamonds ['diamond_type'] == diamond_type, 'stock'] -= jumlah_diamond
                simpan_diamond_stock(diamonds)

                # Simpan ke riwayat pembelian
                riwayat = cek_riwayat_pembelian()
                new_entry = pd.DataFrame([{
                    'username': current_user_username,  # Menggunakan username pengguna yang login
                    'game': game_name,
                    'item_name': item.iloc[0]['item_name'],
                    'jumlah': jumlah_diamond, 
                    'price': price_per_item,
                    'game_id': game_id,
                    'nickname': nickname
                }])
                riwayat = pd.concat([riwayat, new_entry], ignore_index=True)
                simpan_riwayat_pembelian(riwayat)

                print(f"SELAMAATTT ANDA TELAH BERHASIL TOP UP")
            else:
                print(f"Stok {diamond_type} tidak mencukupi untuk transaksi.")
        else:
            print("Item tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")

def skin_ML():
    clear_terminal()
    # Load skin Mobile Legends
    try:
        ml_skins = pd.read_csv("ml_skins.csv")
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    if not ml_skins.empty:
        print(f"Skin Mobile Legends yang tersedia:")
        print(tabulate(ml_skins, headers='keys', tablefmt='pretty', showindex=False))
    else:
        print("Tidak ada skin yang tersedia untuk Mobile Legends.")
        return

    try:
        item_index = int(input("Masukkan index skin yang ingin dibeli: ").strip())
        item = ml_skins[ml_skins['index'] == item_index]
        if not item.empty:
            # Input ID dan Nickname setelah pemilihan skin
            game_id = input("Masukkan ID Mobile Legends Anda: ").strip()
            nickname = input("Masukkan Nickname Mobile Legends Anda: ").strip()

            # Konfirmasi sebelum melanjutkan transaksi
            print("\n==== Konfirmasi ====")
            print(f"ID Mobile Legends: {game_id}")
            print(f"Nickname Mobile Legends: {nickname}")
            print(f"Skin yang dipilih: {item.iloc[0]['skin_name']}")
            print(f"Price: {item.iloc[0]['price']}")
            konfirmasi = input("Apakah informasi di atas sudah benar? (iya/tidak): ").strip().lower()

            if konfirmasi != 'iya':
                print("Transaksi dibatalkan.")
                return

            print("\nSilakan lakukan transfer ke rekening berikut:")
            print("Rekening BCA: 1234567890")
            print("Rekening Mandiri: 9876543210")
            print("Pastikan jumlah transfer sesuai dengan harga skin yang dipilih.")

            # Verifikasi transfer
            transfer_verifikasi = input("Sudah melakukan transfer? (iya/tidak): ").strip().lower()
            if transfer_verifikasi != 'iya':
                print("Transaksi dibatalkan. Silakan transfer terlebih dahulu.")
                return

            # Simpan ke riwayat pembelian
            riwayat = cek_riwayat_pembelian()
            new_entry = pd.DataFrame([{
                'username': current_user_username,  # Menggunakan username pengguna yang login
                'game': "Mobile Legends",
                'item_name': item.iloc[0]['skin_name'],
                'jumlah': 1,
                'price': item.iloc[0]['price'],
                'game_id': game_id,
                'nickname': nickname
            }])
            riwayat = pd.concat([riwayat, new_entry], ignore_index=True)
            simpan_riwayat_pembelian(riwayat)

            print(f"Skin '{item.iloc[0]['skin_name']}' berhasil dibeli!")
        else:
            print("Skin tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")
 
# MENU UTAMA
def menu_utama():
    while True:
        clear_terminal()
        print(
"""
╔═══════════════════════════════════╗
║          Selamat datangg          ║
║┌─────────────────────────────────┐║
║│  1. Login                       │║
║│  2. Registrasi                  │║
║│  3. Keluar                      │║
║│                                 │║
║│            ALGOPEDIA            │║
╚═══════════════════════════════════╝
"""
        )
        pilihan = input("Pilih opsi: ").strip()
        if pilihan == '1':
            role = login()
            if role == 'admin':
                menu_admin()
            else:
                menu_user()
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu_utama()
