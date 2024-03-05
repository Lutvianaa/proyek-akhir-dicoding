import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv("day_df_cleaned.csv")
hour_df = pd.read_csv("hour_df_cleaned.csv")


with st.sidebar:
    st.header("DASHBOARD")
    # Menambahkan logo
    st.image("https://cdn.pixabay.com/photo/2022/04/15/12/19/bike-7134325_1280.png")


st.title("Bike Sharing Dashboard")
st.markdown(
    """
    The following is a dashboard regarding bicycle borrowing from 1/1/2011 to 12/31/2012
    """
)
st.header("Distribution of Casual and Registered Users Based on Time")

# Line plot for comparison of average Casual and Registered users by hour
average_per_hour = hour_df.groupby('hr').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(x='hr', y='casual', data=average_per_hour, label='Casual', color='blue')
sns.lineplot(x='hr', y='registered', data=average_per_hour, label='Registered', color='orange')

# Menambahkan judul dan label sumbu
plt.title('Perbandingan Rata-rata Pengguna Casual dan Registered Berdasarkan Waktu')
plt.xlabel('Jam (Hour of the Day)')
plt.ylabel('Rata-rata Pengguna')

# Menampilkan legenda untuk membedakan antara Casual dan Registered
plt.legend()

# Menampilkan grafik
st.pyplot(plt.gcf())

with st.expander("Count of Bike Sharing"):
    tab1, tab2, tab3 = st.tabs(["By Weather", "By Season", "By Working Day"])
    
    with tab1:
        # Mapping antara nilai weathersit dan label yang lebih deskriptif
        weathersit_labels = {
            1: 'Clear/Few clouds',
            2: 'Mist/Cloudy',
            3: 'Light Snow/Rain',
            4: 'Heavy Rain/Ice Pallets'
        }

        # Mengganti nilai 'weathersit' dengan label yang lebih deskriptif
        day_df['weathersit_label'] = day_df['weathersit'].map(weathersit_labels)

        # Mengelompokkan berdasarkan kolom weathersit
        grouped_data = day_df.groupby(by="weathersit_label")["cnt"].sum().reset_index()

        # Mengurutkan data secara descending
        sorted_data = grouped_data.sort_values(by="cnt", ascending=False)

        # Membuat sebuah bar chart
        plt.figure(figsize=(10, 6))
        colors = sns.color_palette("viridis", len(sorted_data))
        sns.barplot(x='weathersit_label', y='cnt', data=sorted_data, palette=colors)

        # Menyesuaikan rotasi label di sumbu x
        plt.xticks(rotation=45, ha='right')
        plt.title('Total Peminjaman Sepeda Berdasarkan Weathersit')
        plt.xlabel('Weathersit')
        plt.ylabel('Total Peminjaman Sepeda')

        # Format sumbu y sebagai bilangan bulat
        plt.gca().get_yaxis().set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))

        # Menampilkan grafik
        st.pyplot(plt.gcf())
    
    with tab2:
        # Aggregate data by season
        seasonal_data = hour_df.groupby('season').agg({'cnt': ['mean', 'median', 'sum']}).reset_index()

        # Visualize the results
        plt.figure(figsize=(10, 6))
        sns.barplot(x='season', y=('cnt', 'mean'), data=seasonal_data)
        plt.title('Average Bike Rentals by Season')
        plt.xlabel('Season')
        plt.ylabel('Average Bike Rentals')

        # Menampilkan grafik
        st.pyplot(plt.gcf())

    with tab3:
        # Aggregate data by workingday
        workingday_data = hour_df.groupby('workingday').agg({'cnt': ['mean', 'median', 'sum']}).reset_index()

        # Visualize the results
        plt.figure(figsize=(10, 6))
        sns.barplot(x='workingday', y=('cnt', 'mean'), data=workingday_data)
        plt.title('Average Bike Rentals by Working Day')
        plt.xlabel('Working Day (1: Yes, 0: No)')
        plt.ylabel('Average Bike Rentals')

        # Menampilkan grafik
        st.pyplot(plt.gcf())


with st.expander("Conclusion"):
    st.write(
        '''
        1. Hasil menunjukkan bahwa faktor cuaca memengaruhi peminjaman sepeda. Semakin cerah/baik cuaca maka semakin banyak peminjaman sepeda, pun sebaliknya semakin buruk cuacanya maka semakin sedikit peminjaman sepeda.
        2. Distribusi peminjaman sepeda berdasarkan waktu menunjukkan bahwa pengguna Casual cenderung aktif pada jam tengah hari dengan jumlah peminjaman yang bervariasi, sedangkan pengguna Registered memiliki dua puncak aktivitas pada pagi dan sore hari, dengan jumlah peminjaman yang lebih stabil dan umumnya lebih tinggi daripada pengguna Casual.
        3. Musim panas memiliki frekuensi peminjaman sepeda tertinggi dan waktu antar peminjaman yang paling singkat.
        4. Peminjaman sepeda lebih tinggi pada hari kerja dibandingkan hari libur. Waktu antar peminjaman pada hari kerja dan hari libur relatif singkat.
        '''
    )