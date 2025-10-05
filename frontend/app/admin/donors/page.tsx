import { redirect } from "next/navigation"
import { cookies } from "next/headers"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { getDonors } from "@/lib/db"
import DonorsClient from "./donors-client"

async function logout() {
  "use server"
  const cookieStore = await cookies()
  cookieStore.delete("admin_session")
  redirect("/admin")
}

export default async function DonorsPage() {
  const cookieStore = await cookies()
  const session = cookieStore.get("admin_session")

  if (!session) {
    redirect("/admin")
  }

  const donors = await getDonors()

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
            <Link href="/admin/dashboard" className="text-sm font-medium text-muted-foreground hover:text-foreground">
              Dashboard
            </Link>
            <Link href="/admin/donors" className="text-sm font-medium text-primary">
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
        <DonorsClient donors={donors} />
      </main>
    </div>
  )
}
