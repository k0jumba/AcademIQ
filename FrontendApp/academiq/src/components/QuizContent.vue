<template>
    <div class="quiz-content">
        <h1>{{ contentData.title }}</h1>
        <p>{{ contentData.description }}</p>
        <hr>
        <div class="questions">
            <component v-for="question in contentData.questions"
                       :is="getQuestionComponent(question.question_type)"
                       :key="question.id"
                       :question="question"
                       @answer="handleAnswer"></component>
        </div>
        <button class="submit-button" @click="submitQuiz">Submit</button>
    </div>
</template>

<script>
    import axios from '../axios';
    import SingleChoiceQuestion from './SingleChoiceQuestion.vue';
    import MultipleChoiceQuestion from './MultipleChoiceQuestion.vue';
    import TextFieldQuestion from './TextFieldQuestion.vue';

    export default {
        components: {
            SingleChoiceQuestion,
            MultipleChoiceQuestion,
            TextFieldQuestion
        },
        props: {
            contentOrder: {
                type: Number,
                required: true
            }
        },
        data() {
            return {
                contentData: {},
                answers: []
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

                // Initialize answers array with default values
                this.answers = this.contentData.questions.map(question => ({
                    question_order: question.order,
                    answer: null
                }));
            } catch (error) {
                console.error('Error fetching quiz content data:', error);
            }
        },
        methods: {
            getQuestionComponent(questionType) {
                const componentMap = {
                    'SingleChoiceQuestion': 'SingleChoiceQuestion',
                    'MultipleChoiceQuestion': 'MultipleChoiceQuestion',
                    'TextFieldQuestion': 'TextFieldQuestion',
                    // Add more mappings as needed
                };
                return componentMap[questionType] || null;
            },
            handleAnswer({ questionOrder, answer }) {
                const answerIndex = this.answers.findIndex(a => a.question_order === questionOrder);
                if (answerIndex !== -1) {
                    this.answers[answerIndex].answer = answer;
                }
            },
            async submitQuiz() {
                const courseSlug = this.$route.params.course_slug;
                const assignmentId = this.contentData.assignment;
                const token = localStorage.getItem('authToken');

                try {
                    const response = await axios.post(`/courses/${courseSlug}/assignments/${assignmentId}/create_submission/`, {
                        submission_type: 'quiz',
                        submission_data: JSON.stringify(this.answers)
                    }, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    alert('Quiz submitted successfully!');
                    console.log('Quiz submitted successfully:', response.data);
                } catch (error) {
                    console.error('Error submitting quiz:', error);
                }
            }
        }
    };
</script>

<style scoped>
    .quiz-content {
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

    .questions {
        margin-bottom: 20px;
    }

    .submit-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }

        .submit-button:hover {
            background-color: #0056b3;
        }
</style>
