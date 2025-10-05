import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Droplet, Heart } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Droplet className="h-7 w-7 text-primary" />
            <span className="text-lg font-bold text-foreground">BloodLink Kenya</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Privacy
            </Link>
            <Link href="/admin" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Admin
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-6 text-balance">
              Linking Blood Donors with Urgent Blood Appeals in Kenya
            </h1>
            <p className="text-lg text-muted-foreground mb-8 text-pretty">
              We connect blood donors with people who need urgent blood. Simple, fast, and life-saving.
            </p>
            <p className="text-base text-primary font-semibold mb-8">100% Free. No charges. No payments.</p>
            <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Heart className="mr-2 h-5 w-5" />
              Get Started
            </Button>
          </div>
        </div>
      </main>

      <footer className="border-t border-border">
        <div className="container mx-auto px-4 py-6 flex items-center justify-between">
          <span className="text-sm text-muted-foreground">© 2025 BloodLink Kenya</span>
          <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Privacy Policy
          </Link>
        </div>
      </footer>
    </div>
  )
}
