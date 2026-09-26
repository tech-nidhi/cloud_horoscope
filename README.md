# 🔮 Cloud Horoscope

A serverless, AI-powered web application that delivers personalized, cosmic, and humorous astrology readings tailored for cloud engineers, architects, and developers.

![React](https://img.shields.io/badge/React-18.x-61DAFB?logo=react&logoColor=black)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-Serverless-FF9900?logo=awslambda&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-Generative%20AI-232F3E?logo=amazon-aws&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwind-css&logoColor=white)

---

## 🌟 Overview

**Cloud Horoscope** takes a user's name and date of birth to calculate their accurate Western Zodiac sign and deliver a custom, cloud-themed reading. Each horoscope pairs astrological wisdom with cloud computing realities:

- ⚡ **Lucky AWS Service:** e.g., *AWS Lambda & EC2 Spot*, *Amazon DynamoDB Global Tables*
- 🌐 **Lucky AWS Region:** e.g., *us-east-1*, *eu-west-1*, *ap-northeast-1*
- 🛡️ **Architecture Resilience Score (SLA %):** e.g., *99.999%*
- 🤖 **AI-Generated Horoscope:** Humorous and insightful predictions regarding deployments, scaling, security, and cost optimization powered by **Amazon Bedrock (Claude 3 Haiku)** with an offline fallback engine.

---

## 🛠️ Architecture & Technologies

### **Frontend**
- **React 18 & React Router v6:** Modern single-page application structure.
- **Tailwind CSS:** Responsive cosmic dark-mode interface with glassmorphism effects.
- **HTML5 Canvas & Report Exporter:** Direct client-side generation and export of `.png` horoscope cards and `.md` reports.

### **Backend (Serverless)**
- **AWS Lambda (Python 3.x):** Serverless compute processing requests, computing astrological math, and managing AI interactions.
- **Amazon Bedrock:** Foundation model invocation (`anthropic.claude-3-haiku-20240307`) for dynamic horoscope generation.
- **Amazon API Gateway:** REST API endpoint routing frontend requests to Lambda with CORS enabled.
- **Boto3 SDK:** AWS SDK for seamless integration with Amazon Bedrock and AWS services.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+) and npm
- Python 3.9+ (for Lambda development)
- AWS Account with Amazon Bedrock model access enabled (optional for live backend)

### 1. Running Frontend Locally

```bash
# Install dependencies
npm install

# Start development server
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the application in your browser.

### 2. Backend Lambda Setup

```bash
cd lambda_function

# Install dependencies into target
pip install -r requirements.txt -t .

# Package and deploy
zip -r function.zip .
```

---

## 🧪 Testing

### Frontend Tests
```bash
npm test
```

### Backend Tests
```bash
cd lambda_function
python3 -m unittest discover -s . -p "test_*.py"
```

---

## 📄 License
MIT License