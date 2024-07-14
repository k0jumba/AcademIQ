<template>
    <div class="login-container">
        <h1>Login</h1>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" v-model="username" required />
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" v-model="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
        <div v-if="error" class="error-message">
            {{ error }}
        </div>
        <router-link to="/register">Go to Register Page</router-link>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                username: '',
                password: '',
                error: null,
            };
        },
        methods: {
            async login() {
                try {
                    const response = await axios.post('/auth/token/login', {
                        username: this.username,
                        password: this.password,
                    });
                    localStorage.setItem('authToken', response.data.auth_token);
                    this.$router.push('/');
                } catch (err) {
                    console.error('Logout failed:', err);
                    this.error = 'Login failed. Please try again.';
                }
            },
        },
    };
</script>

<style scoped>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
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

    input {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
    }

    button {
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    .error-message {
        margin-top: 10px;
        color: red;
    }

    .login-container a {
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
