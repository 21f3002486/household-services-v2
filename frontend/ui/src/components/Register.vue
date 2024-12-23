<template>
    <div>
        <label for="">Register as: </label>
        <input type="radio" id="customer" value="customer" v-model="role" checked="checked"/>
        <label for="admin">Customer</label>
        <input type="radio" id="professional" value="professional" v-model="role" />
        <label for="professional">Professional</label>
        <br><br>
        <div v-if="role == 'customer'">
            <label for="emailId" name="emailId">Registered Email ID: </label>
            <input type="text" name="emailId" v-model="emailId">
            <br>
            <label for="password" name="password">Password: </label>
            <input type="password" name="password" v-model="password">
            <br>
            <label for="address" name="address">Address: </label>
            <input type="text" name="address" v-model="address">
            <br>
            <label for="number" name="number">Phone Number: </label>
            <input type="number" name="number" v-model="phone_number">
            <br>
            <button @click="submitCustomer">Register as Customer</button>
        </div>
        <div v-else>
            <label for="emailId" name="emailId">Registered Email ID: </label>
            <input type="text" name="emailId" v-model="emailId">
            <br>
            <label for="password" name="password">Password: </label>
            <input type="password" name="password" v-model="password">
            <br>
            <label for="service_type" name="service_type">Service Type: </label>
            <input type="text" name="service_type" v-model="service_type">
            <br>
            <label for="experience" name="experience">Experience (in years): </label>
            <input type="number" name="experience" v-model="experience">
            <br>
            <button @click="submitProfessional">Register as Professional</button>
        </div>
        <h3 style="color: red">{{ error }}</h3>
        <h3 style="color: green">{{ professional_message }}</h3>
    </div>
</template>

<script>
    export default {
        name: 'RegisterPeople',
        data(){
            return{
                role: 'customer',
                emailId: '',
                password: '',
                address: '',
                phone_number: '',
                service_type: '',
                experience: '',
                error: '',
                professional_message: ''
            }
        },
        methods:{
            submitCustomer(e){
                e.preventDefault();
                console.log("clicked submit customer")
                const data = {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    body: JSON.stringify({
                        'emailId': this.emailId,
                        'password': this.password,
                        'role': this.role,
                        'address': this.address,
                        'phone_number': this.phone_number
                     })
                };
                console.log("data created")
                fetch("http://127.0.0.1:5000/register", data)
                .then(resp => resp.json())
                .then(data => {
                    console.log("data recieved")
                    if(data.message == 'User created'){
                        this.error = ''
                        this.$router.push('/login')
                    }else{
                        this.error = data.message
                    }
                })
            },
            submitProfessional(e){
                e.preventDefault();
                const data = {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    body: JSON.stringify({
                        'emailId': this.emailId,
                        'password': this.password,
                        'role': this.role,
                        'service_type': this.service_type,
                        'experience': this.experience
                     })
                };
                fetch("http://127.0.0.1:5000/register", data)
                .then(resp => resp.json())
                .then(data => {
                    if(data.message == 'User created'){
                        this.error = ''
                        this.professional_message = "You will be able to login once the admin approves your profile"
                        // this.$router.push('/login')
                    }else{
                        this.error = data.message
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>