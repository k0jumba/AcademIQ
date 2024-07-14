import axios from '../axios';

export async function checkSubscription(courseSlug) {
    const token = localStorage.getItem('authToken');
    try {
        const response = await axios.get(`/courses/${courseSlug}/`, {
            headers: {
                Authorization: `Token ${token}`
            }
        });
        return response.data.is_subscribed;
    } catch (error) {
        console.error('Error checking subscription:', error);
        return false;
    }
}

export const checkEducator = async (to, from, next) => {
    const token = localStorage.getItem('authToken');
    try {
        const response = await axios.get('/profile/', {
            headers: {
                Authorization: `Token ${token}`
            }
        });
        if (response.data.educator) {
            next();
        } else {
            next({ path: '/access-denied' });
        }
    } catch (error) {
        console.error('Error during route guard check:', error);
        next({ path: '/access-denied' });
    }
};