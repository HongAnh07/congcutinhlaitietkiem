import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write("Tính tiền lãi theo phương pháp lãi đơn hoặc lãi kép.")

# =========================
# NHẬP THÔNG TIN
# =========================

so_tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

hinh_thuc_lai = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 Tính tiền lãi", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r_nam = lai_suat / 100

    # Số tháng trong kỳ hạn
    so_thang = ky_han

    # Số kỳ nhận lãi và số tháng/kỳ
    if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
        so_ky = so_thang
        thang_moi_ky = 1

    elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
        so_ky = so_thang // 3

        if so_thang % 3 != 0:
            st.warning(
                "Kỳ hạn không chia hết cho 3 tháng. "
                "Phần tháng lẻ sẽ được tính riêng ở cuối kỳ."
            )

        thang_moi_ky = 3

    else:
        so_ky = 1
        thang_moi_ky = so_thang

    # =====================================================
    # LÃI ĐƠN
    # =====================================================

    if hinh_thuc_lai == "Lãi đơn":

        tong_lai = so_tien_gui * r_nam * (so_thang / 12)

        # Lãi định kỳ
        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            lai_dinh_ky = so_tien_gui * r_nam / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            lai_dinh_ky = so_tien_gui * r_nam / 4

        else:
            lai_dinh_ky = tong_lai

        tong_goc_lai = so_tien_gui + tong_lai

        # Tạo bảng chi tiết
        danh_sach = []

        for ky in range(1, so_ky + 1):

            if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
                lai_ky = so_tien_gui * r_nam / 12

            elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
                lai_ky = so_tien_gui * r_nam / 4

            else:
                lai_ky = tong_lai

            danh_sach.append({
                "Kỳ": ky,
                "Tiền gốc": so_tien_gui,
                "Tiền lãi kỳ này": lai_ky,
                "Tổng gốc + lãi": so_tien_gui + lai_ky
            })

    # =====================================================
    # LÃI KÉP
    # =====================================================

    else:

        danh_sach = []

        so_du = so_tien_gui
        tong_lai = 0

        # Lãi suất theo kỳ
        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            lai_suat_ky = r_nam / 12
            so_ky_thuc = so_thang

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            lai_suat_ky = r_nam / 4
            so_ky_thuc = so_thang // 3

        else:
            lai_suat_ky = r_nam * (so_thang / 12)
            so_ky_thuc = 1

        for ky in range(1, so_ky_thuc + 1):

            lai_ky = so_du * lai_suat_ky
            so_du = so_du + lai_ky
            tong_lai = so_du - so_tien_gui

            danh_sach.append({
                "Kỳ": ky,
                "Tiền gốc đầu kỳ": so_du - lai_ky,
                "Tiền lãi kỳ này": lai_ky,
                "Tổng gốc + lãi": so_du
            })

        tong_goc_lai = so_du

        if len(danh_sach) > 0:
            lai_dinh_ky = danh_sach[-1]["Tiền lãi kỳ này"]
        else:
            lai_dinh_ky = 0

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.divider()

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    with col3:
        st.metric(
            "Tổng gốc + lãi",
            dinh_dang_tien(tong_goc_lai)
        )

    # =========================
    # THÔNG TIN ĐẦU VÀO
    # =========================

    st.subheader("📋 Thông tin khoản gửi")

    st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Phương pháp:** {hinh_thuc_lai}")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")

    # =========================
    # BẢNG CHI TIẾT
    # =========================

    if danh_sach:

        st.subheader("📈 Chi tiết tiền lãi")

        df = pd.DataFrame(danh_sach)

        # Format tiền
        for cot in df.columns:
            if cot != "Kỳ":
                df[cot] = df[cot].apply(dinh_dang_tien)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================
# GHI CHÚ
# =========================

st.divider()

st.caption(
    "Lưu ý: Đây là công cụ mô phỏng cách tính lãi đơn và lãi kép. "
    "Lãi suất thực tế của ngân hàng có thể có cách tính, quy định "
    "và điều kiện khác."
)
