import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import SignIn from './components/SignIn.vue';
import SignUp from './components/SignUp.vue'
import ProfilePage from './components/ProfilePage.vue'
import HomeContent from './components/HomeContent.vue'
import CoursesPage from './components/CoursesPage.vue'
import CoursePage from './components/CoursePage.vue'
import CourseDetailsPage from './components/CourseDetailsPage.vue'
import MyCoursesPage from './components/MyCoursesPage.vue'
import LessonsPage from './components/LessonsPage.vue'
import NotSubscribedPage from './components/NotSubscribedPage.vue'
import LessonPage from './components/LessonPage.vue'
import JournalPage from './components/JournalPage.vue'
import AssignmentsPage from './components/AssignmentsPage.vue'
import AccessDenied from './components/AccessDenied.vue'
import AssignmentSubmissionsPage from './components/AssignmentSubmissionsPage.vue'
import SubmissionDetailsPage from './components/SubmissionDetailsPage.vue'
import { isAuthenticated } from './auth';
import { checkSubscription, checkEducator } from '@/utils/courseUtils';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'HomeContent',
                component: HomeContent,
            },
            {
                path: 'profile',
                name: 'Profile',
                component: ProfilePage,
            },
            {
                path: 'courses',
                name: 'Courses',
                component: CoursesPage
            },
            {
                path: 'my_courses',
                name: 'MyCourses',
                component: MyCoursesPage
            },
            {
                path: 'courses/:course_slug',
                name: 'CoursePage',
                component: CoursePage,
                beforeEnter: async (to, from, next) => {
                    const isSubscribed = await checkSubscription(to.params.course_slug);
                    if (isSubscribed) {
                        next();
                    } else {
                        next('/not-subscribed'); // Redirect to a not subscribed page or handle it differently
                    }
                },
                children: [
                    {
                        path: 'lessons',
                        name: 'Lessons',
                        component: LessonsPage,
                    },
                    {
                        path: 'lessons/:lesson_order',
                        name: 'LessonPage',
                        component: LessonPage,
                    },
                    {
                        path: 'journal',
                        name: 'Journal',
                        component: JournalPage,
                    },
                    {
                        path: 'assignments',
                        name: 'AssignmentsPage',
                        component: AssignmentsPage,
                        beforeEnter: checkEducator,
                    },
                    {
                        path: 'assignments/:assignment_id/submissions',
                        name: 'AssignmentSubmissions',
                        component: AssignmentSubmissionsPage,
                        beforeEnter: checkEducator,
                    },
                    {
                        path: 'submission/:submission_id',
                        name: 'SubmissionDetails',
                        component: SubmissionDetailsPage,
                        beforeEnter: checkEducator,
                    }
                ],
            },
            {
                path: 'courses/:course_slug/details',
                name: 'CourseDetails',
                component: CourseDetailsPage,
            },
            {
                path: 'not-subscribed',
                name: 'NotSubscribed',
                component: NotSubscribedPage, // Create a NotSubscribedPage component to show the error message
            },
            {
                path: '/access-denied',
                name: 'AccessDenied',
                component: AccessDenied
            },
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: SignIn,
    },
    {
        path: '/register',
        name: 'Register',
        component: SignUp,
    }, 
];


const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated()) {
            next({ path: '/login' });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
