import { NextResponse } from 'next/server'
import { Pool } from 'pg'

export async function GET() {
  try {
    const databaseUrl = process.env.DATABASE_URL
    
    if (!databaseUrl) {
      return NextResponse.json({
        error: 'DATABASE_URL not set',
        env: process.env.NODE_ENV
      }, { status: 500 })
    }

    // Parse and mask the URL for security
    const urlParts = databaseUrl.match(/postgresql:\/\/([^:]+):([^@]+)@([^:]+):(\d+)\/(.+)/)
    const maskedUrl = urlParts 
      ? `postgresql://${urlParts[1]}:***@${urlParts[3]}:${urlParts[4]}/${urlParts[5]}`
      : 'Invalid URL format'

    // Try to connect
    const pool = new Pool({
      connectionString: databaseUrl,
      ssl: {
        rejectUnauthorized: false
      },
      connectionTimeoutMillis: 5000,
    })

    const result = await pool.query('SELECT NOW() as time, current_database() as db')
    await pool.end()

    return NextResponse.json({
      success: true,
      maskedUrl,
      connection: 'OK',
      time: result.rows[0].time,
      database: result.rows[0].db,
      message: 'Database connection successful!'
    })

  } catch (error: any) {
    return NextResponse.json({
      error: error.message,
      code: error.code,
      errno: error.errno,
      syscall: error.syscall,
      details: 'Failed to connect to Railway PostgreSQL from Vercel'
    }, { status: 500 })
  }
}

