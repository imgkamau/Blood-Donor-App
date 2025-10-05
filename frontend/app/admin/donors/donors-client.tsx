"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Search, Download } from "lucide-react"

interface Donor {
  id: number
  first_name: string
  phone: string
  blood_type: string
  location: string
  city: string | null
  created_at: string
}

export default function DonorsClient({ donors }: { donors: Donor[] }) {
  const [searchTerm, setSearchTerm] = useState("")
  const [bloodTypeFilter, setBloodTypeFilter] = useState("all")

  const handleExport = async () => {
    const response = await fetch("/api/admin/export-donors")
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "donors.csv"
    a.click()
  }

  const filteredDonors = donors.filter((donor) => {
    const matchesSearch =
      donor.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      donor.phone.includes(searchTerm) ||
      donor.location.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesBloodType = bloodTypeFilter === "all" || donor.blood_type === bloodTypeFilter
    return matchesSearch && matchesBloodType
  })

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Registered Donors</CardTitle>
            <CardDescription>Search and manage blood donors</CardDescription>
          </div>
          <Button onClick={handleExport} variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by name, phone, or location..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <select
            value={bloodTypeFilter}
            onChange={(e) => setBloodTypeFilter(e.target.value)}
            className="px-3 py-2 border rounded-md bg-background"
          >
            <option value="all">All Blood Types</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
          </select>
        </div>

        {/* Results count */}
        <p className="text-sm text-muted-foreground mb-4">
          Showing {filteredDonors.length} of {donors.length} donors
        </p>

        {/* Table */}
        <div className="border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left p-3 font-medium">Name</th>
                  <th className="text-left p-3 font-medium">Phone</th>
                  <th className="text-left p-3 font-medium">Blood Type</th>
                  <th className="text-left p-3 font-medium">Location</th>
                  <th className="text-left p-3 font-medium">Registered</th>
                </tr>
              </thead>
              <tbody>
                {filteredDonors.map((donor) => (
                  <tr key={donor.id} className="border-t hover:bg-muted/50">
                    <td className="p-3">{donor.first_name}</td>
                    <td className="p-3">{donor.phone}</td>
                    <td className="p-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                        {donor.blood_type}
                      </span>
                    </td>
                    <td className="p-3">{donor.location}</td>
                    <td className="p-3 text-muted-foreground">{new Date(donor.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
