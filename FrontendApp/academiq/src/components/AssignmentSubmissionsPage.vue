<template>
    <div class="submissions-page">
        <h1>Submissions for Assignment {{ assignmentId }}</h1>
        <table>
            <thead>
                <tr>
                    <th>Author</th>
                    <th>Username</th>
                    <th>Created</th>
                    <th>Submission Type</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="submission in submissions" :key="submission.id">
                    <td>{{ submission.author.first_name }} {{ submission.author.last_name }}</td>
                    <td>{{ submission.author.user.username }}</td>
                    <td>{{ new Date(submission.created).toLocaleString() }}</td>
                    <td>{{ submission.submission_type }}</td>
                    <td><router-link :to="{ name: 'SubmissionDetails', params: { submission_id: submission.id }}">See Details</router-link></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from '../axios'; // Adjust the path as needed

    export default {
        data() {
            return {
                submissions: []
            };
        },
        computed: {
            courseSlug() {
                return this.$route.params.course_slug;
            },
            assignmentId() {
                return this.$route.params.assignment_id;
            }
        },
        async created() {
            await this.fetchSubmissions();
        },
        methods: {
            async fetchSubmissions() {
                const token = localStorage.getItem('authToken');
                try {
                    const response = await axios.get(`/courses/${this.courseSlug}/assignments/${this.assignmentId}/submissions/`, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    this.submissions = response.data;
                } catch (error) {
                    console.error('Error fetching submissions:', error);
                }
            }
        }
    };
</script>

<style scoped>
    .submissions-page {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    th, td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }

    th {
        background-color: #f4f4f4;
    }

    tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    tr:hover {
        background-color: #f1f1f1;
    }

    .router-link {
        color: #007bff;
        text-decoration: none;
    }

        .router-link:hover {
            text-decoration: underline;
        }
</style>
