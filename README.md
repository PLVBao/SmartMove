# SmartMove - SmartMovers Management System

## 1. Giới thiệu

SmartMove là ứng dụng quản lý hoạt động vận chuyển hàng hóa, được xây dựng bằng Python Streamlit và MySQL. Hệ thống hỗ trợ quản lý khách hàng, sản phẩm, job vận chuyển, load, container, transport unit và báo cáo chi phí vận chuyển.

## 2. Công nghệ sử dụng

- Python
- Streamlit
- MySQL
- PyMySQL
- Pandas

## 3. Cấu trúc thư mục

SmartMove/  
├─ source/  
│  ├─ main.py  
│  ├─ db.py  
│  └─ Smartmove.sql  
└─ README.md  

## 4. Chức năng chính

- Hiển thị dashboard tổng quan dữ liệu  
- Xem danh sách dữ liệu trong các bảng  
- Thêm dữ liệu cho Customer, Product, Job và Load  
- Xem báo cáo chi phí vận chuyển theo từng job  
- Xem thông tin giá theo loại khách hàng, loại sản phẩm và kích thước load  
- Xem phân công job, transport unit, workload theo depot và thống kê load theo khách hàng  

## 5. Cài đặt và chạy chương trình

### Bước 1: Cài đặt thư viện
pip install streamlit pymysql pandas  

### Bước 2: Import cơ sở dữ liệu
Import file: source/Smartmove.sql  
Database: smartmovers_db  

### Bước 3: Kiểm tra kết nối database
Mở file source/db.py và chỉnh:

DB_CONFIG = {  
    "host": "localhost",  
    "user": "root",  
    "password": "",  
    "database": "smartmovers_db",  
    "port": 3306  
}  

### Bước 4: Chạy chương trình
cd source  
streamlit run main.py  


## 6. Ghi chú

- Cần bật MySQL trước khi chạy  
- Import SQL trước khi sử dụng  
- Nếu lỗi kết nối, kiểm tra lại thông tin trong db.py  
- main.py là file chạy chính  
- db.py dùng để kết nối database  
- Smartmove.sql dùng để tạo dữ liệu  

## 7. Nhóm thực hiện

Nhóm 12 - Thiết kế cơ sở dữ liệu
