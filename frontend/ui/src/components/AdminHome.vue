<template>
    <div class="container">
        <div class="navbar justify-content-evenly" v-if="this.$store.state.role == 'admin'">
            <div>
                <router-link to="/admin/home">Welcome to Admin's Dashboard</router-link>
            </div>
            <!-- <button @click="showToken">Show token</button>
            <h3 v-if="token != '' ">{{ token }}</h3> -->
            <div class="justify-content-evenly">
                <button class="btn"><router-link to="/admin/allusers">Manage Users</router-link></button>
                <button class="btn"><router-link to="/admin/services">Manage Services</router-link></button>
                <button class="btn"><router-link to="/admin/requests">Manage Requests</router-link></button>
            </div>
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
        <router-view/>
        <!-- <AddNewService /> -->
    </div>
</template>

<script>
// import AddNewService from './AddNewService.vue';

    export default {
        name: 'AdminHome',
        data(){
            return{
                // token: ''
            }
        },
        methods:{
            // showToken(){
            //     this.token = localStorage.getItem('token')
            // }
        }  
    }
</script>

<style scoped>

</style>
