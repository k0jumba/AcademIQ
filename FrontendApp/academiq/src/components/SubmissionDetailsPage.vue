<template>
    <div class="submission-details-page">
        <h1>Submission Details</h1>
        <div v-if="submission">
            <p><strong>Author:</strong> {{ submission.author.first_name }} {{ submission.author.last_name }} ({{ submission.author.user.username }})</p>
            <p><strong>Created:</strong> {{ new Date(submission.created).toLocaleString() }}</p>
            <p><strong>Submission Type:</strong> {{ submission.submission_type }}</p>
            <h3>Submission Data:</h3>
            <ul>
                <li v-for="(answer, index) in parsedSubmissionData" :key="index">
                    <strong>Question {{ answer.question_order }}:</strong>
                    <span v-if="Array.isArray(answer.answer)">{{ answer.answer.join(', ') }}</span>
                    <span v-else>{{ answer.answer }}</span>
                </li>
            </ul>
        </div>
        <div v-else>
            <p>Loading...</p>
        </div>
        <h3>Grade Submission</h3>
        <form @submit.prevent="submitGrade">
            <div>
                <label for="score">Score (0-100):</label>
                <input type="number" v-model="score" min="0" max="100" required />
            </div>
            <button type="submit">Submit Grade</button>
        </form>
    </div>
</template>

<script>
    import axios from '../axios'; // Adjust the path as needed

    export default {
        data() {
            return {
                submission: null,
                score: 0
            };
        },
        computed: {
            courseSlug() {
                return this.$route.params.course_slug;
            },
            submissionId() {
                return this.$route.params.submission_id;
            },
            parsedSubmissionData() {
                try {
                    return JSON.parse(this.submission.submission_data);
                } catch (e) {
                    return [];
                }
            }
        },
        async created() {
            await this.fetchSubmission();
        },
        methods: {
            async fetchSubmission() {
                const token = localStorage.getItem('authToken');
                try {
                    const response = await axios.get(`/courses/${this.courseSlug}/submissions/${this.submissionId}/`, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    this.submission = response.data;
                } catch (error) {
                    console.error('Error fetching submission details:', error);
                }
            },
            async submitGrade() {
                const token = localStorage.getItem('authToken');
                try {
                    await axios.post(`/courses/${this.courseSlug}/create_grade/`, {
                        student: this.submission.author.id,
                        assignment: this.submission.assignment,
                        score: this.score
                    }, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    alert('Grade submitted successfully');
                } catch (error) {
                    console.error('Error submitting grade:', error);
                    alert('Failed to submit grade');
                }
            }
        }
    };
</script>

<style scoped>
    .submission-details-page {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }

    h1, h3 {
        margin-bottom: 10px;
    }

    p {
        margin: 5px 0;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        margin: 5px 0;
    }

    form {
        margin-top: 20px;
    }

        form div {
            margin-bottom: 10px;
        }

    label {
        display: block;
        margin-bottom: 5px;
    }

    input {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
    }

    button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        font-size: 16px;
    }

        button:hover {
            background-color: #0056b3;
        }
</style>
