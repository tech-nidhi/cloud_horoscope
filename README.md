# ☁️ Cloud Horoscope

> ### **Where your zodiac meets the cloud.**
>
> What if your horoscope could tell you something about your infrastructure?

Cloud Horoscope is a **serverless, AI-powered web application** that combines Western astrology with modern cloud engineering. Enter your name and date of birth to discover your zodiac sign and receive a personalized, humorous **cloud-themed horoscope powered by Amazon Bedrock**.

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?logo=awslambda&logoColor=white)](https://aws.amazon.com/lambda/)
[![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock-232F3E?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![API Gateway](https://img.shields.io/badge/Amazon-API_Gateway-FF4F8B?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/api-gateway/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.3.0-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

<br>

> 🏆 **Featured in the Builder Zone · AWS Community Day Vadodara 2025**

---

## 🌌 The Idea

Traditional horoscopes ask:

> *"What do the stars have planned for you?"*

Cloud Horoscope asks:

> **"What does your infrastructure have planned for you today?"**

It turns zodiac characteristics into a playful cloud-engineering experience, connecting astrology with concepts developers work with every day:

`Scaling` · `Security` · `Reliability` · `Deployments` · `Infrastructure` · `Generative AI`

---

## ✨ What You Get

Every horoscope generates a unique combination of:

| ☁️ Cloud Insight | 🔮 What it means |
|---|---|
| **Lucky AWS Service** | Your cloud service for the day |
| **Lucky AWS Region** | Your cosmic AWS destination |
| **Architecture Resilience Score** | A humorous SLA-style reliability score |
| **AI Cloud Prediction** | A personalized infrastructure-themed reading |
| **Zodiac Profile** | Your Western zodiac sign and elemental association |

---

# ⚡ Features

<table>
<tr>
<td width="50%">

### 🤖 AI-Powered Readings
Personalized cloud-themed predictions generated using **Amazon Bedrock**.

</td>
<td width="50%">

### ♈ Zodiac Detection
Automatically determines the user's Western zodiac sign from their date of birth.

</td>
</tr>

<tr>
<td>

### ☁️ Lucky AWS Service
Maps zodiac and elemental characteristics to AWS services.

</td>
<td>

### 🌎 Lucky AWS Region
Generates a personalized AWS region association for every reading.

</td>
</tr>

<tr>
<td>

### 📊 Architecture Resilience
Receive a humorous SLA-style resilience score for your cosmic infrastructure.

</td>
<td>

### 🔄 Multiple Readings
Refresh and explore different cloud-themed horoscope variations.

</td>
</tr>

<tr>
<td>

### 📋 Easy Sharing
Copy your horoscope directly to the clipboard.

</td>
<td>

### 📄 Markdown Export
Download your reading as a Markdown report.

</td>
</tr>

<tr>
<td>

### 🖼️ Horoscope Cards
Generate downloadable PNG cards directly in the browser using HTML5 Canvas.

</td>
<td>

### 🔌 API / Local Mode
Switch between the live AWS backend and the local horoscope engine.

</td>
</tr>
</table>

---

# 🏗️ Serverless Architecture

Cloud Horoscope follows a **serverless frontend-to-AI architecture**, keeping the application lightweight while using AWS managed services for backend processing and generative AI.

```mermaid
flowchart LR

    U(["👤 User"])

    subgraph CLIENT["💻 CLIENT"]
        UI["React 18<br/>Web Application"]
        ENGINE["Local Horoscope<br/>Engine"]
        EXPORT["Canvas<br/>Report Exporter"]
    end

    subgraph AWS["☁️ AWS CLOUD"]
        API["Amazon API Gateway"]
        L["AWS Lambda"]
        AI["Amazon Bedrock"]
        IAM["AWS IAM"]
        CW["Amazon CloudWatch"]
    end

    U -->|"Name + Date of Birth"| UI

    UI -->|"POST /horoscope"| API
    API --> L
    L -->|"Generate AI Reading"| AI
    AI -->|"Generated Horoscope"| L
    L -->|"JSON Response"| API
    API -->|"Horoscope"| UI

    UI -.->|"Local / Offline"| ENGINE
    UI -->|"PNG / Markdown"| EXPORT

    IAM -.->|"Permissions"| L
    L -.->|"Logs"| CW
