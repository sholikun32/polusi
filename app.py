import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data Anda dalam bentuk DataFrame
data = pd.DataFrame({
    'id': ['KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01', 'KC01'],
    'tanggal': ['01-01-2023', '01-02-2023', '01-03-2023', '01-04-2023', '01-05-2023', '01-06-2023', '01-07-2023', '01-08-2023', '02-01-2023', '02-02-2023', '02-03-2023'],
    'Karbon_Monoksida': [631.13375, 1542.09125, 1678.3875, 2502.2825, 1555.442917, 1405.5175, 918.19, 692.8829167, 816.385, 780.22375, 1233.6175],
    'NO': [0.417083333, 7.751666667, 4.929166667, 11.30708333, 4.914583333, 5.425833333, 4.875833333, 0.7225, 0.887083333, 0.178333333, 1.321666667],
    'Nitrogen_Dioksida': [13.12041667, 26.56041667, 25.52666667, 48.61083333, 51.46041667, 31.77208333, 26.74333333, 18.05416667, 21.1775, 14.30875, 23.08416667],
    'Ozon': [40.95541667, 19.74708333, 18.89166667, 10.15541667, 38.66583333, 75.32166667, 38.36833333, 84.56458333, 16.83916667, 37.38291667, 11.94708333],
    'Sulfur_Dioksida': [8.485416667, 19.24708333, 17.84125, 38.13416667, 56.80291667, 34.45875, 33.22416667, 33.23375, 13.57583333, 12.43291667, 14.86583333],
    'Parameter_Partikulat_PM2_5': [15.19458333, 74.63375, 65.09291667, 143.59375, 155.2325, 85.3725, 42.70666667, 52.95958333, 25.32625, 33.58708333, 39.13083333],
    'Parameter_Partikulat_PM10': [16.65333333, 85.645, 76.27875, 160.1370833, 165.6883333, 103.9904167, 42.91, 29.3225, 44.50583333, 37.83208333, 44.50583333],
    'ISPU_Karbon_Monoksida': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_NO': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_Nitrogen_Dioksida': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_Ozon': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_Sulfur_Dioksida': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_Parameter_Partikulat_PM2_5': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ISPU_Parameter_Partikulat_PM10': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
})

# Tabel Konversi Nilai Konsentrasi Parameter ISPU
tabel_konversi = {
    'Karbon_Monoksida': [(0, 4000, 4000), (4001, 8000, 8000), (8001, 15000, 15000), (15001, 30000, 30000), (30001, float('inf'), 45000)],
    'NO': [(0, 80, 80), (81, 200, 200), (201, 1130, 1130), (1131, 2260, 2260), (2261, float('inf'), 3000)],
    'Nitrogen_Dioksida': [(0, 80, 80), (81, 200, 200), (201, 1130, 1130), (1131, 2260, 2260), (2261, float('inf'), 3000)],
    'Ozon': [(0, 120, 120), (121, 235, 235), (236, 400, 400), (401, 800, 800), (801, float('inf'), 1000)],
    'Sulfur_Dioksida': [(0, 52, 52), (53, 180, 180), (181, 400, 400), (401, 800, 800), (801, float('inf'), 1200)],
    'Parameter_Partikulat_PM2_5': [(0, 15.5, 15.5), (15.6, 55.4, 55.4), (55.5, 150.4, 150.4), (150.5, 250.4, 250.4), (250.5, float('inf'), 500)],
    'Parameter_Partikulat_PM10': [(0, 50, 50), (51, 100, 150), (101, 200, 350), (201, 300, 420), (300, float('inf'), 500)]
}

# Fungsi untuk menghitung ISPU berdasarkan rumus konversi
def hitung_ispu(x, kolom):
    for batas_bawah, batas_atas, nilai_ispu in tabel_konversi[kolom]:
        if batas_bawah <= x <= batas_atas:
            return ((nilai_ispu - batas_bawah) / (batas_atas - batas_bawah)) * (x - batas_bawah) + nilai_ispu

# Menghitung ISPU untuk setiap kolom
for kolom in tabel_konversi.keys():
    data['ISPU_' + kolom] = data[kolom].apply(hitung_ispu, args=(kolom,))

# Fungsi untuk menentukan kategori ISPU
def tentukan_kategori(ispu):
    if ispu >= 301:
        return 'Berbahaya'
    elif ispu >= 201:
        return 'Sangat Tidak Sehat'
    elif ispu >= 101:
        return 'Tidak Sehat'
    elif ispu >= 51:
        return 'Sedang'
    else:
        return 'Baik'

# Menambahkan kolom kategori ISPU
for kolom in tabel_konversi.keys():
    data['Kategori_' + kolom] = data['ISPU_' + kolom].apply(tentukan_kategori)

# Streamlit App
st.title('Aplikasi Visualisasi ISPU')
st.subheader('Data ISPU dan Kategori')
st.write(data)

# Visualisasi ISPU
selected_parameter = st.selectbox('Pilih Parameter ISPU:', list(tabel_konversi.keys()))
plt.figure(figsize=(10, 6))
plt.plot(data['tanggal'], data['ISPU_' + selected_parameter], marker='o', linestyle='-')
plt.title(f'Grafik ISPU {selected_parameter}')
plt.xlabel('Tanggal')
plt.ylabel('Nilai ISPU')
plt.xticks(rotation=45)
st.pyplot(plt)

# Visualisasi Kategori
plt.figure(figsize=(10, 6))
plt.bar(data['tanggal'], data['Kategori_' + selected_parameter], color='skyblue')
plt.title(f'Kategori ISPU {selected_parameter}')
plt.xlabel('Tanggal')
plt.ylabel('Kategori')
plt.xticks(rotation=45)
st.pyplot(plt)
