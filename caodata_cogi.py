#Import các thư viện cần thiết
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Định nghĩa hàm để lấy thông tin từ URL và lưu trực tiếp vào file CSV
def get_info_from_url_and_save(url, output_file):
    # Gửi HTTP GET request để tải nội dung của trang web
    response = requests.get(url)
    print(url)
    
    # Kiểm tra xem request có thành công hay không (status code 200 là thành công)
    if response.status_code == 200:
        # Sử dụng BeautifulSoup để phân tích nội dung HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        address = ""
        address_details = []
        street = ""
        ward = ""
        district = ""
        city = ""
        # Tìm thẻ <div> với class là "address"
        address_div = soup.find('div', class_='address')
        if address_div:
            address = address_div.get_text()
            address_details = [detail.strip() for detail in address.split(',')]
            address_details.reverse()

            for i in address_details:
                    text = i
                    if "Đường" in text or text == address_details[-1]:
                        street = text
                        
                    elif "Phường" in text or "Xã" in text:
                        ward = text
                        
                    elif "Quận" in text or "Huyện" in text or "Thành Phố" in text:
                        district = text
                        
                    elif "TP" in text:
                        city = text
                        
        # Tìm thẻ <div> với class là "product-short-info"
        price_info_div = soup.find('div', class_='price')

        # Khởi tạo các biến để lưu thông tin sản phẩm
        price = ""
        price = price_info_div.get_text()
                            
        # Tìm thẻ <div> với class là "product-attributes"
        attributes_div = soup.find('div', class_='info-attrs clearfix')

        # Khởi tạo một từ điển để lưu thông tin lọc ra
        attributes_info = {}

        # Kiểm tra xem thẻ attributes_div có tồn tại hay không
        if attributes_div:
            # Lặp qua các thẻ con bên trong thẻ attributes_div
            for item_div in attributes_div.find_all('div', class_='info-attr clearfix'):
                spans = item_div.find_all('span')

                # Kiểm tra xem có đúng 2 thẻ <span> trong mỗi item_div
                if len(spans) == 2:
                    key = spans[0].text.strip()
                    value = spans[1].text.strip()
                    attributes_info[key] = value

        # Trả về thông tin lấy được từ URL
        info = {
            'URL': url,
            'Địa chỉ': address,
            'Đường': street,
            'Phường/Xã': ward,
            'Quận/Huyện': district,
            'Thành Phố': city,
            'Giá': price,
            **attributes_info,
        }

        # Lưu thông tin vào file CSV
        info_df = pd.DataFrame([info])
        if not os.path.exists(output_file):
            info_df.to_csv(output_file, index=False)
        else:
            info_df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        print(f"Request failed for URL: {url}, Status Code: {response.status_code}")
    
    # Kiểm tra nếu timeout lớn hơn 5 giây thì bỏ qua URL
    if response.elapsed.total_seconds() > 5:
        print(f"Timeout > 5 seconds for URL: {url}, Skipping...")
        return None

    time.sleep(1)

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data_link.csv')

# Tạo một danh sách chứa thông tin từ các URL
info_list = []

# Kiểm tra xem tệp CSV đầu ra đã tồn tại chưa
output_file = 'end_cogi.csv'
output_file_exists = os.path.exists(output_file)

# Iterate through each URL and get information, then save it to the CSV file
for url in df['links']:
    get_info_from_url_and_save(url, output_file)
