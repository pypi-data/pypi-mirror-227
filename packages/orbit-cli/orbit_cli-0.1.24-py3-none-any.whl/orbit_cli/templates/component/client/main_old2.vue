<template>
    <n-dialog-provider>
        <n-message-provider placement="bottom-right">
            <{{ project }}Component :router="router"/>
        </n-message-provider>
    </n-dialog-provider>
</template>

<script>
import { defineComponent, ref } from 'vue';
import { NDialogProvider, NMessageProvider } from 'naive-ui';
import {{ project }}Component from './{{ project }}Component.vue';
const router = ref(null)

export default defineComponent({
    name: '{{ project }}',
    components: { {{ project }}Component, NDialogProvider, NMessageProvider },
    install (app, options) {
        app.component('{{ project }}', this);
        (options.buttons||[]).forEach((button) => {
            options.router.addRoute(button)
            options.menu.push(button)
        })
        router.value = options.router
    },
    computed: {
        router () { return router }
    },
})
</script>