<template>
    <div class="lessons-container">
        <h1>Lessons</h1>
        <div class="lessons-list">
            <router-link v-for="lesson in lessons" 
                         :key="lesson.id"
                         :to="{name: 'LessonPage', params: { lesson_order: lesson.order }}"
                         class="lesson-tile">
                <h2>{{ lesson.title }}</h2>
            </router-link>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                lessons: [],
            };
        },
        async mounted() {
            const courseSlug = this.$route.params.course_slug;
            try {
                const token = localStorage.getItem('authToken');
                const response = await axios.get(`/courses/${courseSlug}/lessons/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.lessons = response.data.sort((a, b) => a.order - b.order);
            } catch (error) {
                console.error('Error fetching lessons:', error);
            }
        },
    };
</script>

<style scoped>
    .lessons-container {
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .lessons-list {
        display: flex;
        flex-direction: column;
        width: 100%; /* Full width */
        max-width: 800px; /* Max width for larger screens */
    }

    .lesson-tile {
        background-color: #f8f8f8;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s;
        text-decoration: none; /* Remove underline from links */
        color: inherit; /* Inherit text color */
    }

        .lesson-tile:hover {
            transform: scale(1.02);
        }

        .lesson-tile h2 {
            margin: 0;
            font-size: 18px;
        }
</style>
