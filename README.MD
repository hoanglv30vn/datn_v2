*********** Cài đặt - chạy code*********
gói pyrebase pyton: pip install Pyrebase
tạo các cặp cổng com kết nối với nhau. (2 cặp)
chạy file code gateway: GATEWAY\GW_python\gateway_config.py
    Lưu ý: có lúc file sẽ bị lỗi do lỗi cổng com --> xóa file .db, và chạy lại
	   có lúc file sẽ bị lỗi do gửi uart nhưng không có nhận được xác nhận --> kiểm tra các cổng com và chạy lại

chạy file mô phỏng TCP-gateway: GATEWAY\UDP\tcpserve.py
	nhập cổng com nối với cổng com gateway.
chạy file mô phỏng TCP-node: GATEWAY\UDP\tcpclient.py
	nhập cổng com nối với cổng com pic.

mở proteus file: NODE\proteus\helloprt
nếu 2 node thì mở thêm file: NODE\proteus\helloprt2
giữ nút trên cùng 3s để vào config. giữ 3s để hoàn thành config


*******DATN_V1
27/9 --> 11/10: 
https://github.com/hoanglv30vn/datn
-[PIC] nút nhấn B0 -> chọn id node (1-10) 
-[PIC] tạm thời chỉ 2 node 1 và 2 - đo nhiệt độ gửi UART ( T>27 gửi) 
-[PIC] nhận UART hiển thị LCD, điều khiển LED 
-[TCP] chọn COM, tên node 
-[TCP] TCP server: nhận TCP gửi UART(GW), nhận UART gửi TCP tới mọi client 
-[TCP] TCP client: nhận UART(NODE) gửi TCP(server), nhận TCP gửi UART. 
-[GATEWAY] chọn COM, baudrate - nhận UART, hiển thị, phân tích id, gửi firebase. 
-[GATEWAY] lắng nghe firebase, gửi uart tới tất cả các node.


*******DATN_V2
27/10 -->
- SỬA CẤU TRÚC FIREBASE ==> SỬA LẠI CODE
- PYTHON NHẬP ID GW, GET DATA TỪ FIREBASE.
- PIC NHẬP ID GW, ID NODE, ĐỂ XÁC NHẬN.
- ĐIỀU KHIỂN THIẾT BỊ
6/11: KHÁ LÀ OKE RỒI
- [CONFIG] cấu hình node, nhập ID GW, IDNODE, Gửi tới GW. GW gửi xác nhận.
- [ĐIỀU KHIỂN] node nhận thông tin điều khiển từ GW, điều khiển thiết bị qua IC 74595. (dịch bit, đk 8 thiết bị)
- [ANALOG] nhận số thiết bị cảm biến từ GW. đo nhiệt độ, gửi uart.
- [GW] nhập ID nhà, nhấn oke để load dữ liệu từ FIREBASE
- [GW] hiện danh sách các thiết bị, trạng thái phòng active. đánh số thứ tự cho các thiết bị để điều khiển, và 1 số hàm chuyển đổi
- [GW] nhận dữ liệu từ uart, gửi firebase.
- ... kế thừa 1 số tính năng từ V1
