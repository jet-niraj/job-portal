<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <!-- Header -->
      <div class="modal-header">
        <h2>Analytics Dashboard</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <div class="modal-body">
        <!-- Summary Cards -->
        <div class="summary-row">
          <div class="stat-card">
            <span class="stat-label">Total Jobs</span>
            <span class="stat-value">{{ analyticsData.total_jobs || 0 }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Cities</span>
            <span class="stat-value">{{ cityCount }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">States</span>
            <span class="stat-value">{{ stateCount }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Categories</span>
            <span class="stat-value">{{ categoryCount }}</span>
          </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
          <!-- Status — Pie Chart -->
          <div class="chart-box">
            <h3 class="chart-title">Jobs by Status</h3>
            <div class="chart-wrap">
              <PieChart
                v-if="hasStatusData"
                :data="statusChartData"
                :options="pieOptions"
              />
              <div v-else class="no-data">No data available</div>
            </div>
          </div>

          <!-- Category — Pie Chart -->
          <div class="chart-box">
            <h3 class="chart-title">Jobs by Category</h3>
            <div class="chart-wrap">
              <PieChart
                v-if="hasCategoryData"
                :data="categoryChartData"
                :options="pieOptions"
              />
              <div v-else class="no-data">No data available</div>
            </div>
          </div>

          <!-- City — Bar Chart -->
          <div class="chart-box chart-wide">
            <h3 class="chart-title">Jobs by City</h3>
            <div class="chart-wrap chart-wrap-bar">
              <BarChart
                v-if="hasCityData"
                :data="cityChartData"
                :options="barOptions"
              />
              <div v-else class="no-data">No data available</div>
            </div>
          </div>

          <!-- State — Bar Chart -->
          <div class="chart-box chart-wide">
            <h3 class="chart-title">Jobs by State</h3>
            <div class="chart-wrap chart-wrap-bar">
              <BarChart
                v-if="hasStateData"
                :data="stateChartData"
                :options="barOptions"
              />
              <div v-else class="no-data">No data available</div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn-close" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { Pie as PieChart, Bar as BarChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  ArcElement, CategoryScale, LinearScale, BarElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement)

const PIE_COLORS = ['#6366f1', '#818cf8', '#34d399', '#fbbf24', '#f87171', '#60a5fa', '#a78bfa', '#fb7185']
const BAR_COLOR = '#6366f1'

export default {
  name: 'AnalyticsModal',
  components: { PieChart, BarChart },
  props: {
    analyticsData: { type: Object, default: () => ({}) }
  },
  emits: ['close'],
  setup(props) {

    // Counts
    const cityCount     = computed(() => Object.keys(props.analyticsData.city_distribution || {}).length)
    const stateCount    = computed(() => Object.keys(props.analyticsData.state_distribution || {}).length)
    // backend returns jobs_by_category
    const categoryCount = computed(() => Object.keys(props.analyticsData.jobs_by_category || {}).length)

    // Has data guards
    const hasStatusData   = computed(() => Object.keys(props.analyticsData.status_distribution || {}).length > 0)
    const hasCityData     = computed(() => Object.keys(props.analyticsData.city_distribution || {}).length > 0)
    const hasStateData    = computed(() => Object.keys(props.analyticsData.state_distribution || {}).length > 0)
    const hasCategoryData = computed(() => Object.keys(props.analyticsData.jobs_by_category || {}).length > 0)

    // Chart options
    const pieOptions = {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 14, font: { size: 12 }, boxWidth: 12 }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: ${ctx.parsed} jobs`
          }
        }
      }
    }

    const barOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.parsed.y} jobs`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 12 } }
        },
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, font: { size: 12 } },
          grid: { color: '#f3f4f6' }
        }
      }
    }

    // Chart data builders
    const statusChartData = computed(() => ({
      labels: Object.keys(props.analyticsData.status_distribution || {}),
      datasets: [{
        data: Object.values(props.analyticsData.status_distribution || {}),
        backgroundColor: PIE_COLORS,
        borderColor: '#fff',
        borderWidth: 2
      }]
    }))

    // Fix: use jobs_by_category not category_distribution
    const categoryChartData = computed(() => ({
      labels: Object.keys(props.analyticsData.jobs_by_category || {}),
      datasets: [{
        data: Object.values(props.analyticsData.jobs_by_category || {}),
        backgroundColor: PIE_COLORS,
        borderColor: '#fff',
        borderWidth: 2
      }]
    }))

    const cityChartData = computed(() => ({
      labels: Object.keys(props.analyticsData.city_distribution || {}),
      datasets: [{
        label: 'Jobs',
        data: Object.values(props.analyticsData.city_distribution || {}),
        backgroundColor: BAR_COLOR,
        borderRadius: 6,
        borderSkipped: false
      }]
    }))

    const stateChartData = computed(() => ({
      labels: Object.keys(props.analyticsData.state_distribution || {}),
      datasets: [{
        label: 'Jobs',
        data: Object.values(props.analyticsData.state_distribution || {}),
        backgroundColor: BAR_COLOR,
        borderRadius: 6,
        borderSkipped: false
      }]
    }))

    return {
      cityCount, stateCount, categoryCount,
      hasStatusData, hasCityData, hasStateData, hasCategoryData,
      pieOptions, barOptions,
      statusChartData, categoryChartData, cityChartData, stateChartData
    }
  }
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal {
  background: #fff;
  border-radius: 12px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 16px 48px rgba(0,0,0,0.18);
  display: flex;
  flex-direction: column;
  animation: fadeUp 0.25s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
}

.modal-header h2 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #6b7280;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.close-btn:hover { background: #f3f4f6; color: #111827; }

/* Body */
.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Summary */
.summary-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.stat-card {
  border: 1.5px solid #e0e7ff;
  border-radius: 10px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #fafbff;
}

.stat-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #6b7280;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #4f46e5;
  line-height: 1;
}

/* Charts */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-box {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 20px;
  background: #fafafa;
}

.chart-wide {
  grid-column: span 1;
}

.chart-title {
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.chart-wrap {
  display: flex;
  justify-content: center;
  max-height: 220px;
}

.chart-wrap-bar {
  height: 200px;
  max-height: 200px;
  display: block;
}

.chart-wrap canvas {
  max-height: 220px;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 180px;
  font-size: 13px;
  color: #9ca3af;
}

/* Footer */
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  padding: 9px 20px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}

.btn-close:hover { background: #f9fafb; }

/* Responsive */
@media (max-width: 640px) {
  .overlay { padding: 0; align-items: flex-end; }
  .modal { max-width: 100%; border-radius: 12px 12px 0 0; max-height: 95vh; }
  .summary-row { grid-template-columns: 1fr 1fr; }
  .charts-grid { grid-template-columns: 1fr; }
  .chart-wide { grid-column: span 1; }
}
</style>