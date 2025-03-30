<template>
    <div v-if="!me['is_blocked']">
        <h4 class="m-5">Welcome {{ me['email_id'] }}!</h4>
        <h5 class="text-center m-5">Checkout available services or dive into your service requests!</h5>
    </div>
</template>

<script>
    export default {
        name: 'CustomerHome',
        data(){
            return{
                me: {},
                my_service_requests: {}
            }
        },
        methods:{
            getme(){
                fetch('http://127.0.0.1:5000/getme',{
                    method: "GET",
                    headers:{
                        'Authorization': 'Bearer ' + this.$store.state.token,
                        'Access-Control-Allow-Origin': "*"
                    }
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data)
                    this.me = data.me;
                    this.my_service_requests = data.my_service_requests
                })
            }
        },
        mounted(){
            this.getme();
        }
    }
</script>

<style scoped>

</style>