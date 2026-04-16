export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchEventTypes() {
  const res = await fetch(`${API_URL}/event-types`);
  if (!res.ok) throw new Error("Failed to fetch event types");
  return res.json();
}

export async function fetchEventType(id: string | number) {
  const res = await fetch(`${API_URL}/event-types/${id}`);
  if (!res.ok) throw new Error("Failed to fetch event type");
  return res.json();
}

export async function createEventType(data: any) {
  const res = await fetch(`${API_URL}/event-types`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to create event type");
  }
  return res.json();
}

export async function updateEventType(id: number, data: any) {
  const res = await fetch(`${API_URL}/event-types/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to update event type");
  }
  return res.json();
}

export async function deleteEventType(id: number) {
  const res = await fetch(`${API_URL}/event-types/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete event type");
  return res.json();
}

// Schedules
export async function fetchSchedules() {
  const res = await fetch(`${API_URL}/schedules`);
  if (!res.ok) throw new Error("Failed to fetch schedules");
  return res.json();
}

export async function createSchedule(data: any) {
  const res = await fetch(`${API_URL}/schedules`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create schedule");
  return res.json();
}

export async function updateSchedule(id: number, data: any) {
  const res = await fetch(`${API_URL}/schedules/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update schedule");
  return res.json();
}

export async function deleteSchedule(id: number) {
  const res = await fetch(`${API_URL}/schedules/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete schedule");
  return res.json();
}

export async function setDefaultSchedule(id: number) {
  const res = await fetch(`${API_URL}/schedules/${id}/default`, {
    method: "PUT",
  });
  if (!res.ok) throw new Error("Failed to set default schedule");
  return res.json();
}

// Availabilities
export async function fetchAvailabilities(scheduleId: number) {
  const res = await fetch(`${API_URL}/schedules/${scheduleId}/availability`);
  if (!res.ok) throw new Error("Failed to fetch availability");
  return res.json();
}

export async function updateAvailabilities(scheduleId: number, data: any) {
  const res = await fetch(`${API_URL}/schedules/${scheduleId}/availability`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update availability");
  return res.json();
}

// Date Overrides
export async function fetchScheduleOverrides(scheduleId: number) {
  const res = await fetch(`${API_URL}/schedules/${scheduleId}/overrides`);
  if (!res.ok) throw new Error("Failed to fetch overrides");
  return res.json();
}

export async function updateScheduleOverrides(scheduleId: number, data: any) {
  const res = await fetch(`${API_URL}/schedules/${scheduleId}/overrides`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update overrides");
  return res.json();
}

// Bookings
export async function fetchBookings() {
  const res = await fetch(`${API_URL}/bookings`);
  if (!res.ok) throw new Error("Failed to fetch bookings");
  return res.json();
}

export async function cancelBooking(id: number) {
  const res = await fetch(`${API_URL}/bookings/${id}/cancel`, {
    method: "PATCH",
  });
  if (!res.ok) throw new Error("Failed to cancel booking");
  return res.json();
}

// Public
export async function fetchPublicEventType(slug: string) {
  const res = await fetch(`${API_URL}/public/event-types/${slug}`);
  if (!res.ok) throw new Error("Failed to fetch event type");
  return res.json();
}

export async function fetchPublicSlots(slug: string, date: string) {
  const res = await fetch(`${API_URL}/public/slots/${slug}?target_date=${date}`);
  if (!res.ok) throw new Error("Failed to fetch slots");
  return res.json();
}

export async function createPublicBooking(data: any) {
  const res = await fetch(`${API_URL}/bookings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Failed to create booking");
  }
  return res.json();
}
