import streamlit as st
import pandas as pd
import numpy as np
import hydralit_components as hc
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="Visualisasi Data Kepadatan Penduduk Jawa Timur",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state='collapsed',
)
# -----------------------------------------------------------------------------------------------------------------------------------
st.set_option('deprecation.showPyplotGlobalUse', False)
menu_data = [
    {'icon': "fa fa-database", 'label':"Dataset"},
    {'id':'Data Filter','icon':'fa fa-database','label':"Data"},
    {'id':'subid12','icon': "📈", 'label':"Line Chart"},
    {'id':'subid11','icon': "📊", 'label':"Barchart"},
    # {'id':'subid13','icon': "💹", 'label':"Area Chart"},
    {'id':'Pie','icon': "◔", 'label':"Pie"},
    {'id':'plot','icon': "〰️", 'label':"Plot chart"},
    {'id':'hst','icon': "far fa-copy", 'label':"Histogram"},
    {'id':'map','icon': "🗺", 'label':"Map"},
    ]
over_theme = {'txc_inactive': 'black','menu_background':'lightblue','txc_active':'yellow','option_active':'black'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=True, 
    sticky_nav=True,
    sticky_mode='pinned', 
)
# -----------------------------------------------------------------------------------------------------------------------------------
df = pd.read_excel(
    io="Kepadatan Penduduk Jawa Timur.xlsx",
    engine='openpyxl',
)
# -----------------------------------------------------------------------------------------------------------------------------------
df.index = df.index + 1
df['jumlah_penduduk_per_m2'] = df['jumlah_penduduk_per_m2'].astype(int)
df['Semester'] = df['Semester'].astype(str)
df['periode_update'] = df['periode_update'].astype(int)
df.replace('-', np.nan, inplace=True)
x = df.rename(columns={'Kabupaten_kota':'Kabupaten/Kota','jumlah_penduduk_per_m2':'Jumlah Penduduk','Semester':'Periode','periode_update':'Update'})
# -----------------------------------------------------------------------------------------------------------------------------------
st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(20, 205, 200, 1);
   border: 1px solid rgba(242, 39, 19, 1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(224,255,255);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   font-size: large;
   font
   color: red;
}
</style>
"""
, unsafe_allow_html=True)
# -----------------------------------------------------------------------------------------------------------------------------------
if menu_id == 'Home':
    st.write("""# Visualisasi Data Kepadatan Penduduk Jawa Timur dengan Streamlit""")
    st.write("# Aplikasi ini dikembangkan untuk melakukan visualisasi data kepadatan penduduk di Jawa Timur menggunakan Streamlit, sebuah framework Python untuk membuat aplikasi web interaktif dengan mudah. Aplikasi ini memanfaatkan beberapa library tambahan seperti Pandas, NumPy, Hydralit Components, Altair, dan Plotly Express untuk analisis dan visualisasi data. ")
# -----------------------------------------------------------------------------------------------------------------------------------
if menu_id == 'Dataset':
    st.write("""## Dataset Keseluruhan""") 
    st.write(x.shape)
    st.dataframe(x, width=1500)
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'Data Filter':
    st.write("""## Filtering Berdasarkan Kabupaten/Kota""") 
    X2018,X2019,X2020,X2021,X2022 = st.columns(5)
    a= x.query("Update == 2018")
    b= x.query("Update == 2019")
    c= x.query("Update == 2020")
    d= x.query("Update == 2021")
    e= x.query("Update == 2022")

    X2018.metric("2018", a['Jumlah Penduduk'].sum())
    X2019.metric("2019", b['Jumlah Penduduk'].sum())
    X2020.metric("2020", c['Jumlah Penduduk'].sum())
    X2021.metric("2021", d['Jumlah Penduduk'].sum())
    X2022.metric("2022", e['Jumlah Penduduk'].sum())
    st.markdown("----")
    st.write("""## Filter data berdasarkan Kabupaten/Kota""") 
    ag = x['kabupaten_kota'].unique()
    data = st.selectbox(
        "Pilih Kabupaten/Kota", ag
        )
    daerah = x.query(
        "kabupaten_kota == @data"
        )
    st.dataframe(daerah.style.format(precision=2), width=1500)
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'subid11':
    st.write("""## Bar Charts""") 
    ag = x['kabupaten_kota'].unique()
    data = st.selectbox(
        "Pilih Kabupaten/Kota", ag
        )
    daerah = x.query(
        "kabupaten_kota == @data"
        )
    alt.Chart(daerah).mark_bar().encode(
    x="Update:N",
    y="sum(Jumlah Penduduk)",
    color="kabupaten_kota:N",
    row='Periode:N',
    ).properties(height=300),
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'subid12':
    st.write("""## Line Charts""") 
    alt.Chart(x).mark_line().encode(
    x="kabupaten_kota:N",
    y="Jumlah Penduduk",
    color="Update:N",
    row='Periode:N',
    ).properties(height=300),
