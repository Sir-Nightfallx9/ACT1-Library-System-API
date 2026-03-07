import { useEffect } from 'react'

export default function Modal({ open, onClose, title, children }) {
    useEffect(() => {
        const handler = (e) => { if (e.key === 'Escape') onClose() }
        if (open) window.addEventListener('keydown', handler)
        return () => window.removeEventListener('keydown', handler)
    }, [open, onClose])

    if (!open) return null

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
            style={{ background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(6px)' }}
            onClick={(e) => { if (e.target === e.currentTarget) onClose() }}
        >
            <div
                className="fade-in w-full max-w-md rounded-2xl p-7 relative"
                style={{
                    background: 'var(--surface)',
                    border: '1px solid var(--border)',
                    boxShadow: '0 0 40px rgba(0,229,255,0.08), 0 20px 60px rgba(0,0,0,0.6)'
                }}
            >
                <div className="absolute top-0 left-8 right-8 h-px" style={{ background: 'linear-gradient(90deg, transparent, var(--accent), transparent)' }} />
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold" style={{ color: 'var(--accent)' }}>{title}</h3>
                    <button onClick={onClose} className="text-sm px-2 py-1 rounded hover:bg-white/5" style={{ color: 'var(--muted)' }}>✕</button>
                </div>
                {children}
            </div>
        </div>
    )
}