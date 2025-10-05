"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

interface SearchActivity {
  id: number
  blood_type: string
  location: string
  searched_at: string
}

export default function ActivityClient({ searches }: { searches: SearchActivity[] }) {
  const [bloodTypeFilter, setBloodTypeFilter] = useState("all")
  const [dateFilter, setDateFilter] = useState("")

  const filteredSearches = searches.filter((search) => {
    const matchesBloodType = bloodTypeFilter === "all" || search.blood_type === bloodTypeFilter
    const searchDate = new Date(search.searched_at).toISOString().split("T")[0]
    const matchesDate = !dateFilter || searchDate === dateFilter
    return matchesBloodType && matchesDate
  })

  return (
    <Card>
      <CardHeader>
        <CardTitle>Search Activity Log</CardTitle>
        <CardDescription>Recent blood search requests (Last 100)</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
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
          <Input type="date" value={dateFilter} onChange={(e) => setDateFilter(e.target.value)} className="md:w-auto" />
        </div>

        {/* Results count */}
        <p className="text-sm text-muted-foreground mb-4">
          Showing {filteredSearches.length} of {searches.length} searches
        </p>

        {/* Table */}
        <div className="border rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-muted">
                <tr>
                  <th className="text-left p-3 font-medium">Blood Type</th>
                  <th className="text-left p-3 font-medium">Location</th>
                  <th className="text-left p-3 font-medium">Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {filteredSearches.map((search) => (
                  <tr key={search.id} className="border-t hover:bg-muted/50">
                    <td className="p-3">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                        {search.blood_type}
                      </span>
                    </td>
                    <td className="p-3">{search.location}</td>
                    <td className="p-3 text-muted-foreground">{new Date(search.searched_at).toLocaleString()}</td>
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
