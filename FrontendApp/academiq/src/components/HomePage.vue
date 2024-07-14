<template>
    <div>
        <nav class="navbar">
            <div class="nav-left">
                <router-link to="/" class="home-button">Home</router-link>
                <router-link to="/courses" class="courses-button">Courses</router-link>
            </div>
            <div class="nav-right">
                <div ref="profileMenu" class="profile-menu" @click="toggleMenu">
                    <button class="profile-button">Profile</button>
                    <div v-if="menuOpen" class="dropdown-menu" @click.stop>
                        <router-link to="/profile" class="dropdown-item">Profile</router-link>
                        <router-link to="/my_courses" class="dropdown-item">My Courses</router-link>
                        <button @click="logout" class="logout-button">Log out</button>
                    </div>
                </div>
            </div>
        </nav>
        <div class="content">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import axios from '../axios';

    export default {
        data() {
            return {
                menuOpen: false,
            };
        },
        mounted() {
            document.addEventListener('click', this.closeMenu);
        },
        beforeUnmount() {
            document.removeEventListener('click', this.closeMenu);
        },
        methods: {
            toggleMenu() {
                this.menuOpen = !this.menuOpen;
            },
            closeMenu(event) {
                const profileMenu = this.$refs.profileMenu;
                if (!profileMenu.contains(event.target)) {
                    this.menuOpen = false;
                }
            },
            async logout() {
                const token = localStorage.getItem('authToken');
                try {
                    await axios.post('/auth/token/logout/', {}, {
                        headers: {
                            Authorization: `Token ${token}`,
                        },
                    });
                    localStorage.removeItem('authToken');
                    this.$router.push('/login');
                } catch (error) {
                    console.error('Logout failed:', error);
                }
            },
        },
    };
</script>

<style scoped>
    .navbar {
        display: flex;
        justify-content: space-between;
        padding: 10px 20px;
        background-color: #f8f8f8;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .nav-left {
        display: flex;
        align-items: center;
    }

    .home-button {
        text-decoration: none;
        color: #007bff;
        font-size: 16px;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        background-color: transparent;
        cursor: pointer;
    }

        .home-button:hover {
            background-color: #e0e0e0;
        }

    .courses-button {
        text-decoration: none;
        color: #007bff;
        font-size: 16px;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        background-color: transparent;
        cursor: pointer;
    }

        .courses-button:hover {
            background-color: #e0e0e0;
        }

    .nav-right {
        display: flex;
        align-items: center;
    }

    .profile-menu {
        position: relative;
    }

    .profile-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
    }

    .dropdown-menu {
        position: absolute;
        right: 0;
        top: 100%;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        margin-top: 5px;
        padding: 10px;
        z-index: 1000;
    }

    .dropdown-item {
        display: block;
        padding: 5px 10px;
        color: #007bff;
        text-decoration: none;
        border: none;
        background: none;
        text-align: left;
        width: 100%;
        cursor: pointer;
    }

        .dropdown-item:hover {
            background-color: #f0f0f0;
        }

    .logout-button {
        color: red; /* Changed text color to red */
        background: none;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
        width: 100%;
        text-align: left;
        font-size: 14px; /* Adjusted font size */
    }

        .logout-button:hover {
            background-color: #f0f0f0;
        }

    .content {
        padding: 20px;
    }
</style>
