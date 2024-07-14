<template>
    <div class="single-choice-question">
        <p>{{ question.text }}</p>
        <div v-for="option in options" :key="option">
            <label>
                <input type="radio" :name="'question-' + question.id" :value="option" @change="updateAnswer(option)">
                {{ option }}
            </label>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            question: {
                type: Object,
                required: true
            }
        },
        data() {
            return {
                selectedOption: null
            };
        },
        computed: {
            options() {
                return JSON.parse(this.question.options);
            }
        },
        methods: {
            updateAnswer(option) {
                this.selectedOption = option;
                this.$emit('answer', { questionOrder: this.question.order, answer: option });
            }
        }
    };
</script>

<style scoped>
    .single-choice-question {
        margin-bottom: 20px;
    }

    p {
        font-size: 16px;
        font-weight: bold;
    }

    label {
        display: block;
        margin-bottom: 5px;
    }
</style>
