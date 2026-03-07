import { useState } from 'react'
import Modal from './Modal'
import FormField, { Input, Select } from './FormField'

const EMPTY = { title: '', isbn: '', genre: '', publication_date: '', author: '' }

export default function Books({ data, authors, onCreate, onUpdate, onDelete }) {
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
    const openEdit = (b) => {
        setSelected(b)
        setForm({ title: b.title, isbn: b.isbn, genre: b.genre, publication_date: b.publication_date, author: extractId(b.author) })
        setModal('edit')
    }
    const openDelete = (b) => { setSelected(b); setModal('delete') }
    const close = () => setModal(null)

    const handleSubmit = async (e) => {
        e.preventDefault()
        const payload = { ...form, author: `http://localhost:8000/api/authors/${form.author}/` }
        if (modal === 'add') await onCreate(payload)
        if (modal === 'edit') await onUpdate(selected.id, payload)
        close()
    }

    const handleDelete = async () => { await onDelete(selected.id); close() }

    return (
        <section className="mb-12">
            <div className="flex items-center justify-between mb-4 pb-3" style={{ borderBottom: '1px solid var(--border)' }}>
                <div className="flex items-center gap-3">
                    <span className="text-2xl">📖</span>
                    <h2 className="text-xl font-bold" style={{ color: 'var(--accent)' }}>Books</h2>
                    <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>{data.length}</span>
                </div>
                <button onClick={openAdd} className="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all hover:scale-105" style={{ background: 'var(--accent)', color: '#080b14' }}>+ Add</button>
            </div>

            <div className="overflow-x-auto rounded-xl" style={{ border: '1px solid var(--border)' }}>
                <table className="w-full text-sm">
                    <thead>
                        <tr style={{ background: 'rgba(0,229,255,0.05)', borderBottom: '1px solid var(--border)' }}>
                            {['ID', 'Title', 'ISBN', 'Genre', 'Published', 'Author', 'Actions'].map(h => (
                                <th key={h} className="px-4 py-3 text-left text-xs uppercase tracking-widest" style={{ color: 'var(--muted)' }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.length === 0
                            ? <tr><td colSpan={7} className="px-4 py-8 text-center" style={{ color: 'var(--muted)' }}>No books yet.</td></tr>
                            : data.map(b => {
                                const author = authors.find(a => String(a.id) === String(extractId(b.author)))
                                return (
                                    <tr key={b.id} className="table-row">
                                        <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>#{b.id}</td>
                                        <td className="px-4 py-3 font-medium">{b.title}</td>
                                        <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>{b.isbn}</td>
                                        <td className="px-4 py-3">
                                            <span className="px-2 py-0.5 rounded text-xs" style={{ background: 'rgba(124,58,237,0.15)', color: '#a78bfa', border: '1px solid rgba(124,58,237,0.2)' }}>{b.genre}</span>
                                        </td>
                                        <td className="px-4 py-3" style={{ color: 'var(--muted)' }}>{b.publication_date}</td>
                                        <td className="px-4 py-3">{author?.name ?? '—'}</td>
                                        <td className="px-4 py-3 flex gap-2">
                                            <button onClick={() => openEdit(b)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(0,229,255,0.1)', color: 'var(--accent)', border: '1px solid rgba(0,229,255,0.2)' }}>Edit</button>
                                            <button onClick={() => openDelete(b)} className="px-3 py-1 rounded text-xs font-medium transition-all hover:scale-105" style={{ background: 'rgba(244,63,94,0.1)', color: 'var(--danger)', border: '1px solid rgba(244,63,94,0.2)' }}>Delete</button>
                                        </td>
                                    </tr>
                                )
                            })}
                    </tbody>
                </table>
            </div>

            <Modal open={modal === 'add' || modal === 'edit'} onClose={close} title={modal === 'add' ? 'Add Book' : 'Edit Book'}>
                <form onSubmit={handleSubmit}>
                    <FormField label="Title"><Input value={form.title} onChange={set('title')} required placeholder="e.g. One Hundred Years of Solitude" /></FormField>
                    <FormField label="ISBN"><Input value={form.isbn} onChange={set('isbn')} required placeholder="e.g. 978-0-06-088328-7" /></FormField>
                    <FormField label="Genre"><Input value={form.genre} onChange={set('genre')} required placeholder="e.g. Magical Realism" /></FormField>
                    <FormField label="Publication Date"><Input type="date" value={form.publication_date} onChange={set('publication_date')} required /></FormField>
                    <FormField label="Author">
                        <Select value={form.author} onChange={set('author')} required>
                            <option value="">Select an author</option>
                            {authors.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                        </Select>
                    </FormField>
                    <div className="flex gap-3 mt-6">
                        <button type="submit" className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--accent)', color: '#080b14' }}>{modal === 'add' ? 'Add Book' : 'Update Book'}</button>
                        <button type="button" onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                    </div>
                </form>
            </Modal>

            <Modal open={modal === 'delete'} onClose={close} title="Confirm Delete">
                <p className="text-sm mb-6" style={{ color: 'var(--muted)' }}>Delete <span className="font-bold" style={{ color: 'var(--text)' }}>{selected?.title}</span>?</p>
                <div className="flex gap-3">
                    <button onClick={handleDelete} className="flex-1 py-2.5 rounded-lg text-sm font-bold" style={{ background: 'var(--danger)', color: 'white' }}>Delete</button>
                    <button onClick={close} className="flex-1 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--border)', color: 'var(--muted)' }}>Cancel</button>
                </div>
            </Modal>
        </section>
    )
}