<template>
    <div class="text-field-question">
        <p>{{ question.text }}</p>
        <textarea :name="'question-' + question.id" rows="4" v-model="answer"></textarea>
    </div>
</template>

<script>
    export default {
        props: {
            question: {
                type: Object,
                required: true
            },
            value: {
                type: String,
                default: ''
            }
        },
        data() {
            return {
                answer: this.value
            };
        },
        watch: {
            answer(newValue) {
                this.$emit('answer', { questionOrder: this.question.order, answer: newValue });
            }
        }
    };
</script>

<style scoped>
    .text-field-question {
        margin-bottom: 20px;
    }

    p {
        font-size: 16px;
        font-weight: bold;
    }

    textarea {
        width: 100%;
        padding: 10px;
        font-size: 14px;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
</style>
