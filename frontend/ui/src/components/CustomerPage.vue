<template>
    <div>
    <div v-if="this.$store.state.is_logged_in && this.$store.state.role=='customer'">
        Customer Page
        <button><router-link to='/customer/searchservices'>Search Services</router-link></button>
        My requests:
        <!-- Put previous requests here -->
        <router-link />
    </div>
    <div v-else>
        <div v-if="this.$store.state.role=='admin'">
            {{ this.$router.push('/admin') }}
        </div>
        <div v-if="this.$store.state.role=='professional'">
            {{ this.$router.push('/professional') }}
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
    </div>
</div>
</template>

<script>
    export default {
        name: 'CustomerPage'
    }
</script>

<style scoped>

</style>