# -----------------------------------------------------------------------------------------------------------------------------------
# elif menu_id == 'subid13':
#     st.write("""## Area Charts""") 
#     alt.Chart(df).mark_area(opacity=0.3).encode(
#     x="kabupaten_kota",
#     y=alt.Y("count(Jumlah penduduk):Q", stack=None),
#     color="Update:N",
#     ).properties(height=300),
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'map':
    st.write("""## Map""") 
    m = pd.read_csv('jatim2.csv')
    mm = pd.read_excel(
        io="Kepadatan Penduduk Jawa Timur2.xlsx")
    ms = m.join(mm)
    mp = ms.query(
        "parent_nid == 15"
    )
    mp.rename(columns={'name':'Kabupaten/Kota'}, inplace=True)
    fig = px.scatter_mapbox(mp, lat="latitude", lon="longitude", color="Kabupaten/Kota", hover_data=[ "jumlah penduduk", "periode update"], width=1100, size_max=3)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(height=600, margin={"r":2,"t":2,"l":2,"b":2}, mapbox_zoom=8, mapbox_center = {"lat": -7.536064, "lon": 112.238403})
    st.plotly_chart(fig)
    
    # df = gp.read_file('jatim.geojson')
    # df = df.set_crs(epsg=3857, allow_override=True)
    # df = df.to_crs(epsg=4326)
    # df['lon'] = df.geometry  # extract longitude from geometry
    # df['lat'] = df.geometry  # extract latitude from geometry
    # df = df[['lon','lat']]     # only keep longitude and latitude
    # st.write(df)        # show on table for testing only
    # st.map(df)                 # show on map
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'Pie':
    st.write("""## Pie""")
    ag = x['kabupaten_kota'].unique()
    data = st.selectbox(
        "Pilih Kabupaten/Kota", ag
        )
    daerah = x.query(
        "kabupaten_kota == @data"
        )
    alt.Chart(daerah).mark_arc().encode(
        theta=alt.Theta(field="Jumlah Penduduk", type="quantitative"),
        color=alt.Color(field="Update", type="nominal"),
        column = alt.Row(field="Periode", type="nominal")
    ).properties(width=500, height=500),
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'plot':
    st.write("""## Plot chart Jumlah penduduk""")
    alt.Chart(x).mark_circle().encode(
    alt.X('kabupaten_kota', scale=alt.Scale(zero=False)),
    alt.Y('Jumlah Penduduk', scale=alt.Scale(zero=False, padding=1)),
    color=alt.Color(field="Update", type="nominal"),
    size='Jumlah Penduduk',
    ).properties(width=1000, height=300),
# -----------------------------------------------------------------------------------------------------------------------------------
elif menu_id == 'hst':
    st.write("""## Histogram""")
    alt.Chart(x).mark_bar().encode(
    alt.X('kabupaten_kota'),
    y='Jumlah Penduduk',
    color='Update',
    row='Periode'
    ).properties(width=1000, height=300),
