<template>
    <div class="submissions-page">
        <h1>Choose Assignment</h1>
        <div class="assignments-list">
            <router-link v-for="assignment in assignments"
                         :key="assignment.id"
                         :to="{ name: 'AssignmentSubmissions', params: { course_slug: $route.params.course_slug, assignment_id: assignment.id }}"
                         class="assignment-tile">
                {{ assignment.title }}
            </router-link>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                assignments: []
            };
        },
        async mounted() {
            try {
                const courseSlug = this.$route.params.course_slug;
                const token = localStorage.getItem('authToken');

                const response = await axios.get(`/courses/${courseSlug}/assignments/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.assignments = response.data;
            } catch (error) {
                console.error('Error fetching assignments:', error);
            }
        }
    };
</script>

<style scoped>
    .submissions-page {
        padding: 20px;
        max-width: 800px;
        margin: 20px auto;
        text-align: left;
    }

    .assignments-list {
        margin-top: 20px;
    }

    .assignment-tile {
        padding: 10px 15px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        background-color: #f8f8f8;
        cursor: pointer;
        transition: background-color 0.3s;
        display: block;
        text-decoration: none;
        color: inherit;
    }

        .assignment-tile:hover {
            background-color: #e0e0e0;
        }

    .access-denied {
        padding: 20px;
        text-align: center;
        color: red;
    }
</style>
