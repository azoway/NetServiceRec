# DeepSeek Registration and Local Model Deployment Guide

To start using DeepSeek, you can either register online or deploy the model locally. Below is a detailed step-by-step guide:

---

## **I. Register and Use DeepSeek Online**

1. **Visit the Official Website**:
   - Open the DeepSeek official website: [https://www.deepseek.com/](https://www.deepseek.com/)

2. **Register an Account**:
   - Click the "Register" or "Sign Up" button on the page
   - Enter your phone number, set a password, and follow the prompts to complete registration
   - If you need a Chinese phone number, you can use an SMS activation platform for assisted registration. Below are the registration channels:
   - [Quick Registration Link for the China Version of SMS Activation Platform - Direct Access to DeepSeek](http://h5.yezi66.net:90/invite/9607189)
   - [Quick Registration Link for the International Version of SMS Activation Platform - Direct Access to DeepSeek](https://sms-activate.org/?ref=3245417)

---

## **II. Local DeepSeek Model Deployment**

If you want to run the DeepSeek model locally, here are the detailed steps:

1. **Install Ollama**:
   - Ollama is a tool for managing and running large language models locally
   - Visit the Ollama official website
   - Download and install the appropriate version for your operating system

2. **Download DeepSeek Model**:
   - In your terminal or command line, use Ollama to download the DeepSeek-R1 model:
     ```
     ollama pull deepseek-r1
     ```
   - Wait for the model download to complete

3. **Run the Model**:
   - Enter the following command in your terminal to start the model:
     ```
     ollama run deepseek-r1
     ```
   - Once the model starts, you can interact with it in the terminal by entering your questions, and the model will generate corresponding responses

4. **Visual Interface (Optional)**:
   - If you prefer using a graphical interface to interact with the model, you can install Chatbox
   - Visit the Chatbox project page
   - Download and install the version suitable for your system
   - Configure Chatbox to use your local DeepSeek model, and you can interact through the graphical interface

**Important Notes**:

- **Hardware Requirements**: Running large models requires high hardware specifications. For example, a 1.5B parameter model requires at least a GPU with 4GB VRAM and 16GB RAM. If hardware specifications are insufficient, the model may use CPU for computation, which will result in longer processing times.

- **Model Size**: DeepSeek-R1 model comes in different parameter sizes. For example, the 7B parameter model is approximately 4.7GB. Choose the appropriate model version based on your hardware configuration.

Successfully tested and deployed DeepSeek r1 7b model locally on MAC M3, achieving AI model inference in an offline environment with good performance. 