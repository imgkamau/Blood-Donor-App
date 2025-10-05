// Using node-postgres for Railway PostgreSQL connection
import { Pool } from 'pg'

let pool: Pool | null = null

function getPool() {
  if (!pool) {
    const databaseUrl = process.env.DATABASE_URL
    if (!databaseUrl) {
      throw new Error("DATABASE_URL environment variable is not set. Please add it in Vercel Environment Variables.")
    }
    pool = new Pool({
      connectionString: databaseUrl,
      ssl: {
        rejectUnauthorized: false
      },
      // Serverless-friendly settings
      max: 20, // Maximum connections in pool
      idleTimeoutMillis: 30000, // Close idle connections after 30s
      connectionTimeoutMillis: 10000, // 10s connection timeout
    })
    
    // Handle connection errors
    pool.on('error', (err) => {
      console.error('Unexpected database pool error:', err)
    })
  }
  return pool
}

async function query(text: string, params?: any[]) {
  try {
    const pool = getPool()
    const result = await pool.query(text, params)
    return result.rows
  } catch (error) {
    console.error('Database query error:', error)
    throw error
  }
}

// Helper function to get donor statistics
export async function getDonorStats() {
  // Use Railway backend API instead of direct database connection
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://blood-donor-app-production-aa1d.up.railway.app'
  
  try {
    const response = await fetch(`${apiUrl}/api/v1/admin/stats`, {
      cache: 'no-store' // Disable caching for fresh data
    })
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching donor stats from API:', error)
    throw error
  }
}

// Helper function to get all donors with optional filters
export async function getDonors(filters?: {
  search?: string
  bloodType?: string
}) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://blood-donor-app-production-aa1d.up.railway.app'
  
  const params = new URLSearchParams()
  if (filters?.search) params.append('search', filters.search)
  if (filters?.bloodType) params.append('blood_type', filters.bloodType)
  
  try {
    const response = await fetch(`${apiUrl}/api/v1/admin/donors?${params.toString()}`, {
      cache: 'no-store'
    })
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching donors from API:', error)
    throw error
  }
}

// Helper function to get search activity
export async function getSearchActivity(filters?: {
  bloodType?: string
  dateFrom?: string
  dateTo?: string
}) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://blood-donor-app-production-aa1d.up.railway.app'
  
  const params = new URLSearchParams()
  if (filters?.bloodType) params.append('blood_type', filters.bloodType)
  if (filters?.dateFrom) params.append('date_from', filters.dateFrom)
  if (filters?.dateTo) params.append('date_to', filters.dateTo)
  
  try {
    const response = await fetch(`${apiUrl}/api/v1/admin/search-activity?${params.toString()}`, {
      cache: 'no-store'
    })
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching search activity from API:', error)
    return []
  }
}
