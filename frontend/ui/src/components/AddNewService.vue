<template>
    <div>
        <div>
            <label for="serviceName">Sevice Name: </label>
            <input type="text" v-model="name">
            <br>
            <label for="description">Description: </label>
            <textarea v-model="description"/>
            <br>
            <label for="basePrice">Base Price: </label>
            <input type="number" v-model="price">
            <br>
            <label for="timeRequired">Time Required (in hours): </label>
            <input type="number" v-model="time_required">
            <br>
            <button @click="addservice">Add</button>
            <button><router-link to="/admin/services">Cancel</router-link></button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'AddNewService',
        data(){
            return{
                name: '',
                description: '',
                base_price: 0,
                time_required: 0
            }
        },
        methods:{
            addservice(){
                fetch('http://127.0.0.1:5000/addservice', {
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        'name': this.name,
                        'description': this.description,
                        'base_price': this.base_price,
                        'time_required': this.time_required
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data)
                })
                this.$router.push('/admin/services')
            }
        }
    }
</script>

<style scoped>

</style>