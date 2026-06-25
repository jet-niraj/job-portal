<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="dialog">
      <!-- Header -->
      <div class="dialog-header">
        <h2>{{ isEditing ? 'Edit Job' : 'Post New Job' }}</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="dialog-form">

        <!-- Job Title -->
        <div class="field full">
          <label for="job_title">Job Title <span class="req">*</span></label>
          <input id="job_title" v-model="formData.job_title" type="text" placeholder="e.g., Senior Python Developer" />
          <p v-if="errors.job_title" class="err">{{ errors.job_title }}</p>
        </div>

        <!-- Status & Category -->
        <div class="row">
          <div class="field">
            <label for="status">Status <span class="req">*</span></label>
            <select id="status" v-model="formData.status">
              <option value="">Select</option>
              <option value="draft">Draft</option>
              <option value="requested">Requested</option>
              <option value="posted">Posted</option>
              <option value="filled">Filled</option>
            </select>
            <p v-if="errors.status" class="err">{{ errors.status }}</p>
          </div>

          <div class="field">
            <label for="category">Category <span class="req">*</span></label>
            <select id="category" v-model="formData.category">
              <option value="">Select</option>
              <option value="full_time">Full-time</option>
              <option value="part_time">Part-time</option>
              <option value="intern">Intern</option>
              <option value="contract">Contract</option>
              <option value="temporary">Temporary</option>
            </select>
            <p v-if="errors.category" class="err">{{ errors.category }}</p>
          </div>
        </div>

        <!-- Address -->
        <div class="field full">
          <label for="address">Address <span class="req">*</span></label>
          <input id="address" v-model="formData.address" type="text" placeholder="e.g., 123 Tech Street, Bandra" />
          <p v-if="errors.address" class="err">{{ errors.address }}</p>
        </div>

        <!-- City & State -->
        <div class="row">
          <div class="field">
            <label for="city">City <span class="req">*</span></label>
            <input id="city" v-model="formData.city" type="text" placeholder="Mumbai" />
            <p v-if="errors.city" class="err">{{ errors.city }}</p>
          </div>

          <div class="field">
            <label for="state">State <span class="req">*</span></label>
            <input id="state" v-model="formData.state" type="text" placeholder="Maharashtra" />
            <p v-if="errors.state" class="err">{{ errors.state }}</p>
          </div>
        </div>

        <!-- Dates -->
        <div class="row">
          <div class="field">
            <label for="start_date">Start Date <span class="req">*</span></label>
            <input id="start_date" v-model="formData.start_date" type="date" />
            <p v-if="errors.start_date" class="err">{{ errors.start_date }}</p>
          </div>

          <div class="field">
            <label for="end_date">End Date</label>
            <input id="end_date" v-model="formData.end_date" type="date" />
            <p v-if="errors.end_date" class="err">{{ errors.end_date }}</p>
          </div>
        </div>

        <!-- Description -->
        <div class="field full">
          <label for="description">Description <span class="req">*</span></label>
          <textarea id="description" v-model="formData.description" rows="4" placeholder="Describe the role and responsibilities..."></textarea>
          <p v-if="errors.description" class="err">{{ errors.description }}</p>
        </div>

        <!-- Image Upload -->
        <div class="field full">
          <label>Profile Picture</label>
          <div
            class="upload-area"
            @click="$refs.fileInput.click()"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <p>Click or drag an image here</p>
            <span class="upload-hint">JPG, PNG, GIF, WebP — max 5MB</span>
            <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" hidden />
          </div>

          <div v-if="imagePreview" class="preview">
            <img :src="imagePreview" alt="Preview" />
            <button type="button" class="remove-btn" @click="removeImage">Remove</button>
          </div>

          <p v-if="errors.job_profile_picture" class="err">{{ errors.job_profile_picture }}</p>
        </div>

        <!-- Actions -->
        <div class="actions">
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn-submit" :disabled="submitting">
            {{ submitting ? 'Saving...' : (isEditing ? 'Update Job' : 'Create Job') }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

export default {
  name: 'CreateJobDialog',
  props: {
    job: { type: Object, default: null },
    filterOptions: { type: Object, default: () => ({}) }
  },
  emits: ['save', 'close'],
  setup(props, { emit }) {
    const formData = ref({
      job_title: '',
      status: '',
      category: '',
      address: '',
      city: '',
      state: '',
      start_date: '',
      end_date: '',
      description: '',
      job_profile_picture: null
    })

    const imagePreview = ref('')
    const errors = ref({})
    const submitting = ref(false)
    const imageRemoved = ref(false)
    const isEditing = computed(() => !!props.job)

    // Normalize date: strips time part from ISO strings so date input works
    const toDateInput = (val) => {
      if (!val) return ''
      if (typeof val === 'string' && val.includes('T')) return val.split('T')[0]
      return val
    }

    watch(() => props.job, (newJob) => {
      if (newJob) {
        formData.value = {
          ...newJob,
          // Use raw status/category values (not display names) for selects
          status: newJob.status || '',
          category: newJob.category || '',
          // Normalize dates for HTML date input
          start_date: toDateInput(newJob.start_date),
          end_date: toDateInput(newJob.end_date),
          // Keep picture as-is; only replaced if user uploads new one
          job_profile_picture: newJob.job_profile_picture || null
        }
        if (newJob.job_profile_picture) {
          imagePreview.value = newJob.job_profile_picture
        }
        imageRemoved.value = false
      }
    }, { immediate: true })

    const validateAndSetImage = (file) => {
      const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
      if (!validTypes.includes(file.type)) {
        errors.value.job_profile_picture = 'Please upload JPG, PNG, GIF, or WebP.'
        return
      }
      if (file.size > 5 * 1024 * 1024) {
        errors.value.job_profile_picture = 'Image must be under 5MB.'
        return
      }
      const reader = new FileReader()
      reader.onload = (e) => {
        imagePreview.value = e.target.result
        formData.value.job_profile_picture = file
        errors.value.job_profile_picture = ''
      }
      reader.readAsDataURL(file)
    }

    const handleFileSelect = (e) => {
      const file = e.target.files[0]
      if (file) validateAndSetImage(file)
    }

    const handleDrop = (e) => {
      const file = e.dataTransfer.files[0]
      if (file) validateAndSetImage(file)
    }

    const removeImage = () => {
      formData.value.job_profile_picture = null
      imagePreview.value = ''
      imageRemoved.value = true
    }

    const validateForm = () => {
      errors.value = {}
      if (!formData.value.job_title?.trim()) errors.value.job_title = 'Job title is required.'
      if (!formData.value.status) errors.value.status = 'Status is required.'
      if (!formData.value.category) errors.value.category = 'Category is required.'
      if (!formData.value.address?.trim()) errors.value.address = 'Address is required.'
      if (!formData.value.city?.trim()) errors.value.city = 'City is required.'
      if (!formData.value.state?.trim()) errors.value.state = 'State is required.'
      if (!formData.value.start_date) errors.value.start_date = 'Start date is required.'
      if (!formData.value.description?.trim()) errors.value.description = 'Description is required.'
      if (formData.value.end_date && formData.value.start_date) {
        if (new Date(formData.value.end_date) < new Date(formData.value.start_date)) {
          errors.value.end_date = 'End date cannot be before start date.'
        }
      }
      return Object.keys(errors.value).length === 0
    }

    const handleSubmit = async () => {
      if (!validateForm()) return
      submitting.value = true
      try {
        const data = new FormData()
        data.append('job_title', formData.value.job_title)
        data.append('status', formData.value.status)
        data.append('category', formData.value.category)
        data.append('address', formData.value.address)
        data.append('city', formData.value.city)
        data.append('state', formData.value.state)
        data.append('start_date', formData.value.start_date)
        data.append('end_date', formData.value.end_date || '')
        data.append('description', formData.value.description)
        if (formData.value.job_profile_picture instanceof File) {
          data.append('job_profile_picture', formData.value.job_profile_picture)
        } else if (imageRemoved.value) {
          // Explicitly tell backend to clear the image
          data.append('job_profile_picture', '')
        }
        emit('save', data)
      } finally {
        submitting.value = false
      }
    }

    return {
      formData, imagePreview, imageRemoved, errors, submitting, isEditing,
      handleFileSelect, handleDrop, removeImage, handleSubmit
    }
  }
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.dialog {
  background: #fff;
  border-radius: 8px;
  width: 100%;
  max-width: 580px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
}

.dialog-header {
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

.dialog-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.close-btn:hover {
  color: #111827;
}

.dialog-form {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.full {
  width: 100%;
}

.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.req {
  color: #ef4444;
}

input,
select,
textarea {
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  color: #111827;
  background: #fff;
  font-family: inherit;
  transition: border-color 0.15s;
  width: 100%;
  box-sizing: border-box;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

textarea {
  resize: vertical;
  min-height: 96px;
}

.err {
  margin: 0;
  font-size: 12px;
  color: #dc2626;
}

/* Upload */
.upload-area {
  border: 1.5px dashed #d1d5db;
  border-radius: 6px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  background: #f9fafb;
  transition: border-color 0.15s;
}

.upload-area:hover {
  border-color: #4f46e5;
}

.upload-area p {
  margin: 0 0 4px;
  font-size: 14px;
  color: #374151;
}

.upload-hint {
  font-size: 12px;
  color: #9ca3af;
}

.preview {
  margin-top: 12px;
  position: relative;
  display: inline-block;
}

.preview img {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.remove-btn {
  margin-top: 6px;
  background: none;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  color: #6b7280;
}

.remove-btn:hover {
  color: #dc2626;
  border-color: #dc2626;
}

/* Actions */
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  padding: 9px 18px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #f3f4f6;
}

.btn-submit {
  padding: 9px 20px;
  border: none;
  border-radius: 6px;
  background: #4f46e5;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-submit:hover:not(:disabled) {
  background: #4338ca;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 560px) {
  .overlay {
    padding: 0;
    align-items: flex-end;
  }

  .dialog {
    max-width: 100%;
    border-radius: 12px 12px 0 0;
    max-height: 95vh;
  }

  .row {
    grid-template-columns: 1fr;
  }
}
</style>