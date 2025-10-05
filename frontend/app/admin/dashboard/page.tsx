import { redirect } from "next/navigation"
import { cookies } from "next/headers"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Users, Search, Activity, Droplet } from "lucide-react"
import { getDonorStats } from "@/lib/db"

async function logout() {
  "use server"
  const cookieStore = await cookies()
  cookieStore.delete("admin_session")
  redirect("/admin")
}

export default async function AdminDashboard() {
  const cookieStore = await cookies()
  const session = cookieStore.get("admin_session")

  if (!session) {
    redirect("/admin")
  }

  const stats = await getDonorStats()

  // Transform blood type data for display
  const bloodTypeMap: Record<string, number> = {}
  stats.donorsByBloodType.forEach((item: any) => {
    bloodTypeMap[item.blood_type] = Number(item.count)
  })

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">Blood Donor Admin Portal</h1>
            <p className="text-sm text-muted-foreground">Manage donors and track activity</p>
          </div>
          <form action={logout}>
            <Button variant="outline" type="submit">
              Logout
            </Button>
          </form>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b">
        <div className="container mx-auto px-4">
          <div className="flex gap-6 py-3">
            <Link href="/admin/dashboard" className="text-sm font-medium text-primary">
              Dashboard
            </Link>
            <Link href="/admin/donors" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Donors
            </Link>
            <Link href="/admin/activity" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Search Activity
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Key Metrics */}
        <div className="grid gap-4 md:grid-cols-3 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Donors</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalDonors}</div>
              <p className="text-xs text-muted-foreground">Registered blood donors</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Searches</CardTitle>
              <Search className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.searchCount}</div>
              <p className="text-xs text-muted-foreground">Blood search requests</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Today's Registrations</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.todayRegistrations}</div>
              <p className="text-xs text-muted-foreground">New donors today</p>
            </CardContent>
          </Card>
        </div>

        {/* Donors by Blood Type */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Donors by Blood Type</CardTitle>
            <CardDescription>Distribution of registered donors</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"].map((type) => (
                <div key={type} className="flex items-center gap-3 p-3 border rounded-lg">
                  <Droplet className="h-5 w-5 text-primary" />
                  <div>
                    <div className="font-bold">{type}</div>
                    <div className="text-sm text-muted-foreground">{bloodTypeMap[type] || 0} donors</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Registrations */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Registrations</CardTitle>
            <CardDescription>Latest donor sign-ups</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {stats.recentDonors.map((donor: any) => (
                <div key={donor.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                      <Droplet className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium">{donor.first_name}</div>
                      <div className="text-sm text-muted-foreground">{donor.location}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">{donor.blood_type}</div>
                    <div className="text-sm text-muted-foreground">
                      {new Date(donor.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
