const BASE = '/api'

async function request(url, options = {}) {
    const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    if (res.status === 204) return null
    return res.json()
}

function resource(name) {
    const url = `${BASE}/${name}/`
    return {
        list: () => request(url),
        create: (data) => request(url, { method: 'POST', body: JSON.stringify(data) }),
        update: (id, data) => request(`${url}${id}/`, { method: 'PUT', body: JSON.stringify(data) }),
        delete: (id) => request(`${url}${id}/`, { method: 'DELETE' }),
    }
}

export const authorsApi = resource('authors')
export const booksApi = resource('books')
export const membersApi = resource('members')
export const loansApi = resource('loans')