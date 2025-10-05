# Admin Password Setup Guide

The admin portal now uses a secure environment variable for authentication.

## Setting Your Admin Password

### Option 1: Via Vercel Dashboard (Recommended)

1. Go to **Vercel Dashboard**: https://vercel.com/dashboard
2. Select your **blood-donor-app** project
3. Go to **Settings** → **Environment Variables**
4. Add a new variable:
   ```
   Name: ADMIN_PASSWORD
   Value: [Your secure password here]
   Environment: Production, Preview, Development (select all)
   ```
5. Click **Save**
6. **Redeploy** your app (Deployments → Latest → "..." → Redeploy)

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Link to your project
vercel link

# Set the environment variable
vercel env add ADMIN_PASSWORD

# When prompted:
# - Enter your secure password
# - Select: Production, Preview, Development (all environments)

# Redeploy
vercel --prod
```

## Password Requirements

**Choose a strong password:**
- ✅ At least 12 characters
- ✅ Mix of uppercase and lowercase
- ✅ Include numbers and symbols
- ✅ Not a common word or phrase

**Example strong passwords:**
- `BloodDonor2024!Secure`
- `K3ny@_D0n0r_P0rt@l`
- `Adm1n$Bl00d#2024`

**DO NOT USE:**
- ❌ `admin123`
- ❌ `password`
- ❌ `admin`
- ❌ Any password you use elsewhere

## For Local Development

Create a `.env.local` file in the `frontend/` directory:

```bash
cd frontend
echo "ADMIN_PASSWORD=your-secure-password-here" > .env.local
```

**Important:** `.env.local` is already in `.gitignore` and will NOT be committed to Git.

## Default Password (Development Only)

If `ADMIN_PASSWORD` is not set, the system will use:
- Default: `change-me-in-production`

**This is intentionally weak** to remind you to set a proper password in production.

## Security Notes

1. **Never commit passwords to Git**
   - Use environment variables only
   - `.env.local` is in `.gitignore`

2. **Use different passwords for different environments**
   - Development: Can be simple for testing
   - Production: Must be strong and unique

3. **Rotate passwords regularly**
   - Change password every 90 days
   - Change immediately if compromised

4. **Limit access**
   - Only share the password with authorized administrators
   - Consider implementing 2FA in the future

## Testing

After setting the password:

1. Visit: `blood-donor-app.vercel.app/admin`
2. Enter your new password
3. You should be redirected to the dashboard

If login fails:
- Check Vercel environment variables are set correctly
- Ensure you redeployed after adding the variable
- Check browser console for errors

## Future Enhancements

Consider implementing:
- [ ] Two-factor authentication (2FA)
- [ ] Email-based login with magic links
- [ ] Role-based access control (multiple admins)
- [ ] Session timeout after inactivity
- [ ] Login attempt rate limiting
- [ ] Audit logs for admin actions

## Troubleshooting

### "Invalid password" error
- Verify `ADMIN_PASSWORD` is set in Vercel
- Check for typos in the password
- Ensure you redeployed after setting the variable

### "An error occurred" message
- Check browser console for details
- Verify the API route is working: `/api/admin/verify-password`
- Check Vercel function logs

### Can't access even with correct password
- Clear browser cookies
- Try incognito/private mode
- Check that the admin session cookie is being set

## Support

If you need help:
1. Check Vercel deployment logs
2. Check browser console for errors
3. Verify environment variables are set correctly

