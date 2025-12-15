# Deployment Guide

## Overview

This guide covers deployment options for the E-commerce Telegram Bot system.

## Deployment Options

### Option 1: Local Deployment (Development)

Already configured. Run on your local machine:

```bash
# Terminal 1
cd backend && npm start

# Terminal 2
cd bot && python telegram_bot.py
```

---

### Option 2: Cloud Deployment (Production)

#### Azure App Service Deployment

**Backend Deployment:**

1. Create Azure Web App (Node.js runtime)
2. Push code to GitHub
3. Enable continuous deployment
4. Set environment variables:
   ```
   NODE_ENV=production
   PORT=80
   ```

**Bot Deployment:**

1. Create Azure Web App (Python runtime)
2. Push code to GitHub
3. Enable continuous deployment
4. Update BACKEND_URL to cloud endpoint

#### AWS Elastic Beanstalk

**Backend:**
```bash
# Initialize
eb init -p "Node.js 16" ecommerce-api

# Deploy
eb create prod-environment
eb deploy
```

**Bot:**
```bash
# Initialize
eb init -p "Python 3.9" ecommerce-bot

# Deploy
eb create prod-bot
eb deploy
```

#### Heroku Deployment

**Backend:**

1. Create Procfile:
```
web: npm start
```

2. Deploy:
```bash
heroku create ecommerce-api
git push heroku main
```

**Bot:**

1. Create Procfile:
```
worker: python telegram_bot.py
```

2. Deploy:
```bash
heroku create ecommerce-bot
git push heroku main
```

---

### Option 3: Docker Containerization

#### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

#### Bot Dockerfile

Create `bot/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "telegram_bot.py"]
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production

  bot:
    build: ./bot
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:3000/api
      - BOT_TOKEN=${BOT_TOKEN}

networks:
  default:
    driver: bridge
```

#### Build and Run:

```bash
# Build images
docker-compose build

# Run services
docker-compose up

# Stop services
docker-compose down
```

---

### Option 4: Kubernetes Deployment

#### Backend Deployment YAML

Create `backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: ecommerce-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: backend
```

#### Deploy:

```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f bot-deployment.yaml
```

---

## Database Migration (For Production)

### From In-Memory to MongoDB

1. Install MongoDB driver:
```bash
npm install mongoose
```

2. Update backend models:

```javascript
const userSchema = new mongoose.Schema({
  telegram_id: String,
  username: String,
  first_name: String,
  cart: Array,
  orders: Array,
  created_at: Date
});

const User = mongoose.model('User', userSchema);
```

3. Replace Maps with database queries:

```javascript
// Before (In-Memory)
const user = users.get(telegram_id);

// After (MongoDB)
const user = await User.findOne({ telegram_id });
```

### Connection String

```javascript
mongoose.connect(process.env.MONGODB_URI);
```

---

## Environment Variables

### Backend (.env file)

```
NODE_ENV=production
PORT=3000
DATABASE_URL=mongodb://connection_string
ALLOWED_ORIGINS=https://yourdomain.com
LOG_LEVEL=info
```

### Bot (.env file)

```
BOT_TOKEN=your_actual_token
BACKEND_URL=https://api.yourdomain.com
LOG_LEVEL=info
WEBHOOK_URL=https://bot.yourdomain.com
```

---

## Security Checklist

- [ ] Use HTTPS for all connections
- [ ] Add authentication to API endpoints
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly
- [ ] Add rate limiting
- [ ] Implement request validation
- [ ] Use strong bot token security
- [ ] Enable logging and monitoring
- [ ] Regular security updates

---

## Monitoring & Logging

### Application Insights (Azure)

```javascript
const appInsights = require('applicationinsights');
appInsights.setup(process.env.APPINSIGHTS_CONNECTION_STRING);
appInsights.start();
```

### CloudWatch (AWS)

```javascript
const winston = require('winston');
const WinstonCloudWatch = require('winston-cloudwatch');

logger.add(new WinstonCloudWatch({
  logGroupName: '/ecommerce/backend',
  logStreamName: 'production'
}));
```

### PM2 Process Manager

```bash
# Install
npm install -g pm2

# Start
pm2 start server.js --name "backend"

# Monitor
pm2 monit
```

---

## Auto-Scaling Configuration

### Azure App Service

```bash
# Create auto-scale rule
az monitor metrics alert create \
  --resource-group myResourceGroup \
  --resource-type Microsoft.Web/serverfarms \
  --name cpu-alert
```

### AWS Elastic Beanstalk

```bash
# Configure auto-scaling
eb scale 3
```

---

## Backup & Recovery

### Database Backup

```bash
# MongoDB backup
mongodump --uri mongodb://connection_string

# Restore
mongorestore dump/
```

### Configuration Backup

- Use version control (Git)
- Store secrets in key vault
- Regular snapshot backups

---

## Performance Optimization

### Backend

1. Enable gzip compression:
```javascript
const compression = require('compression');
app.use(compression());
```

2. Implement caching:
```javascript
const redis = require('redis');
const cache = redis.createClient();
```

3. Database indexing for MongoDB

### Bot

1. Implement message batching
2. Cache product list
3. Optimize image sizes
4. Use webhook instead of polling

---

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Backend
      run: cd backend && npm install && npm test
    
    - name: Deploy Backend
      run: npm run deploy
    
    - name: Build Bot
      run: cd bot && pip install -r requirements.txt
    
    - name: Deploy Bot
      run: python -m pytest tests/
```

---

## Troubleshooting Deployment

### Common Issues

**502 Bad Gateway:**
- Backend not running
- Port not configured correctly
- Connection timeout

**Bot not responding:**
- Wrong backend URL
- Bot token expired
- Network connectivity issues

**Database connection errors:**
- Connection string incorrect
- Database not running
- Firewall blocking access

---

## Rollback Procedures

```bash
# Git rollback
git revert <commit-hash>
git push

# Docker rollback
docker pull image:previous-tag
docker-compose up
```

---

## Cost Estimation

### Monthly Costs (Production)

| Service | Tier | Cost |
|---------|------|------|
| App Service | B2 | $55 |
| Database | M2 | $50 |
| Bandwidth | - | $10 |
| Monitoring | - | $5 |
| **Total** | | **$120** |

---

## Support & Maintenance

- Regular security updates
- Monitor performance metrics
- Update dependencies monthly
- Regular database maintenance
- Backup verification

---

For detailed cloud provider documentation:
- [Azure App Service](https://docs.microsoft.com/azure/app-service)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk)
- [Docker Documentation](https://docs.docker.com)
- [Kubernetes](https://kubernetes.io/docs)

---

**Deployment Ready!** 🚀
