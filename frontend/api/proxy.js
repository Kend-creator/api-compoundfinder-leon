export default async function handler(req, res) {
    // Only allow GET requests
    if (req.method !== "GET") {
        res.setHeader("Allow", "GET");
        return res.status(405).json({ error: "Method not allowed" });
    }

    const { path, q } = req.query;

    // Only allow the three read routes this site needs
    if (typeof path !== "string" || !/^\/compounds(\/\d+|\/search)?$/.test(path)) {
        return res.status(400).json({ error: "Invalid path" });
    }

    const isSearch = path === "/compounds/search";
    if (isSearch && (typeof q !== "string" || !q.trim())) {
        return res.status(400).json({ error: "Missing search query" });
    }
    const query = isSearch ? `?q=${encodeURIComponent(q)}` : "";

    try {
        const upstream = await fetch(
            `${process.env.API_URL}/api/v1${path}${query}`,
            {
                headers: { "x-api-key": process.env.API_KEY },
                signal: AbortSignal.timeout(8000),
            }
        );
        const data = await upstream.json();
        res.status(upstream.status).json(data);
    } catch (error) {
        res.status(502).json({ error: "Could not reach the API" });
    }
}