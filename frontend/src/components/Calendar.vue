<template>
  <div id="app">
    <div class="calendar-container">
      <h1>My Calendar</h1>
      <FullCalendar :options="calendarOptions" />
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  name: 'CalendarPage',
  components: {
    FullCalendar
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,dayGridWeek'
        },
        events: [
          {
            title: 'Sample Event',
            date: '2024-01-15'
          }
        ],
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick
      }
    }
  },
  methods: {
    handleDateClick(arg) {
      console.log('Date clicked:', arg.dateStr)
    },
    handleEventClick(arg) {
      console.log('Event clicked:', arg.event.title)
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
</style>