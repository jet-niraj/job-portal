import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

const jobService = {
  getJobs(params = {}) {
    return api.get('/jobs/', { params })
  },

  getJob(id) {
    return api.get(`/jobs/${id}/`)
  },

  createJob(jobData) {
    return api.post('/jobs/', jobData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // PATCH instead of PUT — PUT requires all fields,
  // PATCH sends only what changed (fixes address/date blanking on update)
  updateJob(id, jobData) {
    return api.patch(`/jobs/${id}/`, jobData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  deleteJob(id) {
    return api.delete(`/jobs/${id}/`)
  },

  duplicateJob(id) {
    return api.post(`/jobs/${id}/duplicate/`)
  },

  getAnalytics() {
    return api.get('/jobs/analytics/')
  },

  getStatistics() {
    return api.get('/jobs/statistics/')
  },

  getFilters() {
    return api.get('/jobs/filters/')
  },

  searchJobs(searchQuery, filters = {}) {
    return api.get('/jobs/', {
      params: { search: searchQuery, ...filters }
    })
  }
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 404) {
        console.error('Resource not found')
      } else if (error.response.status === 400) {
        console.error('Bad request:', error.response.data)
      } else if (error.response.status === 500) {
        console.error('Server error')
      }
    }
    return Promise.reject(error)
  }
)

export default jobService