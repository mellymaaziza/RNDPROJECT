import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import base64

# --- CONFIG ---
st.set_page_config(page_title="E-Bike Market Intelligence", page_icon="⚡", layout="wide")

# --- DATABASE USER (MULTI-USER) ---
# Kamu bisa tambah user di sini sesuai kebutuhan
USER_DB = {
    "admin": {"pw": "ebike2026", "role": "Full Access"},
    "research": {"pw": "ebike_data", "role": "Data Analyst"},
    "marketing": {"pw": "ebike_smart", "role": "Marketing"}
}

# --- FUNGSI UNTUK MERENDER GAMBAR LOKAL KE BACKGROUND ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- LOAD ASSETS (BACKGROUND & LOGO) ---
path_foto = os.path.join("assets", "Foto Sepeda Listrik.webp") 
bin_str = get_base64_of_bin_file(path_foto)

path_logo = os.path.join("assets", "logo.png") 
logo_str = get_base64_of_bin_file(path_logo)

# --- SISTEM LOGIN REVISI (AESTHETIC & RAPIH) ---
def login_page():
    # CSS KHUSUS LOGIN (Glassmorphism Effect)
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8)), 
                        url("data:image/webp;base64,{bin_str if bin_str else ""}");
            background-size: cover !important;
            background-position: center !important;
        }}
        /* Container utama login biar gak melayang gak jelas */
        .login-box {{
            background: transparent;            /* Jadi transparan total */
            backdrop-filter: none;              /* Efek buram hilang */
            padding: 40px;
            border: none;                       /* Garis pinggir hilang */
            box-shadow: none;                   /* Bayangan hilang */
        }}
        .login-title {{
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 52px;
            text-align: center;
            margin-bottom: 5px; /* Kurangi margin bawah agar dekat dengan tulisan R&D */
            
            /* EFEK GRADASI TEKS */
            background: linear-gradient(to bottom, #ffffff 40%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
            /* EFEK CAHAYA (GLOW) */
            filter: drop-shadow(0px 0px 10px rgba(96, 165, 250, 0.5));
            text-transform: uppercase;
            letter-spacing: -1px;
        }}
        /* Menghilangkan border default streamlit di tabs */
        .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 10px 20px;
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # PENGGUNAAN TABS UNTUK HOME, LOGIN, ABOUT
        tab_login, tab_home, tab_about = st.tabs(["ACCESS SYSTEM", "HOME", "ABOUT"])
        
        with tab_login:
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            st.markdown("<div class='login-title'>E-BIKE MARKET RESEARCH</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#ffffff; font-family:\"Poppins\", sans-serif; font-style:normal; font-size:15px; margin-top:-10px; margin-bottom:35px; font-weight:500; letter-spacing:4px; text-shadow: 0px 0px 15px rgba(255,255,255,0.6), 2px 2px 10px rgba(0,0,0,1); text-transform:uppercase;'>by Research & Development</p>", unsafe_allow_html=True)
            user = st.text_input("Username", placeholder="Masukkan ID Anda...")
            pw = st.text_input("Password", type="password", placeholder="••••••••")
            
            # FITUR LUPA PASSWORD (Sederhana via Pop-up)
            with st.expander("Forgot Password?"):
                st.info("Silakan hubungi R&D Departement Hub atau Admin IT untuk reset password Anda.")
            
            if st.button("AUTHENTICATE", use_container_width=True, type="primary"):
                if user in USER_DB and USER_DB[user]["pw"] == pw:
                    st.session_state["logged_in"] = True
                    st.session_state["user_now"] = user
                    st.session_state["role_now"] = USER_DB[user]["role"]
                    st.success(f"Selamat Datang {user.capitalize()}! Mengalihkan...")
                    st.rerun()
                else:
                    st.error("Credential tidak valid. Coba lagi!")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_home:
            st.markdown("""
                <div class='login-box'>
                    <h3 style='color:white;'>Selamat Datang di Website Ar En Dy</h3>
                    <p style='color:#ccc;'>Sistem ini dirancang untuk memantau pergerakan pasar e-bike secara real-time. 
                    Gunakan akun resmi Anda untuk mengakses visualisasi data dan laporan penjualan.</p>
                    <ul style='color:#60a5fa;'>
                        <li>Monitoring Revenue 30 Hari</li>
                        <li>Analisis Segmen Produk</li>
                        <li>Pemantauan Kompetitor</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with tab_about:
            st.markdown("""
                <div class='login-box'>
                    <h3 style='color:white;'>R&D Departement Mantuls</h3>
                    <p style='color:#ccc;'>Versi Dashboard: v2.4.0 (Update 2026)<br>
                    Sistem ini mengintegrasikan data dari berbagai marketplace untuk memberikan gambaran pasar yang akurat.</p>
                </div>
            """, unsafe_allow_html=True)

# Inisialisasi status login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Cek apakah sudah login atau belum
if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# --- CSS REVISI UNTUK DASHBOARD UTAMA ---
bg_style = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("data:image/webp;base64,{bin_str if bin_str else ""}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    /* --- FITUR BARU: LOGOUT DI KANAN ATAS --- */
    .stButton > button[key="logout_top"] {{
        position: fixed;
        top: 15px;
        right: 80px;
        z-index: 999999;
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        padding: 5px 20px !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: 0.3s;
    }}

    /* --- FITUR BARU: USER STATUS DI KIRI BAWAH --- */
    .user-status-fixed {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 999999;
        background: rgba(15, 23, 42, 0.7);
        padding: 12px 18px;
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        line-height: 1.5;
    }}
    .main-title {{
        font-family: 'Inter', sans-serif !important;
        font-size: 75px !important; 
        font-weight: 900 !important;
        text-align: center !important;
        margin: 40px 0px 60px 0px !important;
        background: linear-gradient(to bottom, #ffffff 40%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap !important;
        letter-spacing: -1px !important; 
        text-transform: uppercase;
        line-height: 1.1 !important;
        filter: drop-shadow(0px 15px 25px rgba(0,0,0,0.6));
    }}

    .sidebar-header-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 30px !important;
    }}

    .sidebar-logo {{
        width: 100px;
        height: auto;
        filter: drop-shadow(0px 0px 10px rgba(96, 165, 250, 0.5));
    }}

    .sidebar-title {{
        font-family: 'Inter', sans-serif !important;
        font-size: 38px !important; 
        font-weight: 900 !important;
        line-height: 0.95 !important;
        letter-spacing: -1.5px !important;
        background: linear-gradient(to bottom, #ffffff 30%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 5px 15px rgba(96, 165, 250, 0.3));
        text-transform: uppercase;
        margin-left: 20px !important;
        margin-top: 0 !important;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(15, 23, 42, 0.92) !important;
        padding: 15px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(96, 165, 250, 0.25) !important;
    }}
    
    .section-header {{ 
        font-size: 24px; color: #ffffff; font-weight: 700; 
        margin-top: 35px; margin-bottom: 20px;
        background: rgba(96, 165, 250, 0.2);
        border-left: 6px solid #60a5fa; padding: 10px 20px;
        border-radius: 0 10px 10px 0;
        text-transform: uppercase;
    }}

    .podium-base {{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        padding: 20px 10px;
        border-radius: 15px 15px 0 0;
        position: relative;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .rank-1-base {{ height: 320px; background: linear-gradient(180deg, rgba(255, 215, 0, 0.3) 0%, rgba(255, 215, 0, 0.1) 100%); border: 2px solid #ffd700; }}
    .rank-2-base {{ height: 240px; background: rgba(192, 192, 192, 0.15); border: 1.5px solid #c0c0c0; }}
    .rank-3-base {{ height: 200px; background: rgba(205, 127, 50, 0.15); border: 1.5px solid #cd7f32; }}
    .rank-4-base {{ height: 160px; background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.4); }}
    .rank-5-base {{ height: 140px; background: rgba(96, 165, 250, 0.1); border: 1px solid rgba(96, 165, 250, 0.4); }}

    .badge-label {{
        width: 45px;
        height: 45px;
        background: #333;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}

    .gallery-card {{
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 0 0 10px 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
        margin-bottom: 10px;
        width: 100%;
    }}
</style>
"""
st.markdown(bg_style, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
@st.cache_data(show_spinner=False)
def load_image_url(url):
    try:
        if not isinstance(url, str) or not url.startswith("http"): return None
        response = requests.get(url.strip(), headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        return response.content if response.status_code == 200 else None
    except: return None

def clean_num(val):
    if pd.isna(val) or val == 0: return 0.0
    if isinstance(val, str):
        clean = val.replace('Rp', '').replace('.', '').replace(',', '').strip()
        try: return float(clean)
        except: return 0.0
    return float(val)

@st.cache_data
def load_data(category):
    if category == "Sepeda Listrik":
        filenames = ["sepeda listrik.csv", "Sepeda Listrik.csv", os.path.join("data", "sepeda listrik.csv")]
    elif category == "Sepeda Lipat":
        filenames = ["sepeda lipat.csv", "Sepeda Lipat.csv", os.path.join("data", "sepeda lipat.csv")]
    elif category == "Sepeda Listrik Lipat":
        filenames = ["Sepeda listrik lipat.csv", os.path.join("data", "Sepeda listrik lipat.csv")]
    else: return pd.DataFrame()
    
    df = pd.DataFrame()
    for f in filenames:
        if os.path.exists(f):
            df = pd.read_csv(f)
            break
    
    if df.empty: return df
    df.columns = [c.strip() for c in df.columns]
    
    col_map = {
        'Harga': ['Harga', 'price', 'Price'], 
        'Omset': ['Omset 30 Hari', 'Revenue', 'Omset'], 
        'Sold': ['Penjualan 30 Hari', 'Terjual', 'Sold', 'Penjualan Total'], 
        'Rating': ['Rating', 'Stars']
    }
    
    for key, variants in col_map.items():
        found = next((v for v in variants if v in df.columns), None)
        df[f'{key}_Clean'] = df[found].apply(clean_num) if found else 0.0
    
    df['Category_Label'] = category
    df['Segment'] = pd.cut(df['Harga_Clean'], 3, labels=['Entry', 'Mid', 'Premium'])
    return df

# --- SIDEBAR & CONTENT ---
with st.sidebar:
    logo_html = f'<img src="data:image/png;base64,{logo_str}" class="sidebar-logo">' if logo_str else ""
    st.markdown(f"""
        <div class="sidebar-header-container">
            {logo_html}
            <div class="sidebar-title">MARKET<br>FILTER</div>
        </div>
    """, unsafe_allow_html=True)

    # Info User Login di Sidebar
    st.info(f"👤 User: {st.session_state['user_now']}\n\n🛡️ Role: {st.session_state['role_now']}")

    category_choice = st.selectbox("Pilih Kategori", ["Best Product All", "Sepeda Listrik", "Sepeda Lipat", "Sepeda Listrik Lipat"])
    
    if category_choice == "Best Product All":
        df1 = load_data("Sepeda Listrik")
        df2 = load_data("Sepeda Lipat")
        df3 = load_data("Sepeda Listrik Lipat")
        df = pd.concat([df1, df2, df3], ignore_index=True)
    else:
        df = load_data(category_choice)

    if not df.empty:
        all_segments = df['Segment'].unique().tolist()
        selected_segments = st.multiselect("Pilih Segmen Harga", all_segments, default=all_segments)
        toko_col = 'Nama Toko' if 'Nama Toko' in df.columns else df.columns[1]
        selected_shops = st.multiselect("Pilih Toko", sorted(df[toko_col].unique().astype(str)))
        min_p, max_p = int(df['Harga_Clean'].min()), int(df['Harga_Clean'].max())
        price_range = st.slider("Rentang Harga (Rp)", min_p, max_p, (min_p, max_p))
        min_rating = st.slider("Minimal Rating ⭐", 0.0, 5.0, 4.0, 0.5)

# --- LANJUTAN MAIN PAGE ---
if df.empty:
    st.error(f"❌ Data tidak ditemukan!")
else:
    mask = (df['Harga_Clean'].between(price_range[0], price_range[1])) & \
            (df['Rating_Clean'] >= min_rating) & \
            (df['Segment'].isin(selected_segments))
    if selected_shops: mask = mask & (df[toko_col].isin(selected_shops))
    df_filtered = df[mask].copy()

    if category_choice == "Best Product All":
        st.markdown("<div class='main-title'>🏆 BEST PRODUCT ALL CATEGORIES</div>", unsafe_allow_html=True)
        top_5 = df_filtered.nlargest(5, 'Sold_Clean')
        col_img = next((c for c in ['Gambar Produk', 'Gambar', 'Image'] if c in top_5.columns), None)
        
        order_indices = [1, 0, 2, 3, 4] 
        podium_cols = st.columns([1, 1.2, 1, 0.9, 0.8])
        
        ranks_config = {
            0: {"color": "#FFD700", "class": "rank-1-base", "label": "1st"},
            1: {"color": "#C0C0C0", "class": "rank-2-base", "label": "2nd"},
            2: {"color": "#CD7F32", "class": "rank-3-base", "label": "3rd"},
            3: {"color": "#60a5fa", "class": "rank-4-base", "label": "4th"},
            4: {"color": "#60a5fa", "class": "rank-5-base", "label": "5th"}
        }

        for i, idx in enumerate(order_indices):
            if idx < len(top_5):
                item = top_5.iloc[idx]
                cfg = ranks_config[idx]
                with podium_cols[i]:
                    if col_img:
                        img_data = load_image_url(item[col_img])
                        if img_data: st.image(img_data, use_container_width=True)
                    
                    st.markdown(f"""
                        <div class="gallery-card">
                            <p style='font-size:11px; font-weight:bold; color:white; margin:0;'>{str(item.iloc[0])[:35]}...</p>
                            <p style='font-size:9px; color:#60a5fa; margin:0;'>{item['Category_Label']}</p>
                        </div>
                        <div class="podium-base {cfg['class']}">
                            <div class="badge-label" style="border: 3px solid {cfg['color']}; color:{cfg['color']};">{cfg['label']}</div>
                            <h3 style='color:white; margin:0; font-size:18px;'>Rp {item['Harga_Clean']:,.0f}</h3>
                            <p style='font-size:12px; color:#ccc;'>Sold: {int(item['Sold_Clean'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>📈 Comparison Data Top 5</div>", unsafe_allow_html=True)
        st.dataframe(top_5[['Nama Produk', 'Category_Label', 'Harga_Clean', 'Sold_Clean', 'Rating_Clean']], use_container_width=True)

    else:
        st.markdown(f"<div class='main-title'>⚡ {category_choice.upper()} MARKET INTELLIGENCE</div>", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Revenue", f"Rp {df_filtered['Omset_Clean'].sum():,.0f}")
        m2.metric("Units Sold", f"{int(df_filtered['Sold_Clean'].sum()):,} Pcs")
        m3.metric("Avg. Price", f"Rp {df_filtered['Harga_Clean'].mean():,.0f}")
        m4.metric("Active Listings", len(df_filtered))

        st.markdown("<div class='section-header'>📊 Market Overview</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            if not df_filtered.empty:
                df_filtered['Price_Range'] = pd.cut(df_filtered['Harga_Clean'], bins=5)
                df_filtered['Price_Range_Label'] = df_filtered['Price_Range'].apply(lambda x: f"Rp {x.left/1e6:.1f}jt - {x.right/1e6:.1f}jt")
                range_analysis = df_filtered.groupby(['Price_Range', 'Price_Range_Label'], observed=True)['Sold_Clean'].sum().reset_index().sort_values('Price_Range')
                fig_range = px.bar(range_analysis, x='Price_Range_Label', y='Sold_Clean', color='Sold_Clean', template="plotly_dark", color_continuous_scale="Blues", title="Unit Terjual Berdasarkan Rentang Harga")
                fig_range.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_range, use_container_width=True)

        with c2:
            fig_pie = px.pie(df_filtered, names='Segment', hole=0.5, template="plotly_dark", title="Distribusi Segmen")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("<div class='section-header'>💰 Revenue Analysis</div>", unsafe_allow_html=True)
        rev_c1, rev_c2 = st.columns([1, 1.5])
        
        with rev_c1:
            seg_rev = df_filtered.groupby('Segment', observed=True)['Omset_Clean'].sum().reset_index()
            fig_seg_rev = px.bar(
                seg_rev, x='Segment', y='Omset_Clean', 
                color='Segment', title="Revenue per Segmen (Vertical)",
                labels={'Omset_Clean': 'Total Revenue (Rp)'},
                template="plotly_dark",
                color_discrete_map={"Entry": "#60a5fa", "Mid": "#fbbf24", "Premium": "#f87171"}
            )
            fig_seg_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_seg_rev, use_container_width=True)

        with rev_c2:
            store_rev = df_filtered.groupby(toko_col)['Omset_Clean'].sum().nlargest(10).reset_index()
            fig_store_rev = px.bar(
                store_rev, x='Omset_Clean', y=toko_col, 
                orientation='h', title="Top 10 Stores by Revenue (Horizontal)",
                labels={'Omset_Clean': 'Total Revenue (Rp)', toko_col: 'Nama Toko'},
                template="plotly_dark", color='Omset_Clean', color_continuous_scale="Viridis"
            )
            fig_store_rev.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_store_rev, use_container_width=True)

        st.markdown("<div class='section-header'>🏆 Top Sellers Gallery</div>", unsafe_allow_html=True)
        top_10 = df_filtered.nlargest(10, 'Sold_Clean')
        rows = st.columns(5)
        col_img = next((c for c in ['Gambar Produk', 'Gambar', 'Image'] if c in top_10.columns), None)
        col_link = next((c for c in ['Link Produk', 'Url', 'Link'] if c in top_10.columns), None)
        
        for i, (_, item) in enumerate(top_10.iterrows()):
            with rows[i % 5]:
                if col_img:
                    img_data = load_image_url(item[col_img])
                    if img_data: st.image(img_data, use_container_width=True)
                st.markdown(f'<div class="gallery-card"><p style="font-size:12px; font-weight:bold; color:#ddd; height:40px; overflow:hidden;">{str(item.iloc[0])[:50]}...</p><h4 style="color:#60a5fa; margin:0;">Rp {item["Harga_Clean"]:,.0f}</h4><p style="font-size:11px; color:#999;">Terjual: {int(item["Sold_Clean"])}</p></div>', unsafe_allow_html=True)
                if col_link and pd.notna(item[col_link]):
                    st.link_button("🛒 Open Product", item[col_link], use_container_width=True)

    # --- FITUR LOGOUT & EXPORT ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚙️ SYSTEM CONTROL</div>", unsafe_allow_html=True)
    
    ctrl_col1, ctrl_col2 = st.columns(2)
    
    with ctrl_col1:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DOWNLOAD CURRENT REPORT (CSV)",
            data=csv_data,
            file_name=f"report_{category_choice.lower()}.csv",
            mime='text/csv',
            use_container_width=True
        )

    with ctrl_col2:
        if st.button("🚪 TERMINATE SESSION & LOG OUT", use_container_width=True, type="secondary"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.markdown("<br><hr><center style='color:white; opacity:0.5;'>Dashboard by R&D Departement Hub © 2026</center>", unsafe_allow_html=True)
