const BASE = "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  getServices: () => request("/services"),
  getService: (slug) => request(`/services/${slug}`),
  getCourses: () => request("/courses"),
  getCourse: (slug) => request(`/courses/${slug}`),
  getProjects: () => request("/projects"),
  getAvailability: (durationMinutes) =>
    request(`/bookings/availability?duration_minutes=${durationMinutes}`),
  createBooking: (payload) =>
    request("/bookings", { method: "POST", body: JSON.stringify(payload) }),
  sendContactMessage: (payload) =>
    request("/contact", { method: "POST", body: JSON.stringify(payload) }),
  submitPlagiarismCheck: (formData) =>
    fetch(`${BASE}/plagiarism-check`, { method: "POST", body: formData }).then(async (res) => {
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed: ${res.status}`);
      }
      return res.json();
    }),
};
