<template>
    <div class="not-subscribed-container">
        <h1>You are not subscribed to this course</h1>
        <p>Please subscribe to access this content.</p>
    </div>
</template>

<script>
export default {
    name: 'NotSubscribedPage',
};
</script>

<style scoped>
    .not-subscribed-container {
        padding: 20px;
        text-align: center;
    }

        .not-subscribed-container h1 {
            font-size: 24px;
            color: #ff0000;
        }

        .not-subscribed-container p {
            font-size: 18px;
        }
</style>
