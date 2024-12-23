<template>
    <div>
        <div v-if="!isapproved_flag">
            {{ error }}
        </div>
        <div v-else>
            Professional Things here
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
                    Authorization: "Bearer " + localStorage.token
                }
            })
            .then(resp => resp.json())
            .then(data =>{
                if(data.message == "Approved"){
                    this.isapproved = true;
                }else{
                    this.error = data.message;
                }
            })
        }
    }
</script>

<style scoped>

</style>