# -----------------------------------------------------------------------------------------------------------------------------------
if menu_id == 'Logout':
    st.write("""# Sekian""")
    st.write("""# Terima kasih """)
    
#<<<------------------------------------------------ I S I ------------------------------------------------------>>>

# df = pd.read_excel(
#     io="Kepadatan Penduduk Jawa Timur.xlsx",
#     skiprows=0,
#     header=0,
#     index_col=0,
#     engine='openpyxl',
# )

# df['jumlah_penduduk_per_m2'] = df['jumlah_penduduk_per_m2'].astype(int)
# df['Semester'] = df['Semester'].astype(str)
# df['periode_update'] = df['periode_update'].astype(int)
# df.replace('-', np.nan, inplace=True)
# x = df.rename(columns={'jumlah_penduduk_per_m2':'Jumlah Penduduk','Semester':'Periode','periode_update':'Update'})

# option = st.sidebar.selectbox(
# 'Silakan pilih:',
# ('Home','Data frame','Data Visualitation')
# )
# if option == 'Home' or option == '':
#     st.write("# Tugas Ujian Akhir Semester") 
#     st.write("""## Visualisasi Data Kepadatan Penduduk Jawa Timur dengan Streamlit""")
#     st.write("""## kelompok : 6""")
#     st.write(""" Nama : M.Khotibul Umam  NIM : 09020620031 """)
#     st.write(""" Nama : Retno  NIM : 09020620032 """)
#     st.write(""" Nama : Fateh  NIM : 09020620033 """)    

# elif option == 'Data frame':
#     with st.spinner('Wait for it...') :
#         import time
#     time.sleep(3)
#     st.success('Berhasil !',icon="✅")
#     st.snow()
#     st.write("""## Data Frame""") 
#     # x['periode_update'] = pd.to_datetime(df['periode_update'])
#     # xx=df['jumlah_penduduk_per_m2'] = df['jumlah_penduduk_per_m2'].astype(int)
#     st.dataframe(x)
#     st.write("""## Filtering""") 
#     ag = x.index.unique()
#     data = st.selectbox(
#     "Pilih Kabupaten/Kota", ag 
#     )
#     pilihan = x.query(

#     "index == @data"
#     )
#     st.dataframe(pilihan.style.format(precision=2))
    
# elif option == 'Data Visualitation':
#     ag = x.index.unique()
#     data = st.selectbox(
#         "Pilih Kabupaten/Kota", ag
#         )
#     pilihan = x.query(

#         "index == @data"
#         )
    
#     f = ['1','2','3','4','5']
#     v = st.selectbox(
#         'pilih Visualisasi', f
#     )
#     if v == '1':
#         st.success('Berhasil Memilih Data!', icon="✅")
#         st.write("""## Bar Charts""") 
#         vc = pilihan.groupby('Update')['Jumlah Penduduk','Periode'].sum()
#         st.bar_chart(vc.style.format(precision=0))
#     elif v == '2':
#         st.success('Berhasil Memilih Data!', icon="✅")
#         st.write("""## Line Charts""") 
#         vc = pilihan.groupby('Update')['Jumlah Penduduk','Periode'].sum()
#         st.line_chart(vc.style.format(precision=0))
#     elif v == '3':
#         st.success('Berhasil Memilih Data!', icon="✅")
#         st.write("""## Area Charts""") 
#         vc = pilihan.groupby('Update')['Jumlah Penduduk','Periode'].sum()
#         st.area_chart(vc.style.format(precision=0))
#     elif v == '4':
#         st.success('Berhasil Memilih Data!', icon="✅")
#         st.write("""## Map""")
#         st.map(pilihan)        
#         st.write("""## Sek Bingung""")
#     elif v == '5':
#         st.success('Berhasil Memilih Data!', icon="✅")
#         st.write("""## Domongi sek bingung kok e""") 
