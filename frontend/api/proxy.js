// Serverless proxy forwarding approved frontend requests to the FastAPI backend
export default async function handler(req, res) {
  // Restrict HTTP methods to GET, POST, and DELETE
  const allowedMethods = ["GET", "POST", "DELETE"];
  if (!allowedMethods.includes(req.method)) {
    res.setHeader("Allow", allowedMethods.join(", "));
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { path, q, all_users, user_id } = req.query;

  // Allow only /compounds (and /compounds/{id}, /compounds/search) or /discoveries (and /discoveries/{id})
  const isCompoundRoute =
    typeof path === "string" && /^\/compounds(\/\d+|\/search)?$/.test(path);
  const isDiscoveryRoute =
    typeof path === "string" && /^\/discoveries(\/\d+)?$/.test(path);

  if (!isCompoundRoute && !isDiscoveryRoute) {
    return res.status(400).json({ error: "Invalid path" });
  }

  // Compounds are read-only via this proxy; discoveries allow GET, POST, and DELETE
  if (isCompoundRoute && req.method !== "GET") {
    return res.status(405).json({ error: "Method not allowed for compounds" });
  }

  // Build forwarded query string parameters safely
  const upstreamParams = new URLSearchParams();
  if (path === "/compounds/search") {
    if (typeof q !== "string" || !q.trim()) {
      return res.status(400).json({ error: "Missing search query" });
    }
    upstreamParams.set("q", q);
  }
  if (typeof all_users === "string") upstreamParams.set("all_users", all_users);
  if (typeof user_id === "string") upstreamParams.set("user_id", user_id);

  const qs = upstreamParams.toString();
  const queryString = qs ? `?${qs}` : "";

  // Attach server-side API key and forward the user's Supabase Bearer token if present
  const headers = {
    "x-api-key": process.env.API_KEY,
  };

  if (typeof req.headers.authorization === "string" && req.headers.authorization) {
    headers["Authorization"] = req.headers.authorization;
  }

  const fetchOptions = {
    method: req.method,
    headers,
    signal: AbortSignal.timeout(8000),
  };

  // Forward JSON payload for POST and DELETE requests
  if (req.method === "POST" || req.method === "DELETE") {
    if (req.body !== undefined && req.body !== null) {
      headers["Content-Type"] = "application/json";
      fetchOptions.body =
        typeof req.body === "string" ? req.body : JSON.stringify(req.body);
    }
  }

  try {
    const upstream = await fetch(
      `${process.env.API_URL}/api/v1${path}${queryString}`,
      fetchOptions
    );
    const data = await upstream.json();

    // Cache public compound reads at the edge, but never publicly cache user discoveries
    if (upstream.ok && req.method === "GET" && isCompoundRoute) {
      res.setHeader("Cache-Control", "public, s-maxage=300, stale-while-revalidate=3600");
    } else if (req.method === "GET" && isDiscoveryRoute) {
      res.setHeader("Cache-Control", "private, no-store");
    }

    return res.status(upstream.status).json(data);
  } catch {
    return res.status(502).json({ error: "Could not reach the API" });
  }
}