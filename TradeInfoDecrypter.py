import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import datetime
import hashlib
import time

# 用户输入页码
page = int(input("请输入要爬取的页码："))

# 时间参数（固定最近 180 天）
current_time = datetime.datetime.now()
begin_time = (current_time - datetime.timedelta(days=180)).strftime('%Y-%m-%d 00:00:00')
end_time = current_time.strftime('%Y-%m-%d 23:59:59')
time_range = int(time.time() * 1000)

# Cookies（固定值，长期可用）
cookies = {
    'Hm_lvt_db393520fa240b442a13a6d1c5ae95c1': '1753086993',
    'Hm_lvt_94bfa5b89a33cebfead2f88d38657023': '1753086993',
    'Hm_lvt_9d1de05cc99f08ddb5dc6d5e4d32ad30': '1753086993',
    '__root_domain_v': '.fujian.gov.cn',
    '_qddaz': 'QD.514353086992997',
    '_qddagsx_02095bad0b': '85de6a42420450ba890292adb8db284945a3070dbbb200325dae4f9a48efe6ebd9b9be6f2bbf7b10948f071dcff643a64658cd00e9dabee4fdea9ac91a2ba53bc076d9308e388252d2263bbe6603a3c4a3602e05e37493cef1533e3256512c0e1e1ab6219487d6cf5754cefd775ee2a5b3bfe53c9f1291d54cb7f0d6fbe3615c',
    'lastSE': 'baidu',
}

# 签名生成函数（核心逻辑）
def generate_portal_sign(params, secret_key="B3978D054A72A7002063637CCDF6B2E5"):
    filtered = {k: v for k, v in params.items() if v not in ["", None]}
    sorted_params = sorted(filtered.items(), key=lambda x: x[0])
    query_string = ''.join([f"{k}{v}" for k, v in sorted_params])
    sign_string = secret_key + query_string
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()

# 解密函数（核心逻辑）
def decrypt(cipher_text):
    key = 'EB444973714E4A40876CE66BE45D5930'.encode('utf-8')
    iv = 'B5A8904209931867'.encode('utf-8')
    cipher_data = base64.b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(cipher_data)
    return unpad(decrypted, AES.block_size).decode('utf-8')

# 请求数据
json_data = {
    'pageNo': page,
    'pageSize': 20,
    'total': 0,  # 初始为 0，签名时使用
    'AREACODE': '',
    'M_PROJECT_TYPE': '',
    'KIND': 'GCJS',
    'GGTYPE': '1',
    'PROTYPE': '',
    'timeType': '6',
    'BeginTime': begin_time,
    'EndTime': end_time,
    'createTime': '',
    'ts': time_range,
}

# 构造签名参数
sign_params = {
    "BeginTime": json_data["BeginTime"],
    "EndTime": json_data["EndTime"],
    "GGTYPE": json_data["GGTYPE"],
    "KIND": json_data["KIND"],
    "M_PROJECT_TYPE": json_data["M_PROJECT_TYPE"],
    "PROTYPE": json_data["PROTYPE"],
    "createTime": json_data["createTime"],
    "pageNo": json_data["pageNo"],
    "pageSize": json_data["pageSize"],
    "timeType": json_data["timeType"],
    "total": json_data["total"],
    "ts": json_data["ts"],
}

# 生成签名
portal_sign = generate_portal_sign(sign_params)

# 请求头
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://ggzyfw.fujian.gov.cn',
    'Referer': 'https://ggzyfw.fujian.gov.cn/business/list/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'portal-sign': portal_sign,
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# 发送请求
response = requests.post(
    'https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo',
    cookies=cookies,
    headers=headers,
    json=json_data
)

# 获取加密数据
result = response.json()
encrypted_data = result.get("Data")

if not encrypted_data:
    print("接口返回 Data 为空，可能签名错误")
    print("原始响应：", result)
else:
    try:
        decrypted_data = decrypt(encrypted_data)
        print("解密结果：", decrypted_data)
    except Exception as e:
        print("解密失败：", str(e))