import Link from "next/link"
import { Droplet, ArrowLeft } from "lucide-react"

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Droplet className="h-7 w-7 text-primary" />
            <span className="text-lg font-bold text-foreground">BloodLink Kenya</span>
          </div>
          <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Home
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground mb-8 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>

        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-3">Privacy Policy</h1>
          <p className="text-sm text-muted-foreground mb-8">Last updated: September 30, 2025</p>

          <div className="prose prose-neutral dark:prose-invert max-w-none">
            <section className="mb-8">
              <h2 className="text-xl font-bold text-foreground mb-3">What We Do</h2>
              <p className="text-muted-foreground leading-relaxed">
                BloodLink Kenya connects blood donors with people who need urgent blood in Kenya. That's it.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-xl font-bold text-foreground mb-3">Data We Collect</h2>
              <p className="text-muted-foreground leading-relaxed mb-3">
                We only collect the minimum information needed to connect donors with recipients:
              </p>
              <ul className="space-y-2 mb-3">
                <li className="text-muted-foreground">
                  <strong className="text-foreground">Name</strong> - To identify users
                </li>
                <li className="text-muted-foreground">
                  <strong className="text-foreground">Phone Number</strong> - To enable direct communication
                </li>
                <li className="text-muted-foreground">
                  <strong className="text-foreground">Location</strong> - To match nearby donors with recipients
                </li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-xl font-bold text-foreground mb-3">How We Use Your Data</h2>
              <p className="text-muted-foreground leading-relaxed">
                Your data is used only to link blood donors with people who need urgent blood. We connect you with
                matched users so you can coordinate blood donations directly.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-xl font-bold text-foreground mb-3">Data Sharing</h2>
              <p className="text-muted-foreground leading-relaxed font-semibold">
                We do not share your data with third parties.
              </p>
              <p className="text-muted-foreground leading-relaxed mt-2">
                Your information is only shared between matched donors and recipients within our platform for emergency
                coordination.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-xl font-bold text-foreground mb-3">Free Service</h2>
              <p className="text-muted-foreground leading-relaxed">
                BloodLink Kenya is completely free to use. We do not collect any payment information or process any
                financial transactions.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-bold text-foreground mb-3">Questions?</h2>
              <p className="text-muted-foreground leading-relaxed">
                If you have questions about this privacy policy, please contact us.
              </p>
            </section>
          </div>
        </div>
      </div>

      <footer className="border-t border-border mt-16">
        <div className="container mx-auto px-4 py-6 flex items-center justify-between">
          <span className="text-sm text-muted-foreground">© 2025 BloodLink Kenya</span>
          <Link href="/privacy" className="text-sm text-foreground font-medium">
            Privacy Policy
          </Link>
        </div>
      </footer>
    </div>
  )
}
