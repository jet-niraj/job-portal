<template>
  <div class="toast" :class="`toast-${type}`">
    <div class="toast-icon-wrap">
      <svg v-if="type === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      <svg v-else-if="type === 'error'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      <svg v-else-if="type === 'warning'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    </div>
    <span class="toast-message">{{ message }}</span>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  props: {
    message: { type: String, required: true },
    type: {
      type: String,
      default: 'success',
      validator: (v) => ['success', 'error', 'warning', 'info'].includes(v)
    }
  }
}
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 13px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  animation: slideIn 0.25s ease;
  max-width: 320px;
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid transparent;
  border-left-width: 4px;
}

@keyframes slideIn {
  from { transform: translateX(120%); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

.toast-icon-wrap {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.toast-message {
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
}

.toast-success {
  background: #f0fdf4;
  color: #166534;
  border-color: #86efac;
  border-left-color: #22c55e;
}

.toast-error {
  background: #fef2f2;
  color: #991b1b;
  border-color: #fca5a5;
  border-left-color: #ef4444;
}

.toast-warning {
  background: #fffbeb;
  color: #92400e;
  border-color: #fcd34d;
  border-left-color: #f59e0b;
}

.toast-info {
  background: #eff6ff;
  color: #1e40af;
  border-color: #93c5fd;
  border-left-color: #3b82f6;
}

@media (max-width: 480px) {
  .toast { left: 12px; right: 12px; bottom: 12px; max-width: 100%; }
}
</style>