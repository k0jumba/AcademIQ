<template>
    <div class="lesson-page">
        <h1>{{ lessonTitle }}</h1>
        <div class="tabs">
            <div v-for="content in lessonContents"
                 :key="content.order"
                 :class="['tab', { active: activeTab === content.order }]"
                 @click="setActiveTab(content)">
                {{ content.title }}
            </div>
        </div>
        <div class="content">
            <component v-if="activeContent"
                       :is="activeContentComponent"
                       :contentOrder="activeContent.order"
                       :key="activeContent.id"></component>
            <div v-else>
                <p>Select a tab to view content</p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';
    import TextContent from './TextContent.vue';
    import QuizContent from './QuizContent.vue';

    export default {
        components: {
            TextContent,
            QuizContent
        },
        data() {
            return {
                lessonTitle: '',
                lessonContents: [],
                activeContent: null,
                activeContentComponent: null,
                activeTab: null,
            };
        },
        async mounted() {
            const courseSlug = this.$route.params.course_slug;
            const lessonOrder = this.$route.params.lesson_order;
            try {
                const token = localStorage.getItem('authToken');

                // Fetch lesson contents
                const response = await axios.get(`/courses/${courseSlug}/lessons/${lessonOrder}/contents/`, {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                this.lessonContents = response.data;

                // Set the lesson title
                this.lessonTitle = `Lesson ${lessonOrder}`;

                // Optionally, set the first tab as active by default
                if (this.lessonContents.length > 0) {
                    this.setActiveTab(this.lessonContents[0]);
                }

            } catch (error) {
                console.error('Error fetching lesson contents:', error);
            }
        },
        methods: {
            setActiveTab(content) {
                this.activeContent = content;
                this.activeTab = content.order;
                this.activeContentComponent = this.getComponentForContentType(content.content_type);
            },
            getComponentForContentType(contentType) {
                const componentMap = {
                    'TextContent': 'TextContent',
                    'QuizContent': 'QuizContent',
                    // Add more mappings as needed
                };
                return componentMap[contentType] || null;
            }
        }
    };
</script>

<style scoped>
    .lesson-page {
        padding: 20px;
        max-width: 800px;
        margin: 20px auto;
        text-align: left;
    }

    h1 {
        font-size: 24px;
        margin-bottom: 20px;
    }

    .tabs {
        display: flex;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    .tab {
        padding: 10px 20px;
        cursor: pointer;
        border: 1px solid transparent;
        border-bottom: none;
        transition: background-color 0.2s, border-color 0.2s;
    }

        .tab:hover {
            background-color: #f0f0f0;
        }

        .tab.active {
            border: 1px solid #e0e0e0;
            border-bottom: 1px solid white;
            background-color: #f8f8f8;
        }

    .content {
        padding: 20px;
        border: 1px solid #e0e0e0;
        background-color: white;
    }
</style>
