# 量化交易專案集合 (Quantitative Trading Projects)

這個倉庫包含了多個量化交易相關的專案和工具，涵蓋了從基礎回測到實時交易的完整生態系統。

## 📁 專案結構

### 核心交易系統
- **`advice_bot/`** - 交易建議機器人
- **`Automated_trading/`** - 自動化交易系統
- **`real/`** - 實盤交易模組
- **`Crypto_trading/`** - 加密貨幣交易策略

### 回測與研究
- **`Backtestingsample/`** - 回測範例集合，包含多種策略測試
- **`studygroup1/`** - 資金費率套利研究
- **`studygroup2/`** - 技術分析模式研究

### 交易所接口
- **`Binance_alpha_system/`** - Binance 交易系統
- **`bingx/`** - BingX 交易所接口
- **`Kronos/`** - Woox 交易所 WebSocket 接口
- **`Shioaji/`** - 永豐金證券 API

### 數據與工具
- **`Scraping/`** - 數據爬蟲工具
- **`Lambda/`** - 雲端函數
- **`Talib/`** - 技術分析指標庫

## 🚀 快速開始

### 環境設置
```bash
# 創建虛擬環境
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
# 或
myenv\Scripts\activate     # Windows

# 安裝依賴
pip install -r requirements.txt
```

### 基本使用

#### 1. 回測系統
```bash
cd Backtestingsample
python BackTest.py
```

#### 2. 實時交易
```bash
cd real
python 實單範例.py
```

#### 3. 數據爬蟲
```bash
cd Scraping
python twtop20.py
```

## 📊 主要功能

### 交易策略
- 資金費率套利策略
- 技術分析模式識別
- 動量交易策略
- 網格交易系統

### 風險管理
- 動態止損機制
- 倉位管理系統
- 槓桿控制工具

### 數據處理
- 實時行情數據獲取
- 歷史數據回測
- 技術指標計算
- 市場情緒分析

## 🔧 配置說明

### API 設置
在使用前請確保配置相關的 API 密鑰：

```python
# config.py 範例
BINANCE_API_KEY = "your_api_key"
BINANCE_SECRET_KEY = "your_secret_key"
LINE_TOKEN = "your_line_token"  # 用於通知
```

### 交易參數
- 最大倉位限制
- 止損止盈設置
- 交易手續費計算
- 滑點控制

## 📈 策略詳細說明

### 資金費率套利 (Funding Rate Arbitrage)
- 檔案位置: `studygroup1/`
- 利用永續合約資金費率差異進行套利
- 支援 BTC、BNB 等主流幣種

### 技術分析模式 (Pattern Recognition)
- 檔案位置: `studygroup2/`
- 識別價格模式和趨勢
- 整合持倉量 (Open Interest) 分析

## 🛠 依賴套件

主要使用的 Python 套件：
- `pandas` - 數據處理
- `numpy` - 數值計算
- `requests` - API 請求
- `websocket-client` - WebSocket 連接
- `talib` - 技術分析指標
- `matplotlib/plotly` - 數據視覺化

## ⚠️ 風險提示

**重要警告**: 
- 本專案僅供學習和研究使用
- 量化交易涉及高風險，可能導致重大損失
- 在實盤交易前請充分測試策略
- 建議使用小額資金進行測試
- 不構成投資建議，請謹慎使用

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request：

1. Fork 此倉庫
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📞 聯繫方式

- GitHub: [@Allenwang2004](https://github.com/Allenwang2004)
- 專案連結: [https://github.com/Allenwang2004/Quant_projects](https://github.com/Allenwang2004/Quant_projects)

## 📄 授權協議

本專案採用 MIT 授權協議。詳情請參閱 [LICENSE](LICENSE) 文件。

---

**免責聲明**: 本軟體按「現狀」提供，不提供任何明示或暗示的保證。作者不對使用本軟體造成的任何損失承擔責任。