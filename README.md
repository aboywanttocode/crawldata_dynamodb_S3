# Tiki Hybrid Crawler 🕷️☁️

**Tiki Hybrid Crawler** là công cụ thu thập dữ liệu sản phẩm quy mô lớn (200.000+ IDs). Dự án sử dụng kiến trúc **Hybrid (Lai)**: Máy cá nhân chạy Crawler để vượt tường lửa, kết hợp AWS DynamoDB để lưu trữ dữ liệu an toàn.

##  Tính năng
- **Bypass Anti-bot:** Dùng `curl_cffi` giả lập Chrome thật để không bị chặn IP.
- **Batch Processing:** Tự động xử lý hàng loạt file từ `batch_001.csv` đến `batch_200.csv`.
- **Cloud Storage:** Lưu trực tiếp lên **AWS DynamoDB**.
- **Auto Retry:** Cơ chế tự động thử lại khi lỗi mạng hoặc gặp Rate Limit (429).

##  Cài đặt

1.  **Clone dự án:**
    ```bash
    git clone [https://github.com/username-cua-ban/tiki-hybrid-crawler.git](https://github.com/username-cua-ban/tiki-hybrid-crawler.git)
    cd tiki-hybrid-crawler
    ```

2.  **Cài đặt thư viện:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Cấu hình AWS:**
    Chạy lệnh sau và nhập Access Key/Secret Key của bạn:
    ```bash
    aws configure
    ```

4.  **Chuẩn bị dữ liệu:**
    Tạo thư mục `batches/` và đưa các file CSV vào (định dạng `batch_001.csv`, `batch_002.csv`...).

##  Chạy chương trình

```bash
python fetch.py
