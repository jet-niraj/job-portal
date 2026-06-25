<template>
  <div class="job-card">
    <!-- Image Header -->
    <div class="card-image">
      <img
        v-if="job.job_profile_picture"
        :src="job.job_profile_picture"
        :alt="job.job_title"
        class="job-img"
      />
      <div v-else class="no-image">
        <div class="no-image-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </div>
      </div>

      <!-- Status Badge overlaid on image -->
      <span class="status-pill" :class="`status-${job.status}`">
        {{ job.status_display || job.status }}
      </span>
    </div>

    <!-- Card Body -->
    <div class="card-body">
      <!-- Title + Action Menu -->
      <div class="card-top">
        <h3 class="job-title">{{ job.job_title }}</h3>
        <div class="action-menu" ref="menuRef">
          <button class="menu-trigger" @click.stop="toggleMenu">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/>
            </svg>
          </button>
          <div v-if="menuOpen" class="dropdown">
            <button class="dropdown-item" @click="handleEdit">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              Edit
            </button>
            <button class="dropdown-item" @click="handleDuplicate">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
              </svg>
              Duplicate
            </button>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item item-delete" @click="handleDelete">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/>
                <path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/>
              </svg>
              Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Category + Location -->
      <div class="meta-row">
        <span class="category-tag">{{ job.category_display || job.category }}</span>
        <span class="location-text">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>
          </svg>
          {{ job.city }}, {{ job.state }}
        </span>
      </div>

      <!-- Description -->
      <p class="description">{{ truncateText(job.description, 90) }}</p>

      <!-- Divider -->
      <div class="divider"></div>

      <!-- Date Info -->
      <div class="date-row">
        <div class="date-item">
          <span class="date-label">Start</span>
          <span class="date-value">{{ formatDate(job.start_date) }}</span>
        </div>
        <div class="date-sep"></div>
        <div class="date-item">
          <span class="date-label">End</span>
          <span class="date-value">{{ job.end_date ? formatDate(job.end_date) : 'Ongoing' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'

export default {
  name: 'JobCard',
  props: {
    job: { type: Object, required: true }
  },
  emits: ['edit', 'delete', 'duplicate'],
  setup(props, { emit }) {
    const menuOpen = ref(false)
    const menuRef = ref(null)

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value
    }

    const closeMenu = (e) => {
      if (menuRef.value && !menuRef.value.contains(e.target)) {
        menuOpen.value = false
      }
    }

    onMounted(() => document.addEventListener('click', closeMenu))
    onBeforeUnmount(() => document.removeEventListener('click', closeMenu))

    const handleEdit = () => {
      menuOpen.value = false
      emit('edit', props.job)
    }

    const handleDelete = () => {
      menuOpen.value = false
      emit('delete', props.job.id)
    }

    const handleDuplicate = () => {
      menuOpen.value = false
      emit('duplicate', props.job.id)
    }

    const truncateText = (text, length) => {
      if (!text) return ''
      return text.length > length ? text.substring(0, length) + '...' : text
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      if (isNaN(date)) return dateString
      return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    }

    return { menuOpen, menuRef, toggleMenu, handleEdit, handleDelete, handleDuplicate, truncateText, formatDate }
  }
}
</script>

<style scoped>
.job-card {
  background: #fff;
  border-radius: 12px;
  border: 1.5px solid #c7d2fe;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.2s, border-color 0.2s, transform 0.2s;
  height: 100%;
}

.job-card:hover {
  border-color: #6366f1;
  box-shadow: 0 8px 28px rgba(99, 102, 241, 0.12);
  transform: translateY(-3px);
}

/* Image */
.card-image {
  position: relative;
  width: 100%;
  height: 130px;
  background: #eef2ff;
  overflow: hidden;
  flex-shrink: 0;
}

.job-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
  color: #a5b4fc;
}

/* Status pill on image */
.status-pill {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.status-draft    { background: #e0e7ff; color: #4338ca; }
.status-requested{ background: #fef9c3; color: #92400e; }
.status-posted   { background: #dbeafe; color: #1d4ed8; }
.status-filled   { background: #dcfce7; color: #166534; }

/* Card Body */
.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

/* Top row: title + menu */
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.job-title {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.35;
  flex: 1;
}

/* Action Menu */
.action-menu {
  position: relative;
  flex-shrink: 0;
}

.menu-trigger {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  transition: background 0.15s, color 0.15s;
}

.menu-trigger:hover {
  background: #f3f4f6;
  color: #374151;
}

.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  right: 0;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  min-width: 148px;
  z-index: 50;
  overflow: hidden;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 14px;
  background: none;
  border: none;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
  text-align: left;
  transition: background 0.12s;
}

.dropdown-item:hover {
  background: #f9fafb;
}

.dropdown-divider {
  height: 1px;
  background: #f3f4f6;
  margin: 2px 0;
}

.item-delete {
  color: #dc2626;
}

.item-delete:hover {
  background: #fef2f2;
}

/* Meta row */
.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 6px;
}

.category-tag {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
}

.location-text {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #6b7280;
}

/* Description */
.description {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.55;
  margin: 0;
  flex-grow: 1;
}

/* Divider */
.divider {
  height: 1px;
  background: #f3f4f6;
}

/* Date row */
.date-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.date-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #9ca3af;
  font-weight: 600;
}

.date-value {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.date-sep {
  width: 1px;
  height: 28px;
  background: #e5e7eb;
}

/* Responsive */
@media (max-width: 640px) {
  .card-image { height: 110px; }
  .card-body { padding: 14px; }
  .job-title { font-size: 14px; }
}
</style>