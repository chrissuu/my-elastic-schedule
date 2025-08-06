<template>
  <div id="app">
    <div class="calendar-container">
      <h1>My Calendar</h1>
      <FullCalendar :options="calendarOptions" />
      
      <!-- Modal for Blob Form -->
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>Create New Blob</h2>
            <button @click="closeModal" class="close-btn">&times;</button>
          </div>
          
          <form @submit.prevent="submitBlob" class="blob-form">
            <div class="form-group">
              <label for="name">Name:</label>
              <input 
                type="text" 
                id="name" 
                v-model="blobForm.name" 
                required 
                placeholder="Enter blob name"
              />
            </div>
            
            <div class="form-group">
              <label for="description">Description:</label>
              <textarea 
                id="description" 
                v-model="blobForm.description" 
                placeholder="Enter description (optional)"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="timezone">Timezone:</label>
              <input 
                type="text" 
                id="timezone" 
                v-model="blobForm.tz" 
                placeholder="e.g., UTC, America/New_York"
              />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="default_start">Default Start:</label>
                <input 
                  type="datetime-local" 
                  id="default_start" 
                  v-model="blobForm.default_start"
                />
              </div>
              
              <div class="form-group">
                <label for="default_end">Default End:</label>
                <input 
                  type="datetime-local" 
                  id="default_end" 
                  v-model="blobForm.default_end"
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="schedulable_start">Schedulable Start:</label>
                <input 
                  type="datetime-local" 
                  id="schedulable_start" 
                  v-model="blobForm.schedulable_start"
                />
              </div>
              
              <div class="form-group">
                <label for="schedulable_end">Schedulable End:</label>
                <input 
                  type="datetime-local" 
                  id="schedulable_end" 
                  v-model="blobForm.schedulable_end"
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group checkbox-group">
                <label>
                  <input 
                    type="checkbox" 
                    v-model="blobForm.is_splittable"
                  />
                  Is Splittable
                </label>
              </div>
              
              <div class="form-group checkbox-group">
                <label>
                  <input 
                    type="checkbox" 
                    v-model="blobForm.is_overlappable"
                  />
                  Is Overlappable
                </label>
              </div>
              
              <div class="form-group checkbox-group">
                <label>
                  <input 
                    type="checkbox" 
                    v-model="blobForm.is_invisible"
                  />
                  Is Invisible
                </label>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="max_splits">Max Splits:</label>
                <input 
                  type="number" 
                  id="max_splits" 
                  v-model.number="blobForm.max_splits"
                  min="0"
                />
              </div>
              
              <div class="form-group">
                <label for="min_split_duration">Min Split Duration (minutes):</label>
                <input 
                  type="number" 
                  id="min_split_duration" 
                  v-model.number="blobForm.min_split_duration"
                  min="0"
                  step="15"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="dependencies">Dependencies (JSON):</label>
              <textarea 
                id="dependencies" 
                v-model="blobForm.dependencies" 
                placeholder="Enter dependencies as JSON array, e.g., []"
                rows="2"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="tags">Tags:</label>
              <input 
                type="text" 
                id="tags" 
                v-model="blobForm.tags" 
                placeholder="Enter tags separated by commas"
              />
            </div>
            
            <div class="form-actions">
              <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-submit">Create Blob</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  name: 'CalendarPage',
  components: {
    FullCalendar
  },
  data() {
    return {
      showModal: false,
      selectedRange: null,
      blobForm: {
        name: '',
        description: '',
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
        default_start: '',
        default_end: '',
        schedulable_start: '',
        schedulable_end: '',
        is_splittable: false,
        is_overlappable: false,
        is_invisible: false,
        max_splits: 0,
        min_split_duration: 0,
        dependencies: '[]',
        tags: ''
      },
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        nowIndicator: true,
        events: [
          {
            title: 'Sample Event',
            date: '2024-01-15'
          }
        ],
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick,
        select: this.handleSelect,
        // Selection settings
        selectable: true,
        selectMirror: true,
        snapDuration: '00:15:00',
      }
    }
  },
  mounted() {
    // Load existing blobs when component mounts
    this.loadBlobs()
  },
  methods: {
    handleDateClick(arg) {
      console.log('Date clicked:', arg.dateStr)
    },
    
    handleEventClick(arg) {
      console.log('Event clicked:', arg.event.title)
    },
    
    handleSelect(selectionInfo) {
      console.log('Time range selected:', selectionInfo)
      this.selectedRange = selectionInfo
      
      // Convert dates to datetime-local format for form inputs
      const startDateTime = this.formatDateTimeLocal(selectionInfo.start)
      const endDateTime = this.formatDateTimeLocal(selectionInfo.end)
      
      // Populate form with selected time range
      this.blobForm.default_start = startDateTime
      this.blobForm.default_end = endDateTime
      this.blobForm.schedulable_start = startDateTime
      this.blobForm.schedulable_end = endDateTime
      
      // Show the modal
      this.showModal = true
    },
    
    formatDateTimeLocal(date) {
      // Convert Date object to datetime-local format (YYYY-MM-DDTHH:mm)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      
      return `${year}-${month}-${day}T${hours}:${minutes}`
    },
    
    formatDateTimeISO(date) {
      // Convert Date object to ISO format for backend
      return date.toISOString()
    },
    
    closeModal() {
      this.showModal = false
      this.resetForm()
      
      // Clear calendar selection
      if (this.selectedRange) {
        const calendarApi = this.$refs.fullCalendar?.getApi()
        if (calendarApi) {
          calendarApi.unselect()
        }
      }
    },
    
    resetForm() {
      this.blobForm = {
        name: '',
        description: '',
        tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
        default_start: '',
        default_end: '',
        schedulable_start: '',
        schedulable_end: '',
        is_splittable: false,
        is_overlappable: false,
        is_invisible: false,
        max_splits: 0,
        min_split_duration: 0,
        dependencies: '[]',
        tags: ''
      }
      this.selectedRange = null
      console.log(`TIMEZONE: ${Intl.DateTimeFormat().resolvedOptions().timeZone}`);
    },
    
    async submitBlob() {
      try {
        let dependencies
        try {
          dependencies = JSON.parse(this.blobForm.dependencies)
        } catch (e) {
          alert('Invalid JSON format for dependencies')
          return
        }
        
        const tags = this.blobForm.tags
          .split(',')
          .map(tag => tag.trim())
          .filter(tag => tag.length > 0)
          .map(tag => ({ name: tag }));

        
        const blobData = {
          name: this.blobForm.name,
          description: this.blobForm.description,
          tz: this.blobForm.tz,
          default_start: this.formatDateTimeISO(new Date(this.blobForm.default_start)),
          default_end: this.formatDateTimeISO(new Date(this.blobForm.default_end)),
          schedulable_start: this.formatDateTimeISO(new Date(this.blobForm.schedulable_start)),
          schedulable_end: this.formatDateTimeISO(new Date(this.blobForm.schedulable_end)),
          is_splittable: this.blobForm.is_splittable,
          is_overlappable: this.blobForm.is_overlappable,
          is_invisible: this.blobForm.is_invisible,
          max_splits: this.blobForm.max_splits,
          min_split_duration: this.blobForm.min_split_duration * 60, // Convert minutes to seconds
          dependencies: dependencies,
          tags: tags
        }
        
        console.log('Blob data to submit:', blobData)
        
        // Make API call to create the blob
        const response = await fetch('http://localhost:8000/api/blobs/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken(),
          },
          body: JSON.stringify(blobData)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(`HTTP error! status: ${response.status}, details: ${JSON.stringify(errorData)}`)
        }
        
        const createdBlob = await response.json()
        console.log('Blob created successfully:', createdBlob)
        
        // Add the new blob as an event to the calendar
        this.addBlobToCalendar(createdBlob)
        
        alert('Blob created successfully!')
        this.closeModal()
        
      } catch (error) {
        console.error('Error creating blob:', error)
        alert(`Error creating blob: ${error.message}`)
      }
    },
    
    getCsrfToken() {
      // Get CSRF token from cookie if using CSRF protection
      const name = 'csrftoken'
      let cookieValue = null
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim()
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }
      return cookieValue
    },
    
    addBlobToCalendar(blob) {
      // Add the newly created blob as an event to the calendar
      const calendarApi = this.$refs.fullCalendar?.getApi()
      if (calendarApi) {
        calendarApi.addEvent({
          id: blob.id,
          title: blob.name,
          start: blob.default_start,
          end: blob.default_end,
          backgroundColor: blob.is_invisible ? 'transparent' : '#3498db',
          borderColor: blob.is_invisible ? '#ccc' : '#3498db',
          textColor: blob.is_invisible ? '#999' : '#fff'
        })
      }
    },
    
    async loadBlobs() {
      try {
        const response = await fetch('http://localhost:8000/api/blobs/')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const blobs = await response.json()
        
        // Convert blobs to calendar events
        const events = blobs.map(blob => ({
          id: blob.id,
          title: blob.name,
          start: blob.default_start,
          end: blob.default_end,
          backgroundColor: blob.is_invisible ? 'transparent' : '#3498db',
          borderColor: blob.is_invisible ? '#ccc' : '#3498db',
          textColor: blob.is_invisible ? '#999' : '#fff',
          constraint: {
            start: blob.schedulable_start,
            end: blob.schedulable_end
          },
          extendedProps: {
            blob: blob // Store full blob data
          }
        }))
        
        // Update calendar options with loaded events
        this.calendarOptions.events = events
        
      } catch (error) {
        console.error('Error loading blobs:', error)
      }
    }
  }
}
</script>

<style scoped>
.calendar-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

/* Form Styles */
.blob-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.checkbox-group {
  display: flex;
  align-items: center;
  min-width: fit-content;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

input[type="text"],
input[type="number"],
input[type="datetime-local"],
textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

input[type="checkbox"] {
  width: auto;
  margin: 0;
}

textarea {
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-cancel,
.btn-submit {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #5a6268;
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover {
  background-color: #0056b3;
}

/* Calendar Styles */
:deep(.fc-toolbar-title) {
  font-size: 1.5em;
  color: #2c3e50;
}

:deep(.fc-button-primary) {
  background-color: #3498db;
  border-color: #3498db;
}

:deep(.fc-button-primary:hover) {
  background-color: #2980b9;
  border-color: #2980b9;
}

:deep(.fc-highlight) {
  background-color: #3498db !important;
  opacity: 0.3;
}
</style>