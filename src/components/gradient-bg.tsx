export default function GradientBackground() {
  return (
    <div className="absolute min-h-screen w-full overflow-hidden">
      <div className='absolute inset-0 bg-gradient-to-tr from-violet-900 via-sky-700 to-emerald-600 animate-gradient'/>
      <style>{`
        @keyframes gradient {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }
        .animate-gradient {
          animation: gradient 15s ease infinite;
          background-size: 200vh 200vh;
        }
      `}</style>
    </div>
  )
}
