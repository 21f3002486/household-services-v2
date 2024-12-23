<template>
    <div>
        <div>
            <br>
            <label for="emailId" name="emailId">Registered Email ID: </label>
            <input type="text" name="emailId" v-model="emailId">
            <br>
            <label for="password" name="password">Password: </label>
            <input type="password" name="password" v-model="password">
            <br>
            <input type="radio" id="admin" value="admin" v-model="role" checked="checked"/>
            <label for="admin">Admin</label>
            <input type="radio" id="customer" value="customer" v-model="role" />
            <label for="admin">Customer</label>
            <input type="radio" id="professional" value="professional" v-model="role" />
            <label for="professional">Professional</label>
            <br>
            <button @click="submitLogin">Login</button>
            <h1 style="color: red">{{ error }}</h1>
            <br>
            <br>
            <button><router-link to="/register">Create Account?</router-link></button>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'LoginPage',
        data(){
            return{
                emailId: '',
                password: '',
                role: 'admin',
                error: ''
            }
        },
        methods:{
            submitLogin(e){
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
                        'role': this.role
                     })
                };
                fetch("http://127.0.0.1:5000/login", data)
                .then(resp => resp.json())
                .then(data => {
                    if(data.message == "Login Successful"){
                        this.error = ''
                        this.$store.commit('loginUser', this.role, data.token)
                        localStorage.token = data.token;
                        if(this.role == "admin"){
                            this.$router.push('/admin')
                        }else if(this.role == "customer"){
                            this.$router.push('/customer')
                        }else{
                            this.$router.push('/professional')
                        }
                    }else{
                        this.error = data.message;
                    }
                })
                console.log("Frontend: "+this.emailId, this.password, this.role)
            }
        }
    }
</script>

<style scoped>

</style>