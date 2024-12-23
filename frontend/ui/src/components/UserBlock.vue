<template>
    <div>
        {{ user.email_id }}
        <button v-if="this.is_blocked" @click="updateUserStatus">Unblock</button>
        <button v-else @click="updateUserStatus">Block</button>
    </div>
</template>

<script>
    export default {
        name: 'UserBlock',
        props: ['user'],
        data(){
            return{
                user_id: this.user.user_id,
                is_blocked: this.user.is_blocked
            }
        },
        methods:{
            updateUserStatus(){
                this.$emit('bub', this.user_id, this.is_blocked)
                this.is_blocked = !this.is_blocked
            }
        }
    }
</script>

<style scoped>

</style>