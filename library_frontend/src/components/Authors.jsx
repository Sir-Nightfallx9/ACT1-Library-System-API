import { useState } from 'react'
import Modal from './Modal'
import FormField, { Input } from './FormField'

const EMPTY = { name: '', nationality: '' }

export default function Authors({ data, onCreate, onUpdate, onDelete }) {
    const [modal, setModal] = useState(null)
    const [form, setForm] = useState(EMPTY)
    const [selected, setSelected] = useState(null)

    const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))
    const openAdd = () => { setForm(EMPTY); setModal('add') }
    const openEdit = (a) => { setSelected(a); setForm({ name: a.name, nationality: a.nationality }); setModal('edit') }
    const openDelete = (a) => { setSelected(a); setModal('delete') }
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
                    <span className="text-2xl">✍️</span>
                    <h2 className="text-xl font-bold" style={{ color: 'var(--accent)' }}>Authors</h2>
                    <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>{data.length}</span>
                </div>
                <button onClick={openAdd} className="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all hover:scale-105" style={{ background: 'var(--accent)', color: '#080b14' }}>+ Add</button>
            </div>

            <div className="overflow-x-auto rounded-xl" style={{ border: '1px solid var(--border)' }}>
                <table className="w-full text-sm">
                    <thead>
                        <tr style={{ background: 'rgba(0,229,255,0.05)', borderBottom: '1px solid var(--border)' }}>
                            {['ID', 'Name', 'Nationality', 'Actions'].map(h => (
                                <th key={h} className="px-4 py-3 text-left text-xs uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.length === 0
                            ? <tr><td colSpan={4} className="px-4 py-8 text-center" style={{ color: 'var(--muted)' }}>No authors yet. Click "+ Add" to get started.</td></tr>
                            : data.map(a => (
                                <tr key={a.id} className="table-row">
                                    <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>#{a.id}</td>
                                    <td className="px-4 py-3 font-medium">{a.name}</td>
                                    <td className="px-4 py-3">{a.nationality}</td>
                                    <td className="px-4 py-3 flex gap-2">
                                        <button onClick={() => openEdit(a)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>Edit</button>
                                        <button onClick={() => openDelete(a)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(244,63,94,0.1)', color: 'var(--danger)', border: '1px solid rgba(244,63,94,0.2)' }}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </table>
            </div>

            <Modal open={modal === 'add' || modal === 'edit'} onClose={close} title={modal === 'add' ? 'Add Author' : 'Edit Author'}>
                <form onSubmit={handleSubmit}>
                    <FormField label="Name"><Input value={form.name} onChange={set('name')} required placeholder="e.g. Gabriel García Márquez" /></FormField>
                    <FormField label="Nationality"><Input value={form.nationality} onChange={set('nationality')} required placeholder="e.g. Colombian" /></FormField>
                    <div className="flex gap-3 mt-6">
                        <button type="submit" className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--accent)', color: '#080b14' }}>{modal === 'add' ? 'Add Author' : 'Update Author'}</button>
                        <button type="button" onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                    </div>
                </form>
            </Modal>

            <Modal open={modal === 'delete'} onClose={close} title="Confirm Delete">
                <p className="text-sm mb-6" style={{ color: 'var(--muted)' }}>Delete <span className="font-bold" style={{ color: 'var(--text)' }}>{selected?.name}</span>? This cannot be undone.</p>
                <div className="flex gap-3">
                    <button onClick={handleDelete} className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--danger)', color: 'white' }}>Yes, Delete</button>
                    <button onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                </div>
            </Modal>
        </section>
    )
}