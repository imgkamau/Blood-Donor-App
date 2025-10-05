# Blood Donor Admin Portal

A Next.js admin dashboard for managing the Blood Donor App, connected to Railway PostgreSQL database.

## Features

- 📊 **Dashboard** - Overview of total donors, searches, and registrations
- 👥 **Donor Management** - View, search, and filter registered donors
- 🔍 **Search Activity** - Monitor blood search requests and detect abuse
- 🔐 **Simple Authentication** - Password-protected portal
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- ⚡ **Real-time Data** - Queries production database directly

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **UI:** shadcn/ui + Tailwind CSS
- **Database:** Neon SDK (compatible with PostgreSQL)
- **Deployment:** Vercel
- **Backend:** Railway PostgreSQL

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
# or
pnpm install
```

### 2. Setup Environment Variables

Create `.env.local`:

```env
DATABASE_URL=postgresql://postgres:password@host:port/railway
ADMIN_PASSWORD=admin123
```

See [ENV_SETUP.md](./ENV_SETUP.md) for detailed instructions.

### 3. Run Development Server

```bash
npm run dev
# or
pnpm dev
```

Open [http://localhost:3000/admin](http://localhost:3000/admin)

## Deployment

### Deploy to Vercel

1. Push code to GitHub
2. Import project to Vercel
3. Set root directory to `frontend`
4. Add environment variables:
   - `DATABASE_URL` (Railway public connection string)
   - `ADMIN_PASSWORD` (optional)
5. Deploy!

See [ENV_SETUP.md](./ENV_SETUP.md) for step-by-step guide.

## Project Structure

```
frontend/
├── app/
│   ├── admin/              # Admin portal pages
│   │   ├── page.tsx        # Login page
│   │   ├── dashboard/      # Dashboard page
│   │   ├── donors/         # Donors management
│   │   └── activity/       # Search activity logs
│   ├── api/                # API routes
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Landing page
├── components/
│   └── ui/                 # shadcn/ui components
├── lib/
│   ├── db.ts               # Database queries
│   └── utils.ts            # Utilities
├── public/                 # Static assets
└── README.md               # This file
```

## Database Schema

The portal queries these tables:

### `public.blood`
- Donor information
- Blood types, locations, availability
- Registration timestamps

### `public.search_logs`
- Search activity tracking
- Blood type requests
- IP addresses, timestamps
- Results count

## Admin Features

### Dashboard
- Total donors count
- Donors by blood type distribution
- Recent registrations (last 5)
- Total searches count
- Today's new registrations

### Donors Page
- Searchable donor list
- Filter by blood type
- Export to CSV (coming soon)
- View donor details
- Phone numbers, locations, status

### Activity Page
- Last 100 searches
- Filter by blood type, date range
- View search locations
- Detect suspicious IPs
- Results count per search

## Security

- ✅ Password-protected admin portal
- ✅ Session-based authentication
- ✅ Phone numbers visible to admin (for management)
- ✅ Separate from public API (no direct access)
- ✅ Environment variables for sensitive data

**Default password:** `admin123`
**⚠️ Change this in production!**

## Customization

### Change Admin Password

Update environment variable:
```env
ADMIN_PASSWORD=your-new-password
```

Or modify `app/admin/page.tsx`:
```typescript
if (password === "your-new-password") {
  // ...
}
```

### Add New Pages

1. Create new folder in `app/admin/`
2. Add `page.tsx`
3. Add navigation link in header

### Modify Queries

Edit `lib/db.ts`:
```typescript
export async function getCustomData() {
  const sql = getSQL()
  return await sql`SELECT * FROM public.your_table`
}
```

## Troubleshooting

### Build Errors

```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

### Database Connection Issues

1. Check `DATABASE_URL` is set correctly
2. Use Railway's **public** connection string
3. Verify database is accessible from Vercel

### Authentication Not Working

1. Check `ADMIN_PASSWORD` environment variable
2. Clear browser cookies/session
3. Try incognito/private mode

## Development

### Add New UI Component

```bash
npx shadcn-ui@latest add button
```

### Run Linter

```bash
npm run lint
```

### Build for Production

```bash
npm run build
npm start
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check [ENV_SETUP.md](./ENV_SETUP.md)
2. Review error logs
3. Open GitHub issue

## Related

- **Main App:** Flutter Blood Donor App
- **Backend:** FastAPI on Railway
- **Database:** Railway PostgreSQL

