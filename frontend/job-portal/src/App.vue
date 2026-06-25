<template>
  <div class="app">
    <!-- Header -->
    <header class="app-header">
      <div class="header-inner">
        <div class="brand">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="2">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/>
            <line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/>
          </svg>
          <span>Job Portal</span>
        </div>
        <button class="btn-post" @click="openCreateDialog">Post Job</button>
      </div>
    </header>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-wrap">
        <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by title or description..."
          class="search-input"
        />
        <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div class="toolbar-right">
        <select v-model="selectedStatus" class="filter-select">
          <option value="">All Status</option>
          <option value="draft">Draft</option>
          <option value="requested">Requested</option>
          <option value="posted">Posted</option>
          <option value="filled">Filled</option>
        </select>
        <button class="btn-analytics" @click="openAnalyticsModal">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
          Analytics
        </button>
      </div>
    </div>

    <!-- Job Count -->
    <div class="results-bar" v-if="!loading">
      <span class="results-text">
        {{ filteredJobs.length }} {{ filteredJobs.length === 1 ? 'job' : 'jobs' }}
        <template v-if="searchQuery || selectedStatus"> found</template>
      </span>
    </div>

    <!-- Main -->
    <main class="main">
      <!-- Loading -->
      <div v-if="loading" class="state-center">
        <div class="spinner"></div>
        <p>Loading jobs...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredJobs.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#c7d2fe" stroke-width="1.5">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/>
          </svg>
        </div>
        <p class="empty-title">{{ searchQuery || selectedStatus ? 'No jobs match your search' : 'No jobs posted yet' }}</p>
        <p class="empty-sub">{{ searchQuery || selectedStatus ? 'Try adjusting your filters.' : 'Click "Post Job" to get started.' }}</p>
        <button v-if="!searchQuery && !selectedStatus" class="btn-post" @click="openCreateDialog">Post Job</button>
      </div>

      <!-- Grid -->
      <div v-else class="jobs-grid">
        <JobCard
          v-for="job in filteredJobs"
          :key="job.id"
          :job="job"
          @edit="openEditDialog"
          @delete="deleteJob"
          @duplicate="duplicateJob"
        />
      </div>
    </main>

    <!-- Dialogs -->
    <CreateJobDialog
      v-if="showCreateDialog"
      :job="editingJob"
      :filterOptions="filterOptions"
      @save="saveJob"
      @close="closeCreateDialog"
    />

    <AnalyticsModal
      v-if="showAnalyticsModal"
      :analyticsData="analyticsData"
      @close="closeAnalyticsModal"
    />

    <Toast v-if="toast.show" :message="toast.message" :type="toast.type" />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import jobService from './services/jobService'
import JobCard from './components/JobCard.vue'
import CreateJobDialog from './components/CreateJobDialog.vue'
import AnalyticsModal from './components/AnalyticsModal.vue'
import Toast from './components/Toast.vue'

