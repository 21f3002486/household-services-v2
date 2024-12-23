<template>
    <div>
        <h3 style="color: red">{{ error }}</h3>

        Customers:
        <UserBlock 
            v-for="customer in customers" 
            :key="customer.user_id" 
            :user="customer" 
            @bub="updateUserStatus"
        />

        Professionals:
        <UserBlock 
            v-for="professional in professionals" 
            :key="professional.user_id" 
            :user="professional" 
            @bub="updateUserStatus" 
        />
    </div>
</template>

<script>
import UserBlock from './UserBlock.vue';

    export default {
        name: 'AllUsers',
        components: {UserBlock},
        data(){
            return {
                customers: [],
                professionals: [],
                error: ''
            }
        },
        methods:{
            updateUserStatus(user_id, is_blocked){
                console.log("Parent: ", user_id, is_blocked);
                fetch('http://127.0.0.1:5000/getUsers', {
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'user_id': user_id,
                        'is_blocked': !is_blocked
                    })
                })
                .then(resp => resp.json())
                .then(data =>{
                    if(data.message=="Success"){
                        console.log("User blocked/unblocked successfully");
                    }else{
                        console.log(data.message);
                    }
                })
            }
        },
        mounted(){
            fetch("http://127.0.0.1:5000/getUsers")
            .then(resp => resp.json())
            .then(data => {
                if(data.message == "Successful"){
                    this.customers = data.customers
                    this.professionals = data.professionals
                }else{
                    this.error = data.message
                }
            })
        }
    }
</script>

<style scoped>

</style>
