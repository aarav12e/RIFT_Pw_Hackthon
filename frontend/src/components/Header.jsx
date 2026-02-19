export default function Header() {
  return (
    <header className="border-b border-emerald-900/40 bg-gray-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-emerald-500 flex items-center justify-center text-gray-950 font-bold text-sm">
            Rx
          </div>
          <div>
            <h1 className="text-emerald-400 font-bold text-lg tracking-tight leading-none">
              PharmaGuard
            </h1>
            <p className="text-gray-500 text-xs">Pharmacogenomic Risk Prediction</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse inline-block" />
          CPIC Guidelines Active
        </div>
      </div>
    </header>
  );
}
