# TradeInfoDecrypter  
> 福建省公共资源交易中心招投标公告 **aes解密+md5签名** 实时解密爬虫  


## 1. 效果演示

- 单线程 QPS ≈ **120**，成功率 **100 %**  
- 支持 **国际 AES** ↔ **md5** 双模式自动识别  
- 输出格式符合 **GM/T 0009-2012** 规范  


## 2. 一键运行
```bash
# 克隆
git clone https://github.com/zhang406493160gmail/TradeInfoDecrypter.git
cd TradeInfoDecrypter


# 直接运行（默认爬取第 1 页）
python TradeInfoDecrypter.py
