import streamlit as st
import requests
import pandas as pd
import io

# Fungsi untuk mengambil data dari API
def fetch_data(kecamatan, tgl_awal, tgl_akhir):
    url = "http://119.2.50.171/sendpusk/data-polusi/kecamatan"
    params = {
        "kec": kecamatan,
        "tgl_awal": tgl_awal,
        "tgl_akhir": tgl_akhir
    }
    response = requests.get(url, params=params)
    return response

# Fungsi untuk menampilkan data sebagai tabel dan mengunduh sebagai Excel
def display_data():
    st.title("Aplikasi Data Polusi Udara")

    # Input dari pengguna untuk memilih kecamatan, tanggal awal, dan tanggal akhir
    kecamatan = st.text_input("Nama Kecamatan", "semarangtengah")
    tgl_awal = st.text_input("Tanggal Awal (dd-mm-yyyy)", "01-01-2023")
    tgl_akhir = st.text_input("Tanggal Akhir (dd-mm-yyyy)", "10-09-2023")

    if st.button("Cari Data"):
        response = fetch_data(kecamatan, tgl_awal, tgl_akhir)

        if response.status_code == 200:
            data = response.json()["data"]

            data_list = []
            for item in data:
                komponen = item["komponen"]
                data_entry = {
                    "kode": item["kode"],
                    "kode_kecamatan": item["kode_kecamatan"],
                    "kecamatan": item["kecamatan"],
                    "aqi": item["aqi"],
                    "komponen/co": komponen["co"],
                    "komponen/no": komponen["no"],
                    "komponen/no2": komponen["no2"],
                    "komponen/o3": komponen["o3"],
                    "komponen/so2": komponen["so2"],
                    "komponen/pm2_5": komponen["pm2_5"],
                    "komponen/pm10": komponen["pm10"],
                    "komponen/nh3": komponen["nh3"],
                    "tanggal": item["tanggal"],
                    "lon": item["lon"],
                    "lat": item["lat"]
                }
                data_list.append(data_entry)

            df = pd.DataFrame(data_list)

            # Menampilkan data dalam bentuk tabel
            st.write(df)

            # Mengunduh data sebagai file Excel
            excel_data = df.to_excel(index=False, engine='openpyxl', encoding='utf-8-sig')
            st.download_button(
                label="Unduh Data Excel",
                data=excel_data,
                file_name="data_polusi.xlsx",
                key="download_data_button"
            )
        else:
            st.error("Gagal mengambil data. Kode status:", response.status_code)

if __name__ == '__main__':
    display_data()
