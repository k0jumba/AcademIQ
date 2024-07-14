<template>
    <div class="text-material">
        <h1>{{ contentData.title }}</h1>
        <p>{{ contentData.description }}</p>
        <hr>
        <div class="text-content">
            <p>{{ contentData.text }}</p>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        props: {
            contentOrder: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                contentData: {}
            };
        },
        async mounted() {
            try {
                const courseSlug = this.$route.params.course_slug;
                const lessonOrder = this.$route.params.lesson_order;
                const token = localStorage.getItem('authToken');

                const response = await axios.get(`/courses/${courseSlug}/lessons/${lessonOrder}/contents/${this.contentOrder}/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.contentData = response.data;
            } catch (error) {
                console.error('Error fetching content data:', error);
            }
        }
    };
</script>

<style scoped>
    .text-material {
        padding: 20px;
        max-width: 800px;
        margin: 20px auto;
        text-align: left;
    }

    h1 {
        font-size: 24px;
        margin-bottom: 10px;
    }

    p {
        font-size: 16px;
        line-height: 1.6;
    }

    hr {
        margin: 20px 0;
        border: none;
        border-top: 1px solid #e0e0e0;
    }

    .text-content p {
        white-space: pre-wrap; /* Preserves whitespace formatting */
    }
</style>
