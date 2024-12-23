<template>
    <div>
        Logged Out successfully!
    </div>
</template>

<script>
    export default {
        name: 'LogOut',
        mounted(){
            localStorage.clear()
            this.$store.commit('logoutUser')
        }
    }
</script>

<style scoped>

</style>