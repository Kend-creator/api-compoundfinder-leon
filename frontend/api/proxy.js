export default async function handler(req, res) {
    // Only allow GET requests
    if (req.method !== "GET") {
        res.setHeader("Allow", "GET");
        return res.status(405).json({ error: "Method not allowed" });
    }

    const path = req.query.path || "";

    // Only allow the three read routes this site needs
    const allowed = /^\/compounds(\/\d+|\/search)?$/;
    if (!allowed.test(path)) {
        return res.status(400).json({ error: "Invalid path" });
    }

    const query = req.query.q ? `?q=${encodeURIComponent(req.query.q)}` : "";

    try {
        const upstream = await fetch(
            `${process.env.API_URL}/api/v1${path}${query}`,
            { headers: { "x-api-key": process.env.API_KEY } }
        );
        const data = await upstream.json();
        res.status(upstream.status).json(data);
    } catch (error) {
        res.status(502).json({ error: "Could not reach the API" });
    }
}