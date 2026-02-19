export default function Footer() {
    return (
        <footer className="border-t backdrop-blur-md transition-colors duration-300"
            style={{
                background: 'var(--card-bg)',
                borderColor: 'var(--glass-border)'
            }}>
            <div className="max-w-5xl mx-auto px-6 py-5 flex flex-col sm:flex-row items-center justify-between gap-3">

                {/* Left - Logo + copyright */}
                <div className="flex items-center gap-2 text-[var(--text-secondary)] text-xs opacity-60">
                    <span>🧬</span>
                    <span className="font-semibold text-[var(--text-primary)] opacity-80">PharmaGuard</span>
                    <span>·</span>
                    <span>© 2026 Team BugByte</span>
                </div>

                {/* Center - Disclaimer */}
                <p className="text-[var(--text-secondary)] text-xs text-center opacity-50">
                    For research & educational purposes only · Not for clinical diagnosis
                </p>

                {/* Right - Built with */}
                <div className="flex items-center gap-1.5 text-[var(--text-secondary)] text-xs opacity-50">
                    <span>Built with</span>
                    <span className="text-[var(--accent-secondary)]">React</span>
                    <span>·</span>
                    <span className="text-[var(--accent-secondary)]">FastAPI</span>
                </div>

            </div>
        </footer>
    );
}
