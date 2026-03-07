import { useState } from 'react'
import Modal from './Modal'
import FormField, { Input, Select } from './FormField'

const EMPTY = { member: '', book: '', loan_date: '', due_date: '', return_date: '' }

export default function Loans({ data, members, books, onCreate, onUpdate, onDelete }) {
    const [modal, setModal] = useState(null)
    const [form, setForm] = useState(EMPTY)
    const [selected, setSelected] = useState(null)

    const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

    const extractId = (url) => {
        if (!url) return ''
        if (typeof url === 'number') return url
        const m = String(url).match(/\/(\d+)\/$/)
        return m ? m[1] : ''
    }

    const openAdd = () => { setForm(EMPTY); setModal('add') }
    const openEdit = (l) => {
        setSelected(l)
        setForm({ member: extractId(l.member), book: extractId(l.book), loan_date: l.loan_date, due_date: l.due_date, return_date: l.return_date ?? '' })
        setModal('edit')
    }
    const openDelete = (l) => { setSelected(l); setModal('delete') }
    const close = () => setModal(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        const payload = {
            ...form,
            member: `http://localhost:8000/api/members/${form.member}/`,
            book: `http://localhost:8000/api/books/${form.book}/`,
            return_date: form.return_date || null,
        }
        if (modal === 'add') await onCreate(payload)
        if (modal === 'edit') await onUpdate(selected.id, payload)
        close()
    }

    const handleDelete = async () => { await onDelete(selected.id); close() }

    const getStatus = (l) => {
        if (l.return_date) return { label: 'Returned', style: { background: 'rgba(16,185,129,0.1)', color: 'var(--success)', border: '1px solid rgba(16,185,129,0.2)' } }
        if (new Date(l.due_date) < new Date()) return { label: 'Overdue', style: { background: 'rgba(244,63,94,0.1)', color: 'var(--danger)', border: '1px solid rgba(244,63,94,0.2)' } }
        return { label: 'Active', style: { background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' } }
    }

    return (
        <section className="mb-12">
            <div className="flex items-center justify-between mb-4 pb-3" style={{ borderBottom: '1px solid var(--border)' }}>
                <div className="flex items-center gap-3">
                    <span className="text-2xl">📋</span>
                    <h2 className="text-xl font-bold" style={{ color: 'var(--accent)' }}>Loans</h2>
                    <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>{data.length}</span>
                </div>
                <button onClick={openAdd} className="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all hover:scale-105" style={{ background: 'var(--accent)', color: '#080b14' }}>+ Add</button>
            </div>

            <div className="overflow-x-auto rounded-xl" style={{ border: '1px solid var(--border)' }}>
                <table className="w-full text-sm">
                    <thead>
                        <tr style={{ background: 'rgba(0,229,255,0.05)', borderBottom: '1px solid var(--border)' }}>
                            {['ID', 'Member', 'Book', 'Loan Date', 'Due Date', 'Status', 'Actions'].map(h => (
                                <th key={h} className="px-4 py-3 text-left text-xs uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.length === 0
                            ? <tr><td colSpan={7} className="px-4 py-8 text-center" style={{ color: 'var(--muted)' }}>No loans yet.</td></tr>
                            : data.map(l => {
                                const member = members.find(m => String(m.id) === String(extractId(l.member)))
                                const book = books.find(b => String(b.id) === String(extractId(l.book)))
                                const status = getStatus(l)
                                return (
                                    <tr key={l.id} className="table-row">
                                        <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>#{l.id}</td>
                                        <td className="px-4 py-3 font-medium">{member?.name ?? '—'}</td>
                                        <td className="px-4 py-3">{book?.title ?? '—'}</td>
                                        <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>{l.loan_date}</td>
                                        <td className="px-4 py-3" style={{ color: status.label === 'Overdue' ? 'var(--danger)' : 'var(--muted)' }}>{l.due_date}</td>
                                        <td className="px-4 py-3"><span className="px-2 py-0.5 rounded text-xs" style={status.style}>{status.label}</span></td>
                                        <td className="px-4 py-3 flex gap-2">
                                            <button onClick={() => openEdit(l)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>Edit</button>
                                            <button onClick={() => openDelete(l)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(244,63,94,0.1)', color: 'var(--danger)', border: '1px solid rgba(244,63,94,0.2)' }}>Delete</button>
                                        </td>
                                    </tr>
                                )
                            })}
                    </tbody>
                </table>
            </div>

            <Modal open={modal === 'add' || modal === 'edit'} onClose={close} title={modal === 'add' ? 'Add Loan' : 'Edit Loan'}>
                <form onSubmit={handleSubmit}>
                    <FormField label="Member">
                        <Select value={form.member} onChange={set('member')} required>
                            <option value="">Select a member</option>
                            {members.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                        </Select>
                    </FormField>
                    <FormField label="Book">
                        <Select value={form.book} onChange={set('book')} required>
                            <option value="">Select a book</option>
                            {books.map(b => <option key={b.id} value={b.id}>{b.title}</option>)}
                        </Select>
                    </FormField>
                    <FormField label="Loan Date"><Input type="date" value={form.loan_date} onChange={set('loan_date')} required /></FormField>
                    <FormField label="Due Date"><Input type="date" value={form.due_date} onChange={set('due_date')} required /></FormField>
                    <FormField label="Return Date (optional)"><Input type="date" value={form.return_date} onChange={set('return_date')} /></FormField>
                    <div className="flex gap-3 mt-6">
                        <button type="submit" className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--accent)', color: '#080b14' }}>{modal === 'add' ? 'Add Loan' : 'Update Loan'}</button>
                        <button type="button" onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                    </div>
                </form>
            </Modal>

            <Modal open={modal === 'delete'} onClose={close} title="Confirm Delete">
                <p className="text-sm mb-6" style={{ color: 'var(--muted)' }}>Delete loan record <span className="font-bold" style={{ color: 'var(--text)' }}>#{selected?.id}</span>?</p>
                <div className="flex gap-3">
                    <button onClick={handleDelete} className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--danger)', color: 'white' }}>Delete</button>
                    <button onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                </div>
            </Modal>
        </section>
    )
}