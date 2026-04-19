const basePath = '/api';

async function request(path, options = {}) {
  const response = await fetch(`${basePath}${path}`, options);
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(body?.error || 'Server error');
  }
  return body;
}

export function loadToken() {
  return window.localStorage.getItem('cookai_token') || '';
}

export function saveToken(token) {
  window.localStorage.setItem('cookai_token', token);
}

export function clearToken() {
  window.localStorage.removeItem('cookai_token');
}

export async function loginUser(username, password) {
  return request('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
}

export async function registerUser(username, password) {
  return request('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
}

export async function getRecommendations(token, query) {
  return request('/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ query }),
  });
}

export async function getHistory(token) {
  return request('/history', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
