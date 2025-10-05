// Using node-postgres for Railway PostgreSQL connection
import { Pool } from 'pg'

let pool: Pool | null = null

function getPool() {
  if (!pool) {
    const databaseUrl = process.env.DATABASE_URL
    if (!databaseUrl) {
      throw new Error("DATABASE_URL environment variable is not set")
    }
    pool = new Pool({
      connectionString: databaseUrl,
      ssl: {
        rejectUnauthorized: false
      }
    })
  }
  return pool
}

async function query(text: string, params?: any[]) {
  const pool = getPool()
  const result = await pool.query(text, params)
  return result.rows
}

// Helper function to get donor statistics
export async function getDonorStats() {
  const totalDonorsResult = await query('SELECT COUNT(*) as count FROM public.blood')
  const totalDonors = totalDonorsResult[0]

  const donorsByBloodType = await query(`
    SELECT blood_type, COUNT(*) as count 
    FROM public.blood 
    GROUP BY blood_type 
    ORDER BY blood_type
  `)

  const recentDonors = await query(`
    SELECT id, first_name, blood_type, city, latitude, longitude, created_at
    FROM public.blood 
    ORDER BY created_at DESC 
    LIMIT 5
  `)

  const searchCountResult = await query('SELECT COUNT(*) as count FROM public.search_logs')
  const searchCount = searchCountResult[0]

  const todayRegistrationsResult = await query(`
    SELECT COUNT(*) as count 
    FROM public.blood 
    WHERE created_at >= CURRENT_DATE
  `)
  const todayRegistrations = todayRegistrationsResult[0]

  const topCities = await query(`
    SELECT city, COUNT(*) as count 
    FROM public.blood 
    WHERE city IS NOT NULL
    GROUP BY city 
    ORDER BY count DESC 
    LIMIT 5
  `)

  return {
    totalDonors: Number(totalDonors.count),
    donorsByBloodType,
    recentDonors: recentDonors.map((donor: any) => ({
      id: donor.id,
      first_name: donor.first_name,
      blood_type: donor.blood_type,
      location: donor.city || `${donor.latitude}, ${donor.longitude}`,
      created_at: donor.created_at
    })),
    searchCount: Number(searchCount?.count || 0),
    todayRegistrations: Number(todayRegistrations.count),
    topCities,
  }
}

// Helper function to get all donors with optional filters
export async function getDonors(filters?: {
  search?: string
  bloodType?: string
}) {
  let queryText = `
    SELECT id, first_name, phone_number, blood_type, city, latitude, longitude, 
           is_verified, is_available, created_at 
    FROM public.blood 
    WHERE 1=1
  `
  const params: any[] = []

  if (filters?.search) {
    queryText += ` AND (first_name ILIKE $${params.length + 1} OR phone_number ILIKE $${params.length + 1} OR city ILIKE $${params.length + 1})`
    params.push(`%${filters.search}%`)
  }

  if (filters?.bloodType && filters.bloodType !== "all") {
    queryText += ` AND blood_type = $${params.length + 1}`
    params.push(filters.bloodType)
  }

  queryText += " ORDER BY created_at DESC"

  const results = await query(queryText, params)
  
  return results.map((donor: any) => ({
    id: donor.id,
    first_name: donor.first_name,
    phone: donor.phone_number,
    blood_type: donor.blood_type,
    location: donor.city || `${donor.latitude}, ${donor.longitude}`,
    is_verified: donor.is_verified,
    is_available: donor.is_available,
    created_at: donor.created_at
  }))
}

// Helper function to get search activity
export async function getSearchActivity(filters?: {
  bloodType?: string
  dateFrom?: string
  dateTo?: string
}) {
  let queryText = `
    SELECT id, blood_type, latitude, longitude, radius_km, 
           results_count, client_ip, searched_at 
    FROM public.search_logs 
    WHERE 1=1
  `
  const params: any[] = []

  if (filters?.bloodType && filters.bloodType !== "all") {
    queryText += ` AND blood_type = $${params.length + 1}`
    params.push(filters.bloodType)
  }

  if (filters?.dateFrom) {
    queryText += ` AND searched_at >= $${params.length + 1}`
    params.push(filters.dateFrom)
  }

  if (filters?.dateTo) {
    queryText += ` AND searched_at <= $${params.length + 1}`
    params.push(filters.dateTo)
  }

  queryText += " ORDER BY searched_at DESC LIMIT 100"

  try {
    return await query(queryText, params)
  } catch (error) {
    // If table doesn't exist yet, return empty array
    console.error("Error fetching search activity:", error)
    return []
  }
}
