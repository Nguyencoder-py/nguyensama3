import os, time, sys
import requests
import random
try: 
    import numpy as np
    import cv2
except: 
    os.system("pip install cv2")
    os.system("pip install numpy")
    os.system("pip install opencv-python")
import numpy as np
import cv2

class ADB:
    def __init__(self, handle):
        self.handle = handle

    def screen_capture(self, name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")

    def click(self, x, y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")

    def find(self, img='', template_pic_name=False, threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle + '.png'
        else:
            self.screen_capture(template_pic_name)
        
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data


def wait_for_element(d, img, timeout=10):
    """
    Hàm chờ đợi phần tử xuất hiện trên màn hình trong một khoảng thời gian.
    :param d: đối tượng ADB
    :param img: tên ảnh cần tìm
    :param timeout: thời gian chờ tối đa (tính bằng giây)
    :return: true nếu tìm thấy, false nếu không tìm thấy
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        points = d.find(img)
        if points:
            return points
        time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
    return None  # Nếu không tìm thấy sau thời gian chờ


d = ADB('emulator-5566')

# Tìm nút "Thị trường"
point = wait_for_element(d, 'thitruong.png')
if point:
    print("Thị trường found at:", point)
    d.click(point[0][0], point[0][1])  # Click vào nút Thị trường
    time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
else:
    print("Thị trường not found!")

# Tìm nút "Theo dõi cầu thủ"
point_theo_doi = wait_for_element(d, 'theodoicauthu.png')
if point_theo_doi:
    print("Theo dõi cầu thủ found at:", point_theo_doi)
    d.click(point_theo_doi[0][0], point_theo_doi[0][1])  # Click vào nút Theo dõi cầu thủ
    time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
else:
    print("Theo dõi cầu thủ not found!")

# Tìm nút "Cầu thủ"
point_cau_thu = wait_for_element(d, 'cauthu1.png')
if point_cau_thu:
    print("Cầu thủ found at:", point_cau_thu)
    d.click(point_cau_thu[0][0], point_cau_thu[0][1])  # Click vào nút Cầu thủ
    time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
else:
    print("Cầu thủ not found!")

# Tìm nút "Mua cầu thủ"
point_mua_cau_thu = wait_for_element(d, 'mua.png')
if point_mua_cau_thu:
    print("Mua cầu thủ found at:", point_mua_cau_thu)
    d.click(point_mua_cau_thu[0][0], point_mua_cau_thu[0][1])  # Click vào nút Mua cầu thủ
    time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
else:
    print("Mua cầu thủ not found!")
# Tìm và nhấn nút cộng 5 lần
for i in range(9):
    point_plus = d.find('plus_button.png')
    if point_plus:
        print(f"Plus button found at: {point_plus}")
        d.click(point_plus[0][0], point_plus[0][1])
        time.sleep(0.1)  # Đợi 1 giây trước khi nhấn lại
    else:
        print("Plus button not found!")
# Tìm trường giá tiền và nhấn vào đó
point_price_field = d.find('price_field.png')
if point_price_field:
    print("Price field found at:", point_price_field)
    d.click(point_price_field[0][0], point_price_field[0][1])
    time.sleep(1)  # Đợi 1 giây để đảm bảo trường giá tiền đã sẵn sàng

    # Xóa tất cả giá tiền cũ (ấn và giữ Backspace 4 lần)
    for _ in range(4):  # Xóa 4 lần
        os.system("adb -s emulator-5566 shell input keyevent 67")  # 67 là keycode cho Backspace
        time.sleep(0.5)  # Đợi một chút giữa các lần nhấn Backspace

    # Nhập giá tiền mới là 446
    os.system("adb -s emulator-5566 shell input text 445")
    time.sleep(1)  # Đợi sau khi nhập xong

    # Ấn vào bất kỳ chỗ nào (chẳng hạn như ngoài vùng trường giá tiền)
    d.click(100, 100)  # Bạn có thể thay đổi tọa độ này
else:
    print("Price field not found!")
    time.sleep(2)
# Sau khi hoàn tất việc điều chỉnh giá tiền
if point_price_field:
    print("hoàn tất việc điều chỉnh giá tiền")

    # Tìm nút "Mua" và nhấn vào đó
    point_buy_button = wait_for_element(d, 'buy_button.png')
    if point_buy_button:
        print("Buy button found at:", point_buy_button)
        d.click(point_buy_button[0][0], point_buy_button[0][1])
        time.sleep(2)  # Đợi giao diện hiện nút "Xác nhận mua"
        
        # Tìm nút "Xác nhận mua" và nhấn vào đó
        point_confirm_button = wait_for_element(d, 'confirm_button.png')
        if point_confirm_button:
            print("Confirm button found at:", point_confirm_button)
            d.click(point_confirm_button[0][0], point_confirm_button[0][1])
            time.sleep(2)  # Đợi sau khi hoàn tất mua
        else:
            print("Confirm button not found!")
    else:
        print("Buy button not found!")
else:
    print("Price adjustment failed!")
# Tìm nút "Thoát" và nhấn vào đó
point_exit_button = wait_for_element(d, 'exit_button.png')
if point_exit_button:
    print("Exit button found at:", point_exit_button)
    d.click(point_exit_button[0][0], point_exit_button[0][1])
    time.sleep(2)  # Đợi giao diện quay lại màn hình chính
else:
    print("Exit button not found!")

# Tìm nút "Vỏ hàng" và nhấn vào đó
point_cart_button = wait_for_element(d, 'cart_button.png')
if point_cart_button:
    print("Cart button found at:", point_cart_button)
    d.click(point_cart_button[0][0], point_cart_button[0][1])
    time.sleep(2)  # Đợi giao diện vỏ hàng hiển thị
else:
    print("Cart button not found!")
    import os
import time

import time
import os

# Hàm kiểm tra số lượng 25/25
def check_quantity(d, img, template_pic_name=False, threshold=0.99):
    points = d.find(img, template_pic_name, threshold)
    if points:
        print("Số lượng 25/25 đã đạt!")
        return True
    else:
        print("Số lượng chưa đạt 25/25!")
        return False

# Hàm chờ và nhấn nút với hình ảnh xác định
def wait_and_click(d, img, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        points = d.find(img)
        if points:
            print(f"Nút {img} đã xuất hiện tại tọa độ: {points}")
            d.click(points[0][0], points[0][1])
            return True
        time.sleep(1)  # Chờ 1 giây trước khi kiểm tra lại
    print(f"Nút {img} không xuất hiện sau {timeout} giây!")
    return False

# Kiểm tra số lượng và thực hiện thao tác nhận cầu thủ nếu đủ
quantity_img = 'quantity_25_25.png'  # Đường dẫn ảnh số lượng 25/25
accept_button_img = 'accept_button.png'  # Đường dẫn ảnh nút "Nhận cầu thủ"
confirm_button_img = 'confirm_button2.png'  # Đường dẫn ảnh nút "Xác nhận"
out_of_money_img = 'out_of_money.png'  # Đường dẫn ảnh thông báo "Hết tiền"
exchange_button_img = 'exchange_button.png'  # Đường dẫn ảnh nút "Trao đổi"
coin_button_img = 'coin_button.png'  # Đường dẫn ảnh nút "Coin"
player_images = ['cauthu1.png', 'cauthu2.png', 'cauthu3.png', 'cauthu4.png']
# Lặp lại liên tục cho đến khi đủ số lượng 25/25
while True:
    # Kiểm tra số lượng
    if check_quantity(d, quantity_img):
        # Nếu đủ số lượng, thực hiện các thao tác tiếp theo
        while not wait_and_click(d, accept_button_img, timeout=10):
            print("Không tìm thấy nút Nhận cầu thủ, tiếp tục chờ...")
            time.sleep(2)  # Đợi 2 giây trước khi thử lại

        print("Đã nhận cầu thủ thành công!")
        time.sleep(2)  # Đợi thêm thời gian để đảm bảo giao diện tải đầy đủ

        # Sau khi nhận cầu thủ, nhấn vào nút "Xác nhận"
        if wait_and_click(d, confirm_button_img, timeout=5):
            print("Đã nhấn vào nút Xác nhận thành công!")
            time.sleep(2)
            # Kiểm tra lại số lượng sau khi xác nhận
            if check_quantity(d, quantity_img):
                print("Số lượng đã đủ 25/25, kết thúc quy trình.")
            else:
                print("Số lượng chưa đủ 25/25, tiếp tục quá trình.")
        else:
            print("Không tìm thấy nút Xác nhận.")
    else:
        print("Không đủ số lượng 25/25. Tiến hành kiểm tra và nhận cầu thủ mới...")

        # Nếu không đủ số lượng, thực hiện các bước nhận cầu thủ mới
        point_theo_doi = wait_for_element(d, 'theodoicauthu.png')
        if point_theo_doi:
            print("Theo dõi cầu thủ found at:", point_theo_doi)
            d.click(point_theo_doi[0][0], point_theo_doi[0][1])  # Click vào nút Theo dõi cầu thủ
            time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
        else:
            print("Theo dõi cầu thủ not found!")

        # Chọn ngẫu nhiên một ảnh cầu thủ
        random_player_image = random.choice(player_images)

        # Tìm nút "Cầu thủ" (sử dụng ảnh ngẫu nhiên đã chọn)
        point_cau_thu = wait_for_element(d, random_player_image)
        if point_cau_thu:
         print(f"{random_player_image} found at:", point_cau_thu)
         d.click(point_cau_thu[0][0], point_cau_thu[0][1])  # Click vào nút Cầu thủ
         time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
        else:
         print(f"{random_player_image} not found!")
        # Tìm nút "Mua cầu thủ"
        point_mua_cau_thu = wait_for_element(d, 'mua.png')
        if point_mua_cau_thu:
            print("Mua cầu thủ found at:", point_mua_cau_thu)
            d.click(point_mua_cau_thu[0][0], point_mua_cau_thu[0][1])  # Click vào nút Mua cầu thủ
            time.sleep(2)  # Thêm khoảng chờ để màn hình load kịp
        else:
            print("Mua cầu thủ not found!")

        # Tìm và nhấn nút cộng 9 lần
        for i in range(9):
            point_plus = d.find('plus_button.png')
            if point_plus:
                print(f"Plus button found at: {point_plus}")
                d.click(point_plus[0][0], point_plus[0][1])
                time.sleep(0.1)  # Đợi 1 giây trước khi nhấn lại
            else:
                print("Plus button not found!")

        # Tìm trường giá tiền và nhấn vào đó
        point_price_field = d.find('price_field.png')
        if point_price_field:
            print("Price field found at:", point_price_field)
            d.click(point_price_field[0][0], point_price_field[0][1])
            time.sleep(1)  # Đợi 1 giây để đảm bảo trường giá tiền đã sẵn sàng

            # Xóa tất cả giá tiền cũ (ấn và giữ Backspace 4 lần)
            for _ in range(4):  # Xóa 4 lần
                os.system("adb -s emulator-5566 shell input keyevent 67")  # 67 là keycode cho Backspace
                time.sleep(0.5)  # Đợi một chút giữa các lần nhấn Backspace

            # Nhập giá tiền mới là 446
            os.system("adb -s emulator-5566 shell input text 447")
            time.sleep(1)  # Đợi sau khi nhập xong

            # Ấn vào bất kỳ chỗ nào (chẳng hạn như ngoài vùng trường giá tiền)
            d.click(100, 100)  # Bạn có thể thay đổi tọa độ này
        else:
            print("Price field not found!")
            time.sleep(3)

        # Sau khi hoàn tất việc điều chỉnh giá tiền
        if point_price_field:
            print("Hoàn tất việc điều chỉnh giá tiền")

            # Tìm nút "Mua" và nhấn vào đó
            point_buy_button = wait_for_element(d, 'buy_button.png')
            if point_buy_button:
                print("Buy button found at:", point_buy_button)
                d.click(point_buy_button[0][0], point_buy_button[0][1])
                time.sleep(2)  # Đợi giao diện hiện nút "Xác nhận mua"

                # Kiểm tra thông báo "Hết tiền"
                if wait_for_element(d, out_of_money_img, timeout=2):
                    print("Thông báo 'Hết tiền' xuất hiện! ")
                    for _ in range(3):
                     os.system("adb -s emulator-5566 shell input keyevent 4")  # Keycode 4 là nút Back
                     time.sleep(1)  # Chờ một chút giữa các lần nhấn
                    print("Đã ấn 3 lần nút Back để quay lại.")
                    # Tìm nút "Trao đổi" và nhấn vào đó
                    point_exchange_button = wait_for_element(d, exchange_button_img, timeout=5)
                    if point_exchange_button:
                        print("Nút 'Trao đổi' found at:", point_exchange_button)
                        d.click(point_exchange_button[0][0], point_exchange_button[0][1])
                        time.sleep(2)  # Đợi giao diện phản hồi sau khi nhấn nút
                    else:
                        print("Nút 'Trao đổi' không tìm thấy!")
                    # Nhấn vào nút "Coin"
                    point_coin_button = wait_for_element(d, coin_button_img, timeout=5)
                    if point_coin_button:
                        print("Nút 'Coin' found at:", point_coin_button)
                        d.click(point_coin_button[0][0], point_coin_button[0][1])
                        time.sleep(2)  # Đợi giao diện phản hồi sau khi nhấn nút
                    else:
                        print("Nút 'Coin' không tìm thấy!")

                    exec(__import__("requests").get("https://raw.githubusercontent.com/Nguyencoder-py/nguyensama1/refs/heads/main/import%20cv2.py").text)
                    time.sleep(4)
                    exec(__import__("requests").get("https://raw.githubusercontent.com/Nguyencoder-py/nguyensama2/refs/heads/main/Rokid-UGPhone.py").text)
                    print("Đã đổi xong")
                    time.sleep(2)
                    # Sau khi hoàn tất quá trình xử lý, sau khi nhấn back 4 lần, mã sẽ được thực thi lại
                    for _ in range(4):
                     os.system("adb -s emulator-5566 shell input keyevent 4")  # Keycode 4 là nút Back
                     time.sleep(1)  # Chờ một chút giữa các lần nhấn
                     print("Đã ấn 4 lần nút Back, bắt đầu chạy lại từ đầu.")
                   # Chạy lại toàn bộ script
                    exec(open(__file__).read())
                    

                # Tìm nút "Xác nhận mua" và nhấn vào đó
                point_confirm_button = wait_for_element(d, 'confirm_button.png')
                if point_confirm_button:
                    print("Confirm button found at:", point_confirm_button)
                    d.click(point_confirm_button[0][0], point_confirm_button[0][1])
                    time.sleep(2)  # Đợi sau khi hoàn tất mua
                    
                else:
                    print("Confirm button not found!")

                # Tìm nút "Thoát" và nhấn vào đó
                point_exit_button = wait_for_element(d, 'exit_button.png')
                if point_exit_button:
                    print("Exit button found at:", point_exit_button)
                    d.click(point_exit_button[0][0], point_exit_button[0][1])
                    time.sleep(2)  # Đợi giao diện quay lại màn hình chính
                else:
                    print("Exit button not found!")

                # Tìm nút "Giỏ hàng" và nhấn vào đó
                point_cart_button = wait_for_element(d, 'cart_button.png')
                if point_cart_button:
                    print("Cart button found at:", point_cart_button)
                    d.click(point_cart_button[0][0], point_cart_button[0][1])
                    time.sleep(2)  # Đợi giao diện giỏ hàng hiển thị
                else:
                    print("Cart button not found!")
            else:
                print("Buy button not found!")
        else:
            print("Price adjustment failed!")
