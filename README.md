\# ☁️ Cloud Horoscope 🔮

Ever wondered what your zodiac sign would say if it lived in the cloud? 😄

\*\*Cloud Horoscope\*\* is a fun, serverless web app that generates \*\*AWS-themed horoscopes\*\* based on your \*\*name and date of birth\*\*.

\---

\## ✨ Features

\* 🔮 Enter your \*\*name\*\* and \*\*DOB (dd/mm/yyyy)\*\*

\* ☁️ Get a \*\*unique AWS cloud-themed horoscope\*\*

\* 🤖 Powered by AI (Amazon Bedrock)

\* ⚡ Fully serverless architecture

\* 📸 Shareable results (perfect for social media!)

\---

\## 🧠 How It Works

1\. User enters name and DOB on the frontend

2\. Request is sent to backend API

3\. Lambda processes DOB → determines zodiac sign

4\. Amazon Bedrock generates a fun AWS-style horoscope

5\. Response is sent back and displayed instantly

\---

\## 🏗️ Architecture

\`\`\`

Frontend (AWS Amplify)

↓

API Gateway (REST API)

↓

AWS Lambda (Python)

↓

Amazon Bedrock (Claude 3 Haiku)

↓

CloudWatch Logs (Monitoring)

\`\`\`

\### 🔧 Services Used

\* \*\*AWS Amplify\*\* → Frontend hosting

\* \*\*Amazon API Gateway\*\* → API layer

\* \*\*AWS Lambda\*\* → Backend logic

\* \*\*Amazon Bedrock\*\* → AI-powered horoscope generation

\* \*\*Amazon CloudWatch\*\* → Logging & monitoring

\---

\## 🚀 Getting Started (Local Setup)

\### 1️⃣ Clone the repository

\`\`\`bash

git clone https://github.com/your-username/cloud-horoscope.git

cd cloud-horoscope

\`\`\`

\### 2️⃣ Backend Setup

\`\`\`bash

cd backend

python -m venv venv

venv\\Scripts\\activate # Windows

pip install -r requirements.txt

\`\`\`

\### 3️⃣ Run locally (test Lambda logic)

\`\`\`bash

python lambda\_function.py

\`\`\`

\---

\## 🧪 API Usage

\### Endpoint

\`\`\`

POST /horoscope

\`\`\`

\### Sample Request

\`\`\`json

{

"name": "Maitry",

"dob": "05/10/2004"

}

\`\`\`

\### Sample Response

\`\`\`json

{

"sign": "Libra",

"horoscope": "Hey Maitry, your Libra energy is scaling like an EC2 Auto Scaling group — balanced and always available!"

}

\`\`\`

\---

\## 🔐 Environment Variables

| Variable | Description | Default |

| --------------- | --------------- | ----------------------------------------- |

| PROJECT\_NAME | Name of the app | Cloud Horoscope |

| AUTHOR\_NAME | Creator name | Unknown |

| DEFAULT\_MESSAGE | Welcome message | Welcome to Cloud Horoscope powered by AWS |

\---

\## 💡 Future Enhancements

\* 📊 Store horoscope history using DynamoDB

\* 📧 Daily horoscope emails using Amazon SES

\* 🎨 Horoscope image generation (Bedrock Image Models)

\* 📱 Mobile app version

\---

\## 🤝 Contributing

Feel free to fork this repo, improve features, or add new AWS integrations!

\---

\## 📸 Share Your Horoscope!

Tried the app?

Take a screenshot 📸 and share it on LinkedIn with \*\*#CloudHoroscope\*\*

Don’t forget to tag us — we’d love to see your cloud destiny ☁️😄

\---