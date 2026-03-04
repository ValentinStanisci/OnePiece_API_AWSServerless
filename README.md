# 🏴‍☠️ One Piece Character API — AWS Serverless

Serverless REST API to query One Piece character information, built on AWS infrastructure.

> Portfolio project | Backend · Cloud · AWS

---

## ⚙️ Stack

| Layer | Technology |
|-------|-----------|
| Compute | AWS Lambda (Python 3.12) |
| API | API Gateway (HTTP API) |
| Database | Amazon RDS — PostgreSQL |
| Network | Private VPC with subnets and security groups |
| Access | IAM roles with least privilege permissions |

---

## 🧠 Architecture

```
Client → API Gateway → Lambda → RDS (PostgreSQL)
                                  └── Private VPC
```

Two independent Lambda functions:

- **`lambda-name`** — receives a character name and returns their data from the DB.
- **`lambda-question`** — receives a natural language question, extracts the name and returns a formatted answer.

Both Lambdas run inside a VPC and connect to RDS without exposing it to the internet.

---

## 📁 Project Structure

```
OnePiece_API_AWSServerless/
│
├── character_by_name/
│   ├── lambda_function.py
│   └── requirements.txt
│
├── character_by_question/
│   ├── lambda_function.py
│   └── requirements.txt
│
├── architecture.png
└── README.md
```

---

## 🔌 API Usage

### 1. Search by Name

**POST** `/character-by-name`

```json
{
  "name": "Monkey D. Luffy"
}
```

**Response:**

```json
{
  "name": "Monkey D. Luffy",
  "sea": "East Blue",
  "island": "Fuschia Village",
  "status": "Alive",
  "affiliation": "Pirates",
  "devil_fruits": [
    {
      "name": "Hito Hito no Mi: Modelo Nika",
      "type": "Mythical Zoan"
    }
  ]
}
```

### 2. Search by Question

**POST** `/character-by-question`

```json
{
  "question": "Who is Roronoa Zoro?"
}
```

**Response:**

```json
{
  "answer": "Roronoa Zoro is a character from East Blue. Originally from Shimotsuki Village, currently Alive. Affiliation: Pirates. Devil Fruit: No Devil Fruit."
}
```

---

## 🚀 Deploy

Dependencies are packaged locally and uploaded as a `.zip` to each Lambda.

```bash
# Inside each folder
pip install -r requirements.txt -t .
zip -r function.zip .
```

Then upload `function.zip` from the AWS Lambda console or with the AWS CLI.

---

## 🔐 Environment Variables

Credentials are not stored in the code. Set them in each Lambda from **AWS Console → Configuration → Environment variables**:

| Variable | Description |
|----------|-------------|
| `DB_HOST` | RDS instance endpoint |
| `DB_NAME` | Database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |

---

## 🗄️ Database

The schema and data are in a separate repository:
👉 [OnePiece_db](https://github.com/ValentinStanisci/OnePiece_db)

---

## 👨‍💻 Author

**Valentin Stanisci** — Backend / Data Engineering  
Open to opportunities · [GitHub](https://github.com/ValentinStanisci)