export default {
  name: 'App',
  components: { JobCard, CreateJobDialog, AnalyticsModal, Toast },
  setup() {
    const jobs            = ref([])
    const loading         = ref(false)
    const searchQuery     = ref('')
    const selectedStatus  = ref('')
    const showCreateDialog   = ref(false)
    const showAnalyticsModal = ref(false)
    const editingJob      = ref(null)
    const filterOptions   = ref({})
    const analyticsData   = ref({})
    const toast           = ref({ show: false, message: '', type: 'success' })

    const fetchJobs = async () => {
      loading.value = true
      try {
        const res = await jobService.getJobs()
        jobs.value = res.data.results
      } catch {
        showToast('Failed to load jobs.', 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchFilterOptions = async () => {
      try {
        const res = await jobService.getFilters()
        filterOptions.value = res.data
      } catch { /* silent */ }
    }

    const fetchAnalytics = async () => {
      try {
        const res = await jobService.getAnalytics()
        analyticsData.value = res.data
      } catch { /* silent */ }
    }

    const filteredJobs = computed(() =>
      jobs.value.filter(job => {
        const q = searchQuery.value.toLowerCase()
        const matchSearch = !q ||
          job.job_title.toLowerCase().includes(q) ||
          job.description.toLowerCase().includes(q)
        const matchStatus = !selectedStatus.value || job.status === selectedStatus.value
        return matchSearch && matchStatus
      })
    )

    const openCreateDialog  = () => { editingJob.value = null; showCreateDialog.value = true }
    const openEditDialog    = (job) => { editingJob.value = { ...job }; showCreateDialog.value = true }
    const closeCreateDialog = () => { showCreateDialog.value = false; editingJob.value = null }

    const saveJob = async (jobData) => {
      try {
        if (editingJob.value?.id) {
          await jobService.updateJob(editingJob.value.id, jobData)
          showToast('Job updated successfully.')
        } else {
          await jobService.createJob(jobData)
          showToast('Job created successfully.')
        }
        closeCreateDialog()
        fetchJobs()
      } catch {
        showToast('Failed to save job.', 'error')
      }
    }

    const deleteJob = async (jobId) => {
      if (!confirm('Delete this job?')) return
      try {
        await jobService.deleteJob(jobId)
        showToast('Job deleted.')
        fetchJobs()
      } catch {
        showToast('Failed to delete job.', 'error')
      }
    }

    const duplicateJob = async (jobId) => {
      try {
        await jobService.duplicateJob(jobId)
        showToast('Job duplicated.')
        fetchJobs()
      } catch {
        showToast('Failed to duplicate job.', 'error')
      }
    }

    const openAnalyticsModal  = async () => { showAnalyticsModal.value = true; await fetchAnalytics() }
    const closeAnalyticsModal = () => { showAnalyticsModal.value = false }

    const showToast = (message, type = 'success') => {
      toast.value = { show: true, message, type }
      setTimeout(() => { toast.value.show = false }, 3000)
    }

    onMounted(() => { fetchJobs(); fetchFilterOptions() })

    return {
      jobs, loading, filteredJobs, searchQuery, selectedStatus,
      showCreateDialog, showAnalyticsModal, editingJob,
      filterOptions, analyticsData, toast,
      openCreateDialog, openEditDialog, closeCreateDialog,
      openAnalyticsModal, closeAnalyticsModal,
      saveJob, deleteJob, duplicateJob
    }
  }
}
</script>

<style scoped>
* { box-sizing: border-box; }

.app {
  min-height: 100vh;
  background: #f5f6fa;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  color: #111827;
}

/* Header */
.app-header {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 58px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

/* Toolbar */
.toolbar {
  max-width: 1200px;
  margin: 20px auto 0;
  padding: 0 24px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-wrap {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: #9ca3af;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 9px 36px 9px 36px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #fff;
  color: #111827;
  transition: border-color 0.15s;
}

.search-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.08);
}

.search-clear {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  display: flex;
  align-items: center;
  padding: 2px;
}

.search-clear:hover { color: #374151; }

.toolbar-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.filter-select {
  padding: 9px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  background: #fff;
  color: #374151;
  cursor: pointer;
  transition: border-color 0.15s;
}

.filter-select:focus {
  outline: none;
  border-color: #6366f1;
}

/* Buttons */
.btn-post {
  padding: 9px 18px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-post:hover { background: #4338ca; }

.btn-analytics {
  padding: 9px 14px;
  background: #fff;
  color: #374151;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: border-color 0.15s, background 0.15s;
}

.btn-analytics:hover {
  border-color: #6366f1;
  color: #4f46e5;
  background: #fafafe;
}

/* Results bar */
.results-bar {
  max-width: 1200px;
  margin: 12px auto 0;
  padding: 0 24px;
}

.results-text {
  font-size: 13px;
  color: #6b7280;
}

/* Main */
.main {
  max-width: 1200px;
  margin: 16px auto 0;
  padding: 0 24px 48px;
}

/* States */
.state-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 360px;
  gap: 12px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.state-center p { font-size: 14px; color: #6b7280; margin: 0; }

/* Empty */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 360px;
  gap: 10px;
  text-align: center;
}

.empty-icon {
  width: 72px;
  height: 72px;
  background: #eef2ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.empty-sub {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

/* Grid */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* Responsive */
@media (max-width: 640px) {
  .toolbar { flex-direction: column; align-items: stretch; }
  .toolbar-right { flex-direction: row; }
  .filter-select { flex: 1; }
  .jobs-grid { grid-template-columns: 1fr; }
  .header-inner { padding: 0 16px; }
  .toolbar, .results-bar, .main { padding-left: 16px; padding-right: 16px; }
}
</style>