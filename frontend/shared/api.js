import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://ulnzqrwzomzzopvocvzj.supabase.co";
const SUPABASE_ANON_KEY = "<your-full-publishable-key>";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Helper reusable function to make requests to the backend API / proxy
async function request(path, { params = {}, method = "GET", body = null } = {}) {
  const qs = new URLSearchParams({ path, ...params });
  const headers = {};

  if (body !== null && body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  const { data } = await supabase.auth.getSession();
  const token = data?.session?.access_token;
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body !== null && body !== undefined) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`/api/proxy?${qs}`, options);
  if (!res.ok) {
    let message = res.statusText;
    try {
      const errData = await res.json();
      message = errData.error || errData.detail || message;
    } catch {
      // Fall back to HTTP status text if response is not JSON
    }
    throw new Error(message);
  }
  return res.json();
}

export const getCompounds = () => request("/compounds");
export const getCompound = (id) => request(`/compounds/${id}`);
export const searchCompounds = (q) => request("/compounds/search", { params: { q } });

export const getDiscoveries = ({ allUsers = false, userId = null } = {}) => {
  const params = {};
  if (allUsers) params.all_users = "true";
  if (userId) params.user_id = userId;
  return request("/discoveries", { params });
};

export const createDiscovery = (compoundId, userId = null) =>
  request("/discoveries", {
    method: "POST",
    body: userId ? { compoundId, userId } : { compoundId },
  });

export const deleteDiscovery = (compoundId, userId = null) =>
  request(`/discoveries/${compoundId}`, {
    method: "DELETE",
    params: userId ? { user_id: userId } : {},
  });