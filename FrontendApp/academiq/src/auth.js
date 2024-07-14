export function isAuthenticated() {
    const token = localStorage.getItem('authToken');
    console.log(token)
    return !!token;
}
