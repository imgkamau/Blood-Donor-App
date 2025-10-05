import { NextResponse } from "next/server"
import { cookies } from "next/headers"
import { getDonors } from "@/lib/db"

export async function GET() {
  const cookieStore = await cookies()
  const session = cookieStore.get("admin_session")

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }

  const donors = await getDonors()

  // Generate CSV
  const headers = ["Name", "Phone", "Blood Type", "Location", "City", "Registered"]
  const rows = donors.map((donor: any) => [
    donor.first_name,
    donor.phone,
    donor.blood_type,
    donor.location,
    donor.city || "",
    new Date(donor.created_at).toLocaleDateString(),
  ])

  const csv = [headers.join(","), ...rows.map((row) => row.map((cell) => `"${cell}"`).join(","))].join("\n")

  return new NextResponse(csv, {
    headers: {
      "Content-Type": "text/csv",
      "Content-Disposition": 'attachment; filename="donors.csv"',
    },
  })
}
