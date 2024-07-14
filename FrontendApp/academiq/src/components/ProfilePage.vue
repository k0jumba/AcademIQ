<template>
    <div class="profile-page">
        <h1>Profile Page</h1>
        <div class="profile-section">
            <div class="field">
                <label>ID:</label>
                <span>{{ profile.id }}</span>
            </div>
            <div class="field">
                <label>Username:</label>
                <span>{{ profile.username }}</span>
            </div>
        </div>
        <div class="delimiter"></div>
        <div v-if="profile.student" class="profile-section">
            <h2>Student Info</h2>
            <div v-if="!editMode">
                <div class="field">
                    <label>First Name:</label>
                    <span>{{ profile.student.first_name }}</span>
                </div>
                <div class="field">
                    <label>Last Name:</label>
                    <span>{{ profile.student.last_name }}</span>
                </div>
                <button @click="editMode = true">Edit</button>
            </div>
            <div v-else>
                <div class="field">
                    <label for="first_name">First Name:</label>
                    <input type="text" id="first_name" v-model="editData.first_name">
                </div>
                <div class="field">
                    <label for="last_name">Last Name:</label>
                    <input type="text" id="last_name" v-model="editData.last_name">
                </div>
                <button @click="saveChanges">Save</button>
                <button @click="cancelEdit">Cancel</button>
                <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
            </div>
        </div>
        <div v-if="profile.educator" class="profile-section">
            <h2>Educator Info</h2>
            <div v-if="!editMode">
                <div class="field">
                    <label>First Name:</label>
                    <span>{{ profile.educator.first_name }}</span>
                </div>
                <div class="field">
                    <label>Last Name:</label>
                    <span>{{ profile.educator.last_name }}</span>
                </div>
                <button @click="editMode = true">Edit</button>
            </div>
            <div v-else>
                <div class="field">
                    <label for="first_name">First Name:</label>
                    <input type="text" id="first_name" v-model="editData.first_name">
                </div>
                <div class="field">
                    <label for="last_name">Last Name:</label>
                    <input type="text" id="last_name" v-model="editData.last_name">
                </div>
                <button @click="saveChanges">Save</button>
                <button @click="cancelEdit">Cancel</button>
                <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                profile: {},
                editMode: false,
                editData: {
                    first_name: '',
                    last_name: ''
                },
                errorMessage: ''
            };
        },
        async created() {
            await this.fetchProfile();
        },
        methods: {
            async fetchProfile() {
                try {
                    const token = localStorage.getItem('authToken');
                    const response = await axios.get('profile/', {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });
                    this.profile = response.data;
                } catch (error) {
                    console.error('Failed to fetch profile:', error);
                }
            },
            editProfile() {
                this.editData.first_name = this.profile.student ? this.profile.student.first_name : this.profile.educator.first_name;
                this.editData.last_name = this.profile.student ? this.profile.student.last_name : this.profile.educator.last_name;
            },
            async saveChanges() {
                try {
                    const token = localStorage.getItem('authToken');
                    const response = await axios.put('profile/', {
                        first_name: this.editData.first_name,
                        last_name: this.editData.last_name
                    }, {
                        headers: {
                            Authorization: `Token ${token}`
                        }
                    });

                    if (this.profile.student) {
                        this.profile.student.first_name = response.data.first_name;
                        this.profile.student.last_name = response.data.last_name;
                    } else if (this.profile.educator) {
                        this.profile.educator.first_name = response.data.first_name;
                        this.profile.educator.last_name = response.data.last_name;
                    }

                    this.editMode = false;
                    this.errorMessage = '';
                } catch (error) {
                    this.errorMessage = 'Failed to save changes. Please try again.';
                    console.error('Failed to save changes:', error);
                }
            },
            cancelEdit() {
                this.editMode = false;
                this.errorMessage = '';
            }
        },
        watch: {
            editMode(newVal) {
                if (newVal) {
                    this.editProfile();
                }
            }
        }
    };
</script>

<style scoped>
    .profile-page {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #f9f9f9;
    }

    h1 {
        font-size: 24px;
        margin-bottom: 20px;
        text-align: center;
    }

    h2 {
        font-size: 20px;
        margin-top: 20px;
    }

    .profile-section {
        margin-bottom: 20px;
    }

    .field {
        margin-bottom: 10px;
    }

    label {
        font-weight: bold;
    }

    input[type="text"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
    }

    button {
        padding: 10px 20px;
        margin-right: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

        button:hover {
            opacity: 0.9;
        }

    .delimiter {
        height: 1px;
        background-color: #ccc;
        margin: 20px 0;
    }

    .error-message {
        color: #dc3545;
    }

    .profile-button {
        background-color: #007bff;
        color: white;
    }

        .profile-button:hover {
            background-color: #0056b3;
        }
</style>
