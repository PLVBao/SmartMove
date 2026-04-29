SmartMove - SmartMovers Management System
1. Giới thiệu

SmartMove là ứng dụng quản lý hoạt động vận chuyển hàng hóa, được xây dựng bằng Python Streamlit và MySQL.
Hệ thống hỗ trợ quản lý khách hàng, sản phẩm, công việc vận chuyển, kiện hàng, đơn vị vận chuyển và báo cáo chi phí theo từng job.

2. Công nghệ sử dụng
Python
Streamlit
MySQL
PyMySQL
Pandas
3. Cấu trúc thư mục

SmartMove/
├─ source/
│ ├─ main.py
│ ├─ db.py
│ └─ Smartmove.sql
└─ README.md

4. Chức năng chính
Dashboard tổng quan số lượng Customer, Depot, Product, Job, Load, Transport Unit và Container.
Thêm dữ liệu cho Customer, Product, Job và Load.
Xem danh sách dữ liệu trong các bảng.
Xem báo cáo chi phí vận chuyển theo từng job.
Xem chi tiết giá theo loại khách hàng, loại sản phẩm và kích thước load.
Xem phân công job, phân bổ transport unit, workload theo depot và thống kê load theo khách hàng.

6. Cách cài đặt và chạy
Bước 1: Cài thư viện
pip install streamlit pymysql pandas

Bước 2: Import database
Import file: source/Smartmove.sql
Database: smartmovers_db

Bước 3: Kiểm tra kết nối
Mở file source/db.py và chỉnh:
DB_CONFIG = {
"host": "localhost",
"user": "root",
"password": "",
"database": "smartmovers_db",
"port": 3306
}

Bước 4: Chạy chương trình
cd source
streamlit run main.py

6. Ghi chú
Cần bật MySQL trước khi chạy
Import SQL trước khi sử dụng
Nếu lỗi kết nối, kiểm tra lại thông tin trong db.py

8. Nhóm thực hiện
Nhóm 12 - Thiết kế cơ sở dữ liệu
