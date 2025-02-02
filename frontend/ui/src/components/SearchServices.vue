<template>
    <div class="container w-50 mt-5">
        <div class="d-flex justify-content-between align-content-center">
            <label for="serviceName" class="form-label m-2">Search for services: </label>
            <input type="text" v-model="serviceName" class="form-control m-2">
            <button class="btn btn-success m-2" @click="getServices">Search</button>
        </div>
        <div class="d-flex justify-content-center">
            <h6 class="text-success mt-5">{{ message }}</h6>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'SearchServices',
        data(){
            return{
                serviceName: '',
                services: [],
                message: 'Try searching for services...'
            }
        },
        methods:{
            getServices(e){{
                e.preventDefault();
                console.log(this.serviceName);
                // get services here
                fetch('http://127.0.0.1:5000/getservices', {
                    method: "POST",
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'serviceName': this.serviceName
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    this.services = data.services;
                    console.log(data.services)
                })
                // this.services = [];
                if(this.services.length === 0){
                    this.message = 'Hmm.. this service is not available. Try searching for another service :)';
                }else{
                    this.message = '';
                }
            }}
        }
    }
</script>

<style scoped>

</style>