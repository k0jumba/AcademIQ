<template>
    <div class="courses-container">
        <h1>Courses</h1>
        <div class="courses-list">
            <router-link v-for="course in courses"
                         :key="course.id"
                         :to="{ name: 'CourseDetails', params: { course_slug: course.slug } }"
                         class="course-tile">
                <h2>{{ course.title }}</h2>
            </router-link>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                courses: [],
            };
        },
        async mounted() {
            try {
                const token = localStorage.getItem('authToken');
                const response = await axios.get('my_courses/', {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.courses = response.data;
            } catch (error) {
                console.error('Error fetching courses:', error);
            }
        },
    };
</script>

<style scoped>
    .courses-container {
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .courses-list {
        display: flex;
        flex-direction: column;
        width: 33%; /* Middle third of the screen */
    }

    .course-tile {
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

        .course-tile:hover {
            transform: scale(1.05);
        }

        .course-tile h2 {
            margin: 0;
            font-size: 18px;
        }
</style>
