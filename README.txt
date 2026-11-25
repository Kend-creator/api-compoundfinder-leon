# Simple Compound Element API (Compound Lab)

A cloud-hosted chemistry web application and FastAPI REST backend backed by **Supabase** (PostgreSQL, Auth, and Storage) and deployed across **Vercel**[cite: 2]. It combines a compound encyclopedia and search catalog, periodic table and discovery tracking, and interactive chemistry simulations for crafting compounds from elements and combining compounds into reactions[cite: 2].

---

## Architecture Overview

The project runs across two Vercel deployments and Supabase[cite: 2]:

- **Frontend & Proxy Layer (Vercel):** Serves static HTML, CSS, and JavaScript pages (including Home/Index, Finder, Craft, Combine, and Login) and runs `/api/proxy` (`proxy.js`)[cite: 2]. The proxy attaches the server-side `x-api-key` header, forwards the user's Supabase `Authorization: Bearer <token>` header, restricts routes/methods, and caches public compound/element GET reads at the edge while keeping per-user discovery reads uncached[cite: 2]. The browser also connects directly to Supabase Auth for sessions and loads compound images from the public `compound-images` Storage bucket[cite: 2].
- **Backend API Layer (Vercel / FastAPI):** A Python FastAPI application (`api/index.py`) that validates inputs and outputs with Pydantic models, enforces `x-api-key` (`verify_API_KEY`) and user/admin role checks (`profiles`), queries and updates Supabase tables via the `supabase` Python SDK (`create_client`), and runs chemistry rules[cite: 2].
- **Database & Auth Layer (Supabase):** A PostgreSQL database storing relational compound data (`compounds` and `compound_composition`), periodic table and simulation tables (`elements`, `number_prefixes`, `polyatomic_ions`, `reactions`, `reaction_participants`), and user/discovery tables (`profiles`, `compound_discoveries`), alongside Supabase Auth and Storage[cite: 2].

---

## Configuration & Environment Variables

### Environment Variables
- `API_KEY`: Shared secret verified via the `x-api-key` header in `api/index.py` and attached server-side by `/api/proxy` (`proxy.js`)[cite: 2].
- `SUPABASE_URL`: Base URL of the Supabase project passed to `create_client(...)` in `api/index.py`[cite: 2].
- `SUPABASE_KEY`: Key passed to `create_client(...)` in `api/index.py` for authenticating backend requests to Supabase[cite: 2].

### Configuration & Routing Files
- `api/index.py`: FastAPI application entrypoint, Pydantic schemas, `to_api()` row-to-JSON mapper, auth/role helpers, chemistry logic, and route handlers[cite: 2, 3, 10].
- `vercel.json`: Configures Vercel build and routing rules for deployment[cite: 1, 2].
- `proxy.js`: Frontend serverless proxy handler at `/api/proxy` that injects `x-api-key` and forwards Bearer tokens[cite: 2].

---

## Endpoints

### Public Routes
- `GET /health`: Health check returning service status (`"ok"`), service name, version (`1.0.0`), and a UTC timestamp[cite: 2, 3].
- `GET /`: Home/overview route returning a welcome message and listing available API paths[cite: 2, 3].
- `/docs` & `/redoc`: Auto-generated FastAPI interactive OpenAPI (Swagger UI) and ReDoc documentation pages[cite: 1, 2].

### Protected Routes (`x-api-key` required)
- `GET /api/v1/compounds`: Returns all compounds joined with `compound_composition` from Supabase (`fetch_all()`), mapped via `to_api()`, along with the total `count`[cite: 2, 3].
- `GET /api/v1/compounds/search?q=...`: Case-insensitive search across compound name, formula, SMILES, compound type, CAS number, element names/symbols, uses, physical state, signal word, and hazard statements (requires non-empty `q`)[cite: 2, 3].
- `GET /api/v1/compounds/{compound_id}`: Returns a single compound by numeric `id` (or `404` if not found)[cite: 2, 3].
- `GET /api/v1/elements`: Returns periodic table elements ordered by `atomic_number` and `count`[cite: 2, 3].
- `POST /api/v1/compounds/craft`: Combines two distinct elements/atom counts—matching an existing compound composition (`isKnownCompound: true`) or dynamically generating an ionic/covalent IUPAC name and formula using `elements` and `number_prefixes` (`isKnownCompound: false`)[cite: 2, 3, 8, 9].
- `POST /api/v1/compounds/combine`: Combines two compound IDs using a normalized sorted `"smallerId+largerId"` `reactant_key` against `reactions` and `reaction_participants` (`isKnownReaction: true`), or falls back to a double-replacement ion swap using `polyatomic_ions` and `math.gcd` charge balancing (`isKnownReaction: false`)[cite: 2, 3, 8, 9].
- `GET / POST / DELETE /api/v1/discoveries`: Reads, creates, and removes user compound discoveries in `compound_discoveries` with Supabase user authentication and role checks (`profiles`)[cite: 2].

---

## Frontend Logic Flow

- **Compound Finder:** Loads compounds (`GET /api/v1/compounds`), renders cards for each compound, supports searching (`GET /api/v1/compounds/search?q=...`) or showing all compounds, and opens a detail modal (`GET /api/v1/compounds/{compound_id}`)[cite: 1, 2, 7].
- **Craft & Combine Views:** Let users select elements from `/api/v1/elements` to craft compounds (`/api/v1/compounds/craft`), simulate reactions between compounds (`/api/v1/compounds/combine`), and manage sign-in/session state via Supabase Auth[cite: 2, 8].

---

## Running Locally

1. Set `API_KEY`, `SUPABASE_URL`, and `SUPABASE_KEY` in your environment (or local `.env` file)[cite: 2].
2. Start the FastAPI server locally (for example, with `uvicorn` on port `8000`)[cite: 2].
3. Open `/docs` in your browser to inspect and test endpoints using your `x-api-key` header[cite: 1, 2].