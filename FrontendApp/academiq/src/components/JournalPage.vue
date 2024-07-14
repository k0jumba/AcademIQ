<template>
    <div class="journal-page">
        <h1>Course Journal</h1>
        <table class="journal-table">
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Name</th>
                    <th v-for="assignment in assignments" :key="assignment.id"
                        @mouseover="showTooltip($event, assignment)"
                        @mousemove="moveTooltip"
                        @mouseleave="hideTooltip">
                        {{ assignment.title }}
                        <div v-if="tooltip.assignment && tooltip.assignment.id === assignment.id"
                             class="tooltip" :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }">
                            <p><strong>Description:</strong> {{ assignment.description }}</p>
                            <p><strong>Weight:</strong> {{ assignment.weight }}</p>
                            <p><strong>Checkpoint:</strong> {{ assignment.is_checkpoint }}</p>
                        </div>
                    </th>
                    <th>Progress</th>
                    <th>Pass Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="entry in journalData" :key="entry.user.id">
                    <td>{{ entry.user.username }}</td>
                    <td>{{ entry.first_name }} {{ entry.last_name }}</td>
                    <td v-for="assignment in entry.assignments" :key="assignment.id"
                        :class="{ checkpoint: assignment.is_checkpoint }">
                        {{ assignment.grade ? assignment.grade.score : 'N/A' }}
                    </td>
                    <td>{{ entry.progress.toFixed(2) }}%</td>
                    <td :class="{ pass: entry.pass_status, fail: !entry.pass_status }">
                        {{ entry.pass_status ? 'Pass' : 'Fail' }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                journalData: [],
                assignments: [],
                tooltip: {
                    assignment: null,
                    x: 0,
                    y: 0
                }
            };
        },
        async mounted() {
            try {
                const courseSlug = this.$route.params.course_slug;
                const token = localStorage.getItem('authToken');

                const response = await axios.get(`/courses/${courseSlug}/grades_table/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.journalData = response.data;

                // Extract assignments details for table headers
                if (this.journalData.length > 0) {
                    this.assignments = this.journalData[0].assignments;
                }
            } catch (error) {
                console.error('Error fetching journal data:', error);
            }
        },
        methods: {
            showTooltip(event, assignment) {
                this.tooltip.assignment = assignment;
                this.moveTooltip(event);
            },
            moveTooltip(event) {
                this.tooltip.x = event.clientX + 10; // Shift to the right by 10px
                this.tooltip.y = event.clientY + 10; // Shift below the cursor by 10px
            },
            hideTooltip() {
                this.tooltip.assignment = null;
            }
        }
    };
</script>

<style scoped>
    .journal-page {
        padding: 20px;
        max-width: 1000px;
        margin: 20px auto;
        text-align: left;
    }

    h1 {
        font-size: 24px;
        margin-bottom: 20px;
    }

    .journal-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }

        .journal-table th, .journal-table td {
            border: 1px solid #e0e0e0;
            padding: 10px;
            text-align: left;
            position: relative;
        }

        .journal-table th {
            background-color: #f8f8f8;
        }

        .journal-table td.checkpoint {
            background-color: #fffbdd; /* Light yellow for checkpoints */
        }

        .journal-table td.pass {
            color: green;
            font-weight: bold;
        }

        .journal-table td.fail {
            color: red;
            font-weight: bold;
        }

    .tooltip {
        position: fixed;
        background-color: white;
        border: 1px solid #ccc;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        z-index: 10;
        white-space: nowrap;
        pointer-events: none; /* Ensure the tooltip itself doesn't trigger hover events */
    }

        .tooltip p {
            margin: 0;
            font-size: 14px;
        }
</style>
