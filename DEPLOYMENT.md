# Open DIO Deployment Guide

This guide covers deploying the Open DIO application (frontend and backend).

## Architecture

- **Frontend**: React app deployed to GitHub Pages (static hosting)
- **Backend**: Python FastAPI deployed to cloud service (Render, Railway, etc.)

## Backend Deployment

### Option 1: Render.com (Recommended - Free Tier Available)

Render offers a generous free tier perfect for this project.

#### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `kelaxten/DIO-v3`
   - Select branch: `main`

3. **Configure Service**
   - **Name**: `open-dio-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users (e.g., Oregon)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables** (Optional)
   - `PYTHON_VERSION`: `3.11.0`
   - Add any custom CORS origins if needed

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your service URL: `https://open-dio-api.onrender.com`

6. **Verify Deployment**
   ```bash
   curl https://open-dio-api.onrender.com/health
   # Should return: {"status":"healthy","version":"1.0.0","model":"DIO v2.0"}
   ```

#### Important Notes:
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to paid tier ($7/mo) for always-on service

### Option 2: Railway.app (Alternative)

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project" → "Deploy from GitHub repo"
3. Select `kelaxten/DIO-v3`
4. Configure:
   - **Root Directory**: `/backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Railway auto-detects Python and installs dependencies
6. Note your deployment URL

### Option 3: Docker Deployment (Fly.io, AWS, GCP, etc.)

Build and deploy using the provided Dockerfile:

```bash
# Build image
cd backend
docker build -t open-dio-api .

# Test locally
docker run -p 8000:8000 open-dio-api

# Deploy to your platform (example for Fly.io)
fly launch
fly deploy
```

## Frontend Deployment

### Update API URL

Once backend is deployed, update the frontend to use the production API:

1. **Create production env file**: `open-dio-web/frontend/.env.production`
   ```env
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

2. **Rebuild frontend**:
   ```bash
   cd open-dio-web/frontend
   npm run build
   ```

3. **Commit and push**:
   ```bash
   git add .env.production
   git commit -m "Add production API URL"
   git push origin claude/update-dio-model-jcHg1
   ```

4. **Merge to main** (if on feature branch)
   - Create pull request
   - Merge to main
   - GitHub Actions will automatically deploy to GitHub Pages

### GitHub Pages Configuration

Already configured in `.github/workflows/deploy.yml`. Deployment happens automatically on push to `main`.

**Live URL**: https://kelaxten.github.io/DIO-v3/

## Testing Full Stack

After both deployments:

1. **Test Backend**:
   ```bash
   # Health check
   curl https://your-api.onrender.com/health

   # List sectors
   curl https://your-api.onrender.com/api/v1/sectors/?defense_only=true

   # Calculate impact
   curl -X POST https://your-api.onrender.com/api/v1/calculate/ \
     -H "Content-Type: application/json" \
     -d '{"sectors":[{"code":"33299A","amount":100000}],"impact_categories":["GHG","Energy","Water","Land"]}'
   ```

2. **Test Frontend**:
   - Visit https://kelaxten.github.io/DIO-v3/
   - Select a sector (e.g., "Ammunition manufacturing")
   - Enter spending amount (e.g., $100,000)
   - Click "Calculate Impact"
   - Verify results display

3. **Test Integration**:
   - Open browser console (F12)
   - Check for any CORS errors
   - Verify API calls succeed
   - Confirm data loads correctly

## Monitoring

### Backend Health
- Render Dashboard: Monitor requests, errors, logs
- Health endpoint: `GET /health`
- API docs: `GET /docs` (Swagger UI)

### Frontend
- GitHub Actions: Check deployment status
- Browser Console: Check for errors
- Network tab: Verify API calls

## Troubleshooting

### CORS Errors
If frontend can't call backend:
1. Verify CORS origins in backend `app/main.py`
2. Add your frontend URL to `allow_origins` list:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "https://kelaxten.github.io",
       "https://your-custom-domain.com"
   ]
   ```

### Backend Not Responding
- Check Render logs for errors
- Verify environment variables set correctly
- Ensure PORT is bound correctly: `--port $PORT`

### Frontend Not Loading Data
- Check browser console for errors
- Verify `.env.production` has correct API URL
- Check Network tab to see actual requests
- Ensure backend is deployed and healthy

## Scaling Considerations

### Current Setup (Free Tier)
- Backend: Render free tier (512MB RAM, sleeps after 15min)
- Frontend: GitHub Pages (free, unlimited bandwidth)
- **Cost**: $0/month
- **Suitable for**: Demos, prototypes, light usage

### Production Setup
- Backend: Render Starter ($7/mo) or Pro ($25/mo)
- Frontend: GitHub Pages (still free) or Cloudflare Pages
- Add CDN for faster global access
- Add monitoring (Sentry, LogRocket)
- **Cost**: $7-25/month
- **Suitable for**: Public tools, research projects

### High-Scale Setup
- Backend: Multiple instances, load balancer
- Database: PostgreSQL for caching calculations
- CDN: Cloudflare or AWS CloudFront
- **Cost**: $50-200/month
- **Suitable for**: High-traffic applications

## Next Steps

After successful deployment:
1. [ ] Add analytics (Google Analytics, Plausible)
2. [ ] Set up error monitoring (Sentry)
3. [ ] Add rate limiting to API
4. [ ] Implement result caching
5. [ ] Create CSV upload feature
6. [ ] Add PDF export functionality
7. [ ] Integrate all 246 sectors into frontend UI
8. [ ] Add comparison to Costs of War estimates
