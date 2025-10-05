# Environment Setup for Vercel Deployment

## Required Environment Variables

When deploying to Vercel, add these environment variables in your project settings:

### 1. DATABASE_URL
```
postgresql://postgres:password@host:port/railway
```

**Important:** For Vercel to access Railway, you need to use the **PUBLIC** connection string from Railway (not the internal one).

Get it from Railway:
1. Go to your Railway project
2. Click on your PostgreSQL database
3. Go to "Connect" tab
4. Copy the **Public Network** connection string (not internal)

It should look like:
```
postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:12345/railway
```

### 2. ADMIN_PASSWORD (Optional)
```
your-secure-password-here
```

Default is `admin123` - change this for production!

---

## Vercel Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add frontend/
   git commit -m "Add admin portal with Railway integration"
   git push origin main
   ```

2. **Import to Vercel**
   - Go to vercel.com
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select the `frontend` folder as root directory

3. **Configure Environment Variables**
   - In Vercel project settings → Environment Variables
   - Add `DATABASE_URL` with Railway's PUBLIC connection string
   - Add `ADMIN_PASSWORD` (optional)

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Access your admin portal at: `your-project.vercel.app/admin`

---

## Local Development

1. Create `.env.local` in the `frontend` directory:
   ```env
   DATABASE_URL=postgresql://postgres:YriFkwdSDCFRreklJsMUZnXjJKJVusff@monorail.proxy.rlwy.net:12345/railway
   ADMIN_PASSWORD=admin123
   ```

2. Install dependencies:
   ```bash
   cd frontend
   npm install
   # or
   pnpm install
   ```

3. Run development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

4. Open browser: `http://localhost:3000/admin`

---

## Troubleshooting

### "DATABASE_URL environment variable is not set"
- Make sure you added the environment variable in Vercel settings
- Redeploy after adding variables

### "could not translate host name"
- You're using the internal Railway hostname
- Switch to the **Public Network** connection string from Railway

### "Connection timeout"
- Railway's public hostname might be slow on first connection
- Wait a few seconds and refresh

### "Authentication failed"
- Check your Railway database password is correct
- Ensure the connection string is complete and properly formatted

---

## Security Notes

1. **Never commit** `.env.local` to Git (it's gitignored by default)
2. **Change admin password** from default `admin123`
3. **Use Railway's public hostname** for external connections
4. **Enable Railway's** IP whitelist if you want extra security

---

## What's Connected

Frontend (Vercel) → Railway PostgreSQL Database

The frontend queries:
- `public.blood` - Donor data
- `public.search_logs` - Search activity tracking

Same database used by your Flutter app backend!

