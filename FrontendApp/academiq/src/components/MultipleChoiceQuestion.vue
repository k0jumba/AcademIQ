<template>
    <div class="multiple-choice-question">
        <p>{{ question.text }}</p>
        <div v-for="option in options" :key="option">
            <label>
                <input type="checkbox" :value="option" @change="updateAnswer(option, $event)">
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
                selectedOptions: []
            };
        },
        computed: {
            options() {
                return JSON.parse(this.question.options);
            }
        },
        methods: {
            updateAnswer(option, event) {
                if (event.target.checked) {
                    this.selectedOptions.push(option);
                } else {
                    const index = this.selectedOptions.indexOf(option);
                    if (index !== -1) {
                        this.selectedOptions.splice(index, 1);
                    }
                }
                this.$emit('answer', { questionOrder: this.question.order, answer: this.selectedOptions });
            }
        }
    };
</script>

<style scoped>
    .multiple-choice-question {
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
