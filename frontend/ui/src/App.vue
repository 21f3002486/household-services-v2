<template>
  <div>
    <!-- {{ storedata }} -->
    <nav class="d-flex justify-content-center">
      <div v-if="!this.$store.state.is_logged_in">
        <button class="btn"><router-link to="/login">Login</router-link></button> | 
        <button class="btn"><router-link to="/register">Register</router-link></button>
      </div>
      <div v-else>
        <button><router-link to="/logout">Logout</router-link></button>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
  export default{
    name: 'App',
    computed:{
      // storedata(){
      //   return this.$store.state
      // }
    }
  }
</script>

<style>

/*
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
*/

a { text-decoration: none; }
router-link { text-decoration: none;}
@import'~bootstrap/dist/css/bootstrap.css'
</style>
