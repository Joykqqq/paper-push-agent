# AI 前沿论文每日推送 Agent

独立运行的 AI 论文推送系统，每天自动获取热门论文并推送到微信。

## 功能特性

- 🕐 **定时自动运行**：每天 14:00 自动触发（通过 cron / 任务计划程序）
- 📚 **热门论文来源**：HuggingFace Daily Papers，社区投票排名
- 🤖 **AI 中文解读**：调用 DeepSeek API 生成适合零基础理工本科生的通俗解读
- 📱 **微信推送**：通过 Server酱 推送到个人微信
- 📝 **完整论文信息**：包含作者、期刊状态、研究方法、创新点、关键结果

## 项目结构

```
paper_push_agent/
├── main.py              # 主程序入口
├── fetch_papers.py      # 论文获取模块（爬取 HF Papers）
├── parse_arxiv.py      # 摘要解析模块（解析 arXiv 页面）
├── summarize.py         # LLM 解读模块（调用 DeepSeek API）
├── push_wechat.py     # 推送模块（调用 Server酱 API）
├── config.py           # 配置管理（读取环境变量）
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量示例
└── README.md          # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
```

编辑 `.env`：

```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
SERVERCHAN_SENDKEY=your_serverchan_sendkey_here
PAPER_COUNT=3
TARGET_HOUR=14
```

### 3. 手动测试运行

```bash
python main.py
```

如果配置正确，你会收到一条微信推送。

### 4. 配置定时运行

#### Windows（任务计划程序）

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每天 14:00
4. 操作：启动程序
5. 程序/脚本：`C:\Python\python.exe`
6. 参数：`C:\Users\joy\paper_push_agent\main.py`

#### Linux / macOS（cron）

```bash
crontab -e
```

添加一行：

```
0 14 * * * cd /path/to/paper_push_agent && /usr/bin/python3 main.py >> log.txt 2>&1
```

## 环境变量说明

| 变量名 | 说明 | 获取方式 |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | https://platform.deepseek.com/ |
| `SERVERCHAN_SENDKEY` | Server酱 SendKey | https://sct.ftqq.com/ |
| `PAPER_COUNT` | 每日推送论文数量（默认3） | 可选 |
| `TARGET_HOUR` | 推送时间（默认14） | 可选 |

## 如何获取 API Key

### DeepSeek API Key

1. 访问 https://platform.deepseek.com/
2. 注册登录
3. 进入"API Keys"页面
4. 创建新 Key
5. 复制并填入 `.env` 文件

### Server酱 SendKey

1. 访问 https://sct.ftqq.com/
2. 微信扫码登录
3. 进入"消息通道"，选择微信通道并保存
4. 进入"Key & API"，复制 SendKey
5. 填入 `.env` 文件

## 常见问题

### Q：运行后没有收到微信推送？

A：检查以下几点：
1. `.env` 文件中的 `SERVERCHAN_SENDKEY` 是否正确
2. 微信是否关注了"方糖服务号"
3. 运行 `python main.py` 查看控制台输出，是否有错误信息

### Q：DeepSeek API 调用失败？

A：检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确，以及账户是否有余额。

### Q：如何修改推送时间？

A：修改 `.env` 中的 `TARGET_HOUR`，并同步修改 cron / 任务计划程序的触发时间。

## 技术栈

- **Python 3.8+**
- **requests**：HTTP 请求
- **beautifulsoup4**：HTML 解析
- **openai**：调用 DeepSeek API（兼容 OpenAI SDK）
- **python-dotenv**：环境变量管理

## License

MIT License
