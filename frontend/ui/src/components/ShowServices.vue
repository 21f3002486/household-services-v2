<template>
    <div>
        <div v-if="!show_update">
          <h4>Name: {{ service.name }}</h4> 
          <h5>Base Price: {{ service.price }}</h5>
          <h5 v-if="service.time_required <= 1">Time Required: {{ service.time_required }} hour</h5>
          <h5 v-else>Time Required: {{ service.time_required }} hours</h5>
          <p>Description: {{ service.description }}</p>

          <button @click="updateService">Update</button>
          <button @click="deleteService">Delete</button>
        </div>
        <div v-else>
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
            <button @click="emitUpdate">Update</button>
            <button @click="this.show_update = !this,show_update">Cancel</button>
        </div>
    </div>
</template>

<script>
  export default{
    name: 'ShowServices',
    props: ['service'],
    data(){
      return{
        name: this.service.name,
        price: this.service.price,
        time_required: this.service.time_required,
        description: this.service.description,
        show_update: false
      } 
    },
    methods:{
      emitUpdate(){
        console.log(this.service.service_id, this.name, this.price, this.time_required, this.description)
        this.$emit('update-service', this.service.service_id, this.name, this.price, this.time_required, this.description);
        this.name= this.service.name,
        this.price= this.service.price,
        this.time_required= this.service.time_required,
        this.description= this.service.description,
        this.show_update = false;
      },
      updateService(){
        this.show_update = true; 
      },
        deleteService(){
            this.$emit('delete-service', this.service.service_id)
        }
    }
  }
</script>
