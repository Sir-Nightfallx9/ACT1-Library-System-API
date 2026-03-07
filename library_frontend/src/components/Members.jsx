import { useState } from 'react'
import Modal from './Modal'
import FormField, { Input } from './FormField'

const EMPTY = { name: '', email: '', phone: '', membership_date: '' }

export default function Members({ data, onCreate, onUpdate, onDelete }) {
    const [modal, setModal] = useState(null)
    const [form, setForm] = useState(EMPTY)
    const [selected, setSelected] = useState(null)

    const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))
    const openAdd = () => { setForm(EMPTY); setModal('add') }
    const openEdit = (m) => { setSelected(m); setForm({ name: m.name, email: m.email, phone: m.phone, membership_date: m.membership_date }); setModal('edit') }
    const openDelete = (m) => { setSelected(m); setModal('delete') }
    const close = () => setModal(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (modal === 'add') await onCreate(form)
        if (modal === 'edit') await onUpdate(selected.id, form)
        close()
    }

    const handleDelete = async () => { await onDelete(selected.id); close() }

    return (
        <section className="mb-12">
            <div className="flex items-center justify-between mb-4 pb-3" style={{ borderBottom: '1px solid var(--border)' }}>
                <div className="flex items-center gap-3">
                    <span className="text-2xl">👥</span>
                    <h2 className="text-xl font-bold" style={{ color: 'var(--accent)' }}>Members</h2>
                    <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>{data.length}</span>
                </div>
                <button onClick={openAdd} className="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all hover:scale-105" style={{ background: 'var(--accent)', color: '#080b14' }}>+ Add</button>
            </div>

            <div className="overflow-x-auto rounded-xl" style={{ border: '1px solid var(--border)' }}>
                <table className="w-full text-sm">
                    <thead>
                        <tr style={{ background: 'rgba(0,229,255,0.05)', borderBottom: '1px solid var(--border)' }}>
                            {['ID', 'Name', 'Email', 'Phone', 'Member Since', 'Actions'].map(h => (
                                <th key={h} className="px-4 py-3 text-left text-xs uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.length === 0
                            ? <tr><td colSpan={6} className="px-4 py-8 text-center" style={{ color: 'var(--muted)' }}>No members yet.</td></tr>
                            : data.map(m => (
                                <tr key={m.id} className="table-row">
                                    <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>#{m.id}</td>
                                    <td className="px-4 py-3 font-medium">{m.name}</td>
                                    <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>{m.email}</td>
                                    <td className="px-4 py-3">{m.phone}</td>
                                    <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>{m.membership_date}</td>
                                    <td className="px-4 py-3 flex gap-2">
                                        <button onClick={() => openEdit(m)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>Edit</button>
                                        <button onClick={() => openDelete(m)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(244,63,94,0.1)', color: 'var(--danger)', border: '1px solid rgba(244,63,94,0.2)' }}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </table>
            </div>

            <Modal open={modal === 'add' || modal === 'edit'} onClose={close} title={modal === 'add' ? 'Add Member' : 'Edit Member'}>
                <form onSubmit={handleSubmit}>
                    <FormField label="Name"><Input value={form.name} onChange={set('name')} required placeholder="Full name" /></FormField>
                    <FormField label="Email"><Input type="email" value={form.email} onChange={set('email')} required placeholder="email@example.com" /></FormField>
                    <FormField label="Phone"><Input type="tel" value={form.phone} onChange={set('phone')} required placeholder="+63 900 000 0000" /></FormField>
                    <FormField label="Membership Date"><Input type="date" value={form.membership_date} onChange={set('membership_date')} required /></FormField>
                    <div className="flex gap-3 mt-6">
                        <button type="submit" className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--accent)', color: '#080b14' }}>{modal === 'add' ? 'Add Member' : 'Update Member'}</button>
                        <button type="button" onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                    </div>
                </form>
            </Modal>

            <Modal open={modal === 'delete'} onClose={close} title="Confirm Delete">
                <p className="text-sm mb-6" style={{ color: 'var(--muted)' }}>Delete <span className="font-bold" style={{ color: 'var(--text)' }}>{selected?.name}</span>?</p>
                <div className="flex gap-3">
                    <button onClick={handleDelete} className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--danger)', color: 'white' }}>Delete</button>
                    <button onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                </div>
            </Modal>
        </section>
    )
}