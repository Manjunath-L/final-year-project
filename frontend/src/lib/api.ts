const API_BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, "") ?? "";

export function apiUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}
