# deepseek注册使用和本地跑deepseek模型r1

> 围绕「deepseek注册使用和本地跑deepseek模型r1」，本文保留关键参数与套餐要点，并补充选购时容易忽略的细节。

---

## **一、注册并在线使用 DeepSeek**

以下信息为公开套餐与经验整理，具体价格和库存请以下单页实时展示为准。

1. **访问官网**：
   - 打开 DeepSeek 官方网站：[https://www.deepseek.com/](https://www.deepseek.com/)。

2. **注册账号**：
   - 点击页面上的“注册”或“Sign Up”按钮
   - 输入您的手机号，设置密码，按照提示完成注册流程 . 
   - 如果需要中国的手机号可以使用接码平台的号码进行辅助注册，以下是注册渠道 
   - If you need a Chinese phone number, you can use a SMS activation platform number for assisted. registration. Below are the registration channels:
   - [中国版接码平台快速注册deepseek直达地址](https://www.qc86.shop/login?inviterCode=300138)
   - [国际版接码平台快速注册deepseek直达地址](https://hero-sms.com/?ref=509318)
   - [Quick Registration Link for the China Version of SMS Activation Platform - Direct Access to DeepSeek](https://www.qc86.shop/login?inviterCode=300138)
   - [Quick Registration Link for the International Version of SMS Activation Platform - Direct Access to DeepSeek](https://hero-sms.com/?ref=509318)
---

## **二、本地部署 DeepSeek 模型**

如果您希望在本地运行 DeepSeek 模型，以下是详细的步骤：

1. **安装 Ollama**：
   - Ollama 是一个用于本地管理和运行大模型的工具。
   - 访问 Ollama 官网：
   - 根据您的操作系统，下载并安装适合的版本。

2. **下载 DeepSeek 模型**：
   - 在终端或命令行中，使用 Ollama 下载 DeepSeek-R1 模型：
     ```
     ollama pull deepseek-r1
     ```
   - 等待模型下载完成。

3. **运行模型**：
   - 在终端中输入以下命令启动模型：
     ```
     ollama run deepseek-r1
     ```
   - 模型启动后，您可以在终端中与之交互，输入您的问题，模型会生成相应的回答。

4. **可视化界面（可选）**：
   - 如果您希望使用图形界面与模型交互，可以安装 Chatbox。
   - 访问 Chatbox 项目页面：
   - 下载并安装适合您系统的版本。
   - 在 Chatbox 中配置为使用本地的 DeepSeek 模型，即可通过图形界面进行交互。

**注意事项**：

- **硬件要求**：运行大型模型需要较高的硬件配置。以 1.5B 参数的模型为例，最低需要 4GB 显存的 GPU 和 16GB 内存。如果硬件配置不足，模型可能会使用 CPU 进行计算，这会导致计算时间延长。

- **模型大小**：DeepSeek-R1 模型有不同的参数规模。以 7B 参数的模型为例，模型大小约为 4.7GB。根据您的硬件配置，选择适合的模型版本。

实测已经使用 MAC M3 本地成功部署并运行 DeepSeek r1 模型7b，实现离线环境下的 AI 模型推理，体验还不错
