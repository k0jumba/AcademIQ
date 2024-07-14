<template>
    <div class="course-page">
        <div :class="['sidebar', { 'sidebar-collapsed': !sidebarOpen }]">
            <button @click="toggleSidebar" class="toggle-button">
                {{ sidebarOpen ? '❮' : '❯' }}
            </button>
            <div v-if="sidebarOpen" class="sidebar-content">
                <router-link :to="{ name: 'Lessons', params: { course_slug: $route.params.course_slug }}">Lessons</router-link>
                <router-link :to="{ name: 'Journal', params: { course_slug: $route.params.course_slug }}">Journal</router-link>
                <router-link v-if="isEducator" :to="{ name: 'AssignmentsPage', params: { course_slug: $route.params.course_slug }}">Assignments</router-link>
                <!-- Add more links as needed -->
            </div>
        </div>
        <div class="content">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import axios from '../axios'; // Adjust the path as needed

    export default {
        data() {
            return {
                sidebarOpen: true,
                isEducator: false
            };
        },
        async created() {
            const token = localStorage.getItem('authToken');
            try {
                const response = await axios.get('/profile/', {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                if (response.data.educator) {
                    this.isEducator = true;
                }
            } catch (error) {
                console.error('Error fetching profile data:', error);
            }
        },
        methods: {
            toggleSidebar() {
                this.sidebarOpen = !this.sidebarOpen;
            },
        },
    };
</script>

<style scoped>
    .course-page {
        display: flex;
    }

    .sidebar {
        background-color: #f8f8f8;
        border-right: 1px solid #e0e0e0;
        padding: 20px;
        transition: width 0.3s;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .sidebar-collapsed {
        width: 40px;
    }

    .sidebar:not(.sidebar-collapsed) {
        width: 20%; /* Adjust the width as needed */
        max-width: 250px;
    }

    .toggle-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        text-align: left;
        margin-bottom: 20px;
    }

    .sidebar-content {
        display: flex;
        flex-direction: column;
        width: 100%;
    }

        .sidebar-content a {
            margin-bottom: 10px;
            color: #007bff;
            text-decoration: none;
            width: 100%;
        }

            .sidebar-content a:hover {
                text-decoration: underline;
            }

    .content {
        flex-grow: 1;
        padding: 20px;
    }
</style>
