<template>
    <div class="container">
        <!-- Is approved flag: {{ isapproved_flag }} -->
    <div v-if="!isapproved_flag">
        {{ error }}
    </div>
    <div v-else-if="this.$store.state.is_logged_in && this.$store.state.role=='professional' && !this.$store.state.is_blocked">
        Professional Page
    </div>
    <div v-else-if="this.$store.state.is_blocked">
        You have been blocked by the admin.
    </div>
    <div v-else>
        <div v-if="this.$store.state.role=='admin'">
            {{ this.$router.push('/admin') }}
        </div>
        <div v-if="this.$store.state.role=='customer'">
            {{ this.$router.push('/customer') }}
        </div>
        <div v-else>
            {{ this.$router.push('/login') }}
        </div>
    </div>
</div>
</template>

<script>
    export default {
        name: 'ProfessionalPage',
        data(){
            return{
                isapproved_flag: false,
                error: ''
            }
        },
        beforeMount(){
            fetch('http://127.0.0.1:5000/isaccepted', {
                method: "GET",
                headers:{
                    "Authorization": "Bearer " + this.$store.state.token,
                    "Access-Control-Allow-Origin": "*"
                }
            })
            .then(resp => resp.json())
            .then(data =>{
                if(data.message == "Approved"){
                    this.isapproved_flag = true;
                }else{
                    this.error = data.message;
                }
            })
        }
    }
</script>

<style scoped>

</style>
