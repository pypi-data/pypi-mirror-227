##  Thư viện license Mobio 


### Cài đặt:
```bash
 $ pip3 install mobio-license-sdk
 ```


### Sử dụng:

##### 1. Khởi tạo sdk:
   ```python
    from mobio.sdks.license import MobioLicenseSDK

    MobioLicenseSDK().config(
        admin_host="",	# admin host
        redis_uri="",	# redis uri
        module_use="",	# liên hệ admin để khai báo tên của module
        module_encrypt="",	# liên hệ admin để lấy mã
        license_key="", # key salt
    )
    
   ```

##### 2. Lấy thông tin license:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_json_license(
        merchant_id,
    )
    """
    {
      ...   # license info
      
    }
    """
   ```

##### 3. Lấy số lượng tài khoản tối đa:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_number_user(
        merchant_id,
    )
    """
    {
      "number": 12
    }
    """
   ```


##### 4. Lấy số lượng profile tối đa:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_number_profile(
        merchant_id,
    )
    """
    {
      "number": 50000 
    }
    """
   ```

##### 5. Lấy số lượng profile ẩn danh tối đa:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_number_profile_anonymous(
        merchant_id,
    )
    """
    {
      "number": 100000
    }
    """
   ```

##### 6. Lấy số lượng page social tối đa:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_number_page_social(
        merchant_id,
    )
    """
    {
      "number": 6 
    }
    """
   ```

##### 7. Lấy số lượng tin nhắn còn được gửi trong tháng:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_number_messages_allow_used(
        merchant_id,
        day_of_month=None # ngày kiểm tra YYYYmmdd (ITC), nếu None sdk tự động lấy ngày hiện tại  
    )
    """
    {
      "number": 1200,
      "messages": ""    # thông báo nếu có 
    }
    """
   ```

##### 8. Kiểm tra lượng tin nhắn cần sử dụng cho chiến dịch:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().use_message_for_campaign(
        merchant_id,
        number_of_message, # số mess cần sử dụng 
        day_of_month=None # ngày kiểm tra YYYYmmdd (ITC), nếu None sdk tự động lấy ngày hiện tại  
    )
    """
    {
      "number": 12,
        "messages": ""    # thông báo nếu có 
        "success": 1    # trạng thái sử dụng, 1: thành công, 0: thất bại. 
                        # nếu thành công dữ liệu số mess đã sử dụng sẽ lưu lại để tính toán cho lần tiếp theo.
    }
    """
   ```

##### 9. Hàm mã hóa và giải mã:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().decrypt1(
        key_salt, # key salt theo hàm mã hóa  
        data    # dữ liệu cần giải mã 
    )
    result = MobioLicenseSDK().encrypt2(
        data    # dữ liệu cần mã hóa  
    )
    result = MobioLicenseSDK().decrypt2(
        data    # dữ liệu cần giải mã 
    )
    # kết quả là kiểu string 
   ```

##### 10. Hàm kiểm tra merchant đã hết hạn chưa:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().merchant_has_expired(
        merchant_id 
    )
    # result = True : merchant đã hết hạn 
    # result = False : merchant chưa hết hạn 
   ```

#### Log - 1.0.1
    - tạo sdk 

#### Log - 1.0.2
    - init export class SDK 

#### Log - 1.0.3
    - thêm các hàm lấy thông số license 
    
#### Log - 1.0.4
    - thay đổi requirements  

#### Log - 1.0.5
    - sửa import sai   

#### Log - 1.0.6
    - thêm cơ chế cache file license, tự động tải mới file sau 1 khoảng thời gian    

#### Log - 1.0.7
    - export các hàm mã hóa và giải mã    

#### Log - 1.0.8
    - Hàm kiểm tra merchant đã hết hạn chưa     

#### Log - 1.0.9
    - sửa lỗi lấy cache thông tin license  

#### Log - 1.0.10
    - nâng cấp version run cho python 3.8   

#### Log - 1.0.11
    - từ merchant truyền vào tìm merchant root để thực hiện các nghiệp vụ lấy thông tin license    

#### Log - 1.0.12
    - build wheels   
    
    
     
    