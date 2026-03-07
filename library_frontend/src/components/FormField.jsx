export default function FormField({ label, children }) {
    return (
        <div className="mb-4">
            <label className="block text-xs font-medium mb-1.5 uppercase tracking-widest" style={{ color: 'var(--muted)' }}>
                {label}
            </label>
            {children}
        </div>
    )
}

export function Input({ ...props }) {
    return (
        <input
            {...props}
            className="w-full px-3 py-2.5 rounded-lg text-sm outline-none transition-all"
            style={{ background: 'var(--bg)', border: '1px solid var(--border)', color: 'var(--text)', fontFamily: 'DM Mono, monospace' }}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'var(--border)'}
        />
    )
}

export function Select({ children, ...props }) {
    return (
        <select
            {...props}
            className="w-full px-3 py-2.5 rounded-lg text-sm outline-none transition-all"
            style={{ background: 'var(--bg)', border: '1px solid var(--border)', color: 'var(--text)', fontFamily: 'DM Mono, monospace' }}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'var(--border)'}
        >
            {children}
        </select>
    )
}