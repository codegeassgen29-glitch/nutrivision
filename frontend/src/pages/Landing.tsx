// The public landing page - first thing visitors see.
// Hero section, stats strip, and feature highlights,
// styled for a fitness/gym-focused audience.

import { Link } from 'react-router-dom'

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#0a0f0d] text-white">
      <nav className="flex justify-between items-center px-8 py-5 max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center text-xs font-bold text-black">
            N
          </span>
          <span className="font-semibold">NutriVision AI</span>
        </div>
        <div className="hidden sm:flex items-center gap-8 text-sm text-gray-400">
          <a href="#features" className="hover:text-white transition">Features</a>
          <a href="#how" className="hover:text-white transition">How it works</a>
        </div>
        <Link
          to="/signup"
          className="bg-emerald-400 hover:bg-emerald-300 text-black text-sm font-semibold px-4 py-2 rounded-full transition"
        >
          Open app
        </Link>
      </nav>

      <div className="max-w-7xl mx-auto px-8 pt-12 pb-20 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        <div>
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-300 bg-emerald-400/10 border border-emerald-400/20 rounded-full px-3 py-1 mb-6">
            Vision-powered nutrition
          </span>
          <h1 className="text-5xl sm:text-6xl font-bold leading-[1.05] mb-6">
            Stop guessing.<br />
            <span className="text-emerald-400">Start scanning.</span>
          </h1>
          <p className="text-gray-400 text-lg mb-8 max-w-md leading-relaxed">
            NutriVision AI reads your plate like your coach reads your lifts. Snap a photo,
            get calories and macros instantly, and see how every meal moves you toward the
            physique you are training for.
          </p>
          <div className="flex flex-wrap items-center gap-4 mb-8">
            <Link
              to="/signup"
              className="bg-emerald-400 hover:bg-emerald-300 text-black font-semibold px-6 py-3 rounded-full transition"
            >
              Try the dashboard
            </Link>
            <Link
              to="/login"
              className="border border-white/10 hover:border-white/30 text-white font-semibold px-6 py-3 rounded-full transition"
            >
              Log in
            </Link>
          </div>
        </div>

        <div className="relative">
          <div className="relative rounded-3xl overflow-hidden shadow-2xl">
            <img
              src="/hero.jpg"
              alt=""
              className="w-full aspect-[4/5] object-cover"
            />
            <div className="absolute top-4 right-4 bg-[#0f1613]/90 backdrop-blur border border-emerald-400/20 rounded-2xl px-4 py-3">
              <div className="flex items-center gap-1.5 mb-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-xs text-emerald-300 font-medium">Scanning</span>
              </div>
              <p className="text-sm font-semibold mb-1">High protein bowl</p>
              <p className="text-xs text-gray-400">520 kcal - 52g protein - 45g carbs - 15g fat</p>
            </div>
          </div>
          <div className="absolute -bottom-6 -left-6 bg-[#0f1613] border border-white/10 rounded-2xl px-5 py-3 shadow-xl">
            <p className="text-xs text-gray-500 mb-1">Today's protein</p>
            <p className="text-lg font-bold text-emerald-400">168g / 190g</p>
          </div>
        </div>
      </div>

      <div className="border-y border-white/5">
        <div className="max-w-7xl mx-auto px-8 py-10 grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">
          <Stat value="1.2s" label="Average scan time" />
          <Stat value="96%" label="Macro accuracy" />
          <Stat value="10+" label="Foods recognized" />
          <Stat value="24/7" label="AI coaching" />
        </div>
      </div>

      <div id="features" className="max-w-7xl mx-auto px-8 py-20">
        <h2 className="text-4xl font-bold mb-3">
          Everything you need to <span className="text-emerald-400">eat like an athlete</span>
        </h2>
        <p className="text-gray-500 mb-12 max-w-lg">
          No barcode hunting. No 40-tap food diaries. Just the numbers that actually
          change your training outcomes.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <FeatureCard
            icon="camera"
            title="One-snap logging"
            description="Point your camera at the plate. Our vision model identifies your meal in under a second."
          />
          <FeatureCard
            icon="fire"
            title="Macro-accurate"
            description="Calories, protein, carbs, and fat pulled from a real nutrition database, not generic averages."
          />
          <FeatureCard
            icon="chart"
            title="Progress that compounds"
            description="Weekly trend charts surface the patterns behind your plateaus so you can adjust before they cost you."
          />
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-8 py-20 text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to see what you are actually eating?</h2>
        <Link
          to="/signup"
          className="inline-block bg-emerald-400 hover:bg-emerald-300 text-black font-semibold px-8 py-3.5 rounded-full transition"
        >
          Get started free
        </Link>
      </div>

      <footer className="border-t border-white/5 py-8 text-center text-sm text-gray-600">
        2026 NutriVision AI
      </footer>
    </div>
  )
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div>
      <p className="text-3xl font-bold text-emerald-400 mb-1">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="bg-[#0f1613] border border-white/5 rounded-2xl p-6">
      <div className="w-10 h-10 rounded-full bg-emerald-400/10 flex items-center justify-center text-xs font-bold text-emerald-300 mb-4 uppercase">
        {icon.slice(0, 2)}
      </div>
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-gray-500 leading-relaxed">{description}</p>
    </div>
  )
}