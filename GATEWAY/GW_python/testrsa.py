import random

def encode_data(data):
    # d=103
    d=463
    p=19
    q=11
    n=p*q  
    wn = (p-1)*(q-1)      
    e=7
    print("khóa công khai là: " + 'e=' + f'{e}' + 'n=' + f'{n}')
    list_m_int = [5, 7, 17, 31, 57,23,19,29,41,47,63,97,61]
    m=  random.choice(list_m_int)
    print(f'chọn M: {m}')
    c= pow(m,e) % n
    print("c=" + f'{c}')
    kqmahoa=''
    j=1
    for i in data:
        # char to ascii
        j=j+1
        somahoaascii = j*m - j + 3
        dauconghoactru = pow(-1,j%2+1)
        somahoaascii = somahoaascii % 15 + 1
        kqmahoa += chr( ord(i)+ dauconghoactru*somahoaascii)
    kqmahoa = kqmahoa + "___" + str(c) + "___" + str(n)
    return kqmahoa
    # print("kết quả mã hóa: " + kqmahoa )

def decode_data (datas):
    data = datas.split("___")
    c= int(data[1])
    n= int(data[2])
    print("khóa công khai là: " + 'c=' + f'{c}' + 'n=' + f'{n}')
    d=463
    kq_M=pow(c,d)%n
    print("tính ra M của bên B= "+ f'{kq_M}')
    kqgiaima=''
    j=1
    for i in data[0]:
        j=j+1
        somahoaascii = j*kq_M - j + 3
        dauconghoactru = pow(-1,j%2+1)
        somahoaascii = somahoaascii % 15 + 1
        kqgiaima += chr( ord(i)- dauconghoactru*somahoaascii)
    return kqgiaima 




# def encode_data(data):
#     # d=103
#     d=463
#     p=19
#     q=11
#     n=p*q  
#     wn = (p-1)*(q-1)      
#     e=7    
#     list_m_int = [5, 7, 17, 31, 57,23,19,29,41,47,63,97,61]
#     m=  random.choice(list_m_int)    
#     c= pow(m,e) % n
#     kqmahoa=''
#     j=1
#     for i in data:
#         # char to ascii
#         j=j+1
#         somahoaascii = j*m - j + 3
#         dauconghoactru = pow(-1,j%2+1)
#         somahoaascii = somahoaascii % 15 + 1
#         kqmahoa += chr( ord(i)+ dauconghoactru*somahoaascii)
#     kqmahoa = kqmahoa + "___" + str(c) + "___" + str(n)
#     return kqmahoa


# def decode_data (datas):
#     data = datas.split("___")
#     c= int(data[1])
#     n= int(data[2])
#     d=463
#     kq_M=pow(c,d)%n
#     kqgiaima=''
#     j=1
#     for i in data[0]:
#         j=j+1
#         somahoaascii = j*kq_M - j + 3
#         dauconghoactru = pow(-1,j%2+1)
#         somahoaascii = somahoaascii % 15 + 1
#         kqgiaima += chr( ord(i)- dauconghoactru*somahoaascii)
#     return kqgiaima 


# while True:
#     chuoimahoa = input("nhập chuỗi: ")
#     kqmahoa = encode_data(chuoimahoa)
#     print("mã hóa chuỗi:")
#     print(kqmahoa)

#     kqgiaima = decode_data(kqmahoa)
#     print("giải mã chuỗi:")
#     print(kqgiaima)

#     # xxxx = input("hihi")











while True:
    print("Bên A(bên nhận):")
    print("nhập 2 số nguyên tố:")
    # p=int(input("p:"))
    # q=int(input("q:"))
    p=13
    q=7
    n=p*q
    print("module của p và q là P x Q=" + f'{n}')
    wn = (p-1)*(q-1)

    print("Wn = (p-1)*(q-1) = " + f'{wn}')

    # e= int(input("nhập số mũ công khai e: "))
    e=7
    print("hệ thống tính cho bạn 1 vài số D bạn có thể chọn (d là số bí mật):")
    for i in range(200):
        sodu=(i*wn+1)%e
        if sodu == 0:
            print((i*wn+1)/e) 
    # d= int(input("nhập số mũ D bí mật bạn chọn: ")) 
    d=103


    print("khóa công khai là: " + 'e=' + f'{e}' + 'n=' + f'{n}')

    print("Bên B(bên gửi):")
    chuoimahoa = input("nhập chuỗi: ")
    m=int(input("nhập số nguyên tố M: "))
    c= pow(m,e) % n
    print("c=" + f'{c}')
    print("mã hóa chuỗi:")
    kqmahoa=''
    j=1
    for i in chuoimahoa:
        # char to ascii
        j=j+1
        somahoaascii = j*m - j + 3
        dauconghoactru = pow(-1,j%2+1)
        somahoaascii = somahoaascii % 30 + 1
        kqmahoa += chr( ord(i)+ dauconghoactru*somahoaascii)

    print("kết quả mã hóa: " + kqmahoa )

    print("gửi chuỗi và C cho bên A")


    print("bên A:")
    print("chuỗi nhận được là:" + kqmahoa)
    print("C nhận được là:" + f'{c}')
    kq_M=pow(c,d)%n
    print("tính ra M của bên B= "+ f'{kq_M}')
    print("giải mã:")
    kqgiaima=''
    j=1
    for i in kqmahoa:
        j=j+1
        somahoaascii = j*kq_M - j + 3
        dauconghoactru = pow(-1,j%2+1)
        somahoaascii = somahoaascii % 30 + 1
        kqgiaima += chr( ord(i)- dauconghoactru*somahoaascii)
    print("kết quả giải mã: " + kqgiaima)

    xxxx = input("hihi")