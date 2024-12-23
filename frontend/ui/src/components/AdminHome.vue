<template>
    <div>
        <div id="changethistonavbar" v-if="this.$store.state.role == 'admin'">
            <router-link to="/admin">Welcome to Admin's Dashboard</router-link>
            <!-- <button @click="showToken">Show token</button>
            <h3 v-if="token != '' ">{{ token }}</h3> -->
            <button><router-link to="/admin/allusers">Manage Users</router-link></button>
            <button><router-link to="/admin/services">Manage Services</router-link></button>
            <button><router-link to="/admin/requests">Manage Requests</router-link></button>
            <router-view/>
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
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
