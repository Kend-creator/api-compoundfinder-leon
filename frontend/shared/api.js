// helper reusable function to make requests to the backend API
async function request(path, params = {}) {
    const qs = new URLSearchParams({ path, ...params });
    const res = await fetch(`/api/proxy?${qs}`);
    if (!res.ok) throw new Error((await res.json()).error || res.statusText);
    return res.json();
}

export const getCompounds = () => request("/compounds");
export const getCompound = (id) => request(`/compounds/${id}`);
export const searchCompounds = (q) => request("/compounds/search", { q });