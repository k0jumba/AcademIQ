<template>
    <div class="registration-page">
        <h1>Registration Page</h1>
        <form @submit.prevent="register">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="formData.username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="formData.password" required>
            </div>
            <div class="form-group">
                <label for="email">Email (optional):</label>
                <input type="email" id="email" v-model="formData.email">
            </div>
            <button type="submit">Register</button>
        </form>
        <p class="success-message" v-if="successMessage">{{ successMessage }}</p>
        <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
        <router-link to="/login">Go to Login Page</router-link>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                formData: {
                    username: '',
                    password: '',
                    email: ''
                },
                successMessage: '',
                errorMessage: ''
            };
        },
        methods: {
            async register() {
                this.successMessage = '';
                this.errorMessage = '';

                try {
                    const response = await axios.post('/auth/users/', this.formData);
                    this.successMessage = 'Registration successful. Please login.';
                    console.log('Registration successful:', response.data);
                } catch (error) {
                    this.errorMessage = 'Registration failed. Please try again.';
                    console.error('Registration failed:', error);
                }
            }
        }
    };
</script>

<style scoped>
    .registration-page {
        max-width: 400px;
        margin: 50px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    h1 {
        font-family: "Roboto", sans-serif;
        font-size: 24px;
        margin-bottom: 20px;
        text-align: center;
    }

    .form-group {
        margin-bottom: 15px;
    }

    label {
        font-family: "Roboto", sans-serif;
        font-weight: bold;
        display: block;
        margin-bottom: 5px;
    }

    input[type="text"],
    input[type="password"],
    input[type="email"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
    }

    button[type="submit"] {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .success-message {
        color: #28a745;
    }

    .error-message {
        color: #dc3545;
    }

    .registration-page a {
        display: block;
        text-align: center;
        margin-top: 20px;
        text-decoration: none;
        color: #007bff;
    }

        .registration-page a:hover {
            text-decoration: underline;
        }
</style>
