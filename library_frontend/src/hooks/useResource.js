import { useState, useEffect, useCallback } from 'react'

export function useResource(api) {
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    const fetch = useCallback(async () => {
        try {
            setLoading(true)
            setError(null)
            const result = await api.list()
            setData(Array.isArray(result) ? result : (result.results ?? []))
        } catch (e) {
            setError(e.message)
        } finally {
            setLoading(false)
        }
    }, [api])

    useEffect(() => { fetch() }, [fetch])

    const create = async (payload) => { await api.create(payload); await fetch() }
    const update = async (id, payload) => { await api.update(id, payload); await fetch() }
    const remove = async (id) => { await api.delete(id); await fetch() }

    return { data, loading, error, refetch: fetch, create, update, remove }
}