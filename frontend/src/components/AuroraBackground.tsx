// A subtle animated background - soft glowing blobs that slowly drift.
// Used behind auth pages (Login/Signup) to add visual life without
// being distracting. Pure CSS animation, no JS overhead.

export default function AuroraBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <div className="absolute -top-32 -left-32 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl animate-blob" />
      <div className="absolute top-1/2 -right-32 w-96 h-96 bg-teal-500/15 rounded-full blur-3xl animate-blob animation-delay-2000" />
      <div className="absolute -bottom-32 left-1/3 w-96 h-96 bg-emerald-400/10 rounded-full blur-3xl animate-blob animation-delay-4000" />
    </div>
  )
}