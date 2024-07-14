<template>
    <div class="course-container">
        <h1>{{ course.title }}</h1>
        <p>{{ course.description }}</p>
        <button v-if="!isEducator" @click="toggleSubscription" class="subscribe-button">
            {{ course.is_subscribed ? 'Unsubscribe' : 'Subscribe' }}
        </button>
        <button v-if="course.is_subscribed" @click="goToCoursePage" class="course-page-button">
            Go to Course Page
        </button>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                course: {},
                isEducator: true,
            };
        },
        async mounted() {
            const courseSlug = this.$route.params.course_slug;
            try {
                const token = localStorage.getItem('authToken');

                // Fetch course data
                const courseResponse = await axios.get(`/courses/${courseSlug}/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.course = courseResponse.data;

                // Fetch user profile data to check if the user is an educator
                const profileResponse = await axios.get('/profile/', {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.isEducator = !!profileResponse.data.educator;
            } catch (error) {
                console.error('Error fetching course or profile data:', error);
            }
        },
        methods: {
            async toggleSubscription() {
                const courseSlug = this.$route.params.course_slug;
                const token = localStorage.getItem('authToken');
                const url = this.course.is_subscribed
                    ? `/courses/${courseSlug}/unsubscribe/`
                    : `/courses/${courseSlug}/subscribe/`;

                try {
                    await axios.post(url, {}, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    this.course.is_subscribed = !this.course.is_subscribed;
                } catch (error) {
                    console.error('Error changing subscription status:', error);
                }
            },
            goToCoursePage() {
                const courseSlug = this.$route.params.course_slug;
                this.$router.push({ name: 'CoursePage', params: { course_slug: courseSlug } });
            }
        }
    };
</script>

<style scoped>
    .course-container {
        padding: 20px;
        max-width: 800px;
        margin: 20px auto; /* Center align and added margin */
        text-align: left; /* Align text to the left */
    }

    h1 {
        font-size: 24px;
        margin-bottom: 10px;
    }

    p {
        font-size: 16px;
        line-height: 1.6;
    }

    .subscribe-button,
    .course-page-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 20px;
        margin-right: 10px; /* Add margin between buttons */
    }

        .subscribe-button:hover,
        .course-page-button:hover {
            background-color: #0056b3;
        }
</style>
