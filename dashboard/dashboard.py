#!/usr/bin/env python
# coding: utf-8

# # Dashboard Data: E-Commerce Public Dataset
# - Nama:Yoga Kusuma Wardhana
# - Email: yogawardh@gmail.com
# - Id Dicoding: yogawardh

# ## Import Library

# In[1]:


# Import libraries

import pandas as pd
import streamlit as st


# ## Data Wrangling

# ### Gathering Data

# In[2]:


# Memuat tabel yang diperlukan

orders_df = pd.read_csv("orders_dataset.csv")
order_items_df = pd.read_csv("order_items_dataset.csv")
order_payments_df = pd.read_csv("order_payments_dataset.csv")
products_df = pd.read_csv("products_dataset.csv")


# ### Cleaning Data

# In[3]:


# Menghapus data yang mengandung missing values

products_df = products_df.dropna(subset=['product_category_name'])
products_df.info()


# ## Exploratory Data Analysis (EDA)

# ### Pertanyaan 1

# In[4]:


# Menghitung frekuensi munculnya tiap tipe pembayaran

payment_counts = order_payments_df['payment_type'].value_counts()
print(payment_counts)


# In[5]:


# Mencari tipe pembayaran terbanyak

most_used_payment = payment_counts.idxmax()

# Menghitung total penggunaan

total_used = payment_counts.max()

# Tampilkan hasil

print("Metode pembayaran paling banyak digunakan adalah:", most_used_payment, "dengan jumlah penggunaan", total_used, "kali")


# ### Pertanyaan 2

# In[6]:


# Menggabungkan dataset orders dan order_payments

merged_payments_df = pd.merge(orders_df, order_payments_df, on=['order_id'], how='inner')
merged_payments_df.head()


# In[7]:


# Mengetahui total uang yang dibelanjakan oleh setiap pelanggan

monetary_df = merged_payments_df.groupby('customer_id')['payment_value'].sum().reset_index()

# Menampilkan total uang yang dibelanjakan oleh pelanggan

print(monetary_df)


# In[8]:


# Menghitung rata-rata uang yang dibelanjakan oleh pelanggan pada satu kali transaksi

avg_payment_per_order = merged_payments_df.groupby(['customer_id', 'order_id'])['payment_value'].sum().mean()

# Menampilkan rata-rata uang yang dibelanjakan oleh pelanggan pada satu kali transaksi

print(avg_payment_per_order)


# In[9]:


# Membuat fungsi untuk menentukan segmentasi pelanggan

def customer_segment(payment):
    if payment < 40:
        return 'bronze'
    elif payment >= 40 and payment < 80:
        return 'silver'
    elif payment >= 80 and payment < 160:
        return 'gold'
    else:
        return 'diamond'

# Menambahkan kolom segmen ke dalam DataFrame

monetary_df['segment'] = monetary_df['payment_value'].apply(customer_segment)

# Menampilkan total belanja pelanggan beserta segmentasinya

print(monetary_df)


# ### Pertanyaan 3

# In[10]:


# Menggabungkan data dari ketiga dataset

merged_df = pd.merge(orders_df, order_items_df, on='order_id')
merged_all = pd.merge(merged_df, products_df, on='product_id')

# Filter hanya pesanan dengan order_status "delivered"

delivered_df = merged_all[merged_all['order_status'] == 'delivered']

# Menghitung jumlah produk yang terjual per kategori produk

product_category_sales = delivered_df['product_category_name'].value_counts().reset_index()
product_category_sales.columns = ['product_category_name', 'qty_sold']

# Menampilkan jumlaah produk yang terjual per kategori produk

product_category_sales.head(10)


# In[11]:


# Mencari kategori dengan penjualan paling banyak

most_sold = product_category_sales.loc[product_category_sales['qty_sold'].idxmax()]

# Mencari kategori dengan penjualan paling sedikit

least_sold = product_category_sales.loc[product_category_sales['qty_sold'].idxmin()]

# Menampilkan kategori dengan penjualan paling banyak

print("Kategori produk yang paling banyak terjual adalah:", most_sold['product_category_name'])

# Menampilkan kategori dengan penjualan paling sedikit

print("Kategori produk yang paling sedikit terjual adalah:", least_sold['product_category_name'])


# In[ ]:





# ## Streamlit Dashboard

# In[ ]:


# Judul Dashboard
st.title("E-Commerce Data Visualization")

# Visualisasi metode pembayaran
st.header("Metode Pembayaran yang Paling Banyak Digunakan")
st.markdown("Visualisasai ini menunjukkan metode pembayaran yang digunakan oleh pelanggan.")
sorted_payment_counts = payment_counts.sort_values(ascending=False)
st.bar_chart(sorted_payment_counts, use_container_width=True)

# Visualisasi segmentasi pelanggan
st.header("Segmentasi Pelanggan")
st.markdown("Visualisasai ini menunjukkan segmentasi dari pelanggaan E-Commerce.")
segment_counts = monetary_df['segment'].value_counts().sort_values(ascending=False)
st.bar_chart(segment_counts, use_container_width=True)

# Visualisasi kategori produk
st.header("Kategori Produk")

# Kategori dengan penjualan paling banyak
st.subheader("Visualisasai ini menunjukkan kategori dengan penjulan tertinggi")
st.markdown("These are the top 10 product categories with the highest sales.")
top_10_categories = product_category_sales.nlargest(10, 'qty_sold').set_index('product_category_name')
st.bar_chart(top_10_categories['qty_sold'], use_container_width=True)

# Kategori dengan penjualan paling sediki
st.subheader("Visualisasai ini menunjukkan kategori dengan penjualan paling sedikit")
st.markdown("Inilah 10 kategori produk dengan penjualan terendah.")
bottom_10_categories = product_category_sales.nsmallest(10, 'qty_sold').set_index('product_category_name')
st.bar_chart(bottom_10_categories['qty_sold'], use_container_width=True)

