<template>
    <div class="card m-1">
        <div v-if="!click_book" class="">
          <div class="">
            <h5>Name: {{ service.name }}</h5> 
            <h6>Base Price: {{ service.price }}</h6>
            <h6 v-if="service.time_required <= 1">Time Required: {{ service.time_required }} hour</h6>
            <h6 v-else>Time Required: {{ service.time_required }} hours</h6>
            <p>Description: {{ service.description }}</p>
          </div>
          <div>
            <button class="btn btn-success" @click="bookService">Book</button>
          </div>
        </div>
        <div v-else class="">
          <h6 class="text-success">Service successfully booked!</h6>
        </div>
    </div>
</template>

<script>
  export default{
    name: 'ShowServicesCustomer',
    props: ['service'],
    data(){
      return{
        name: this.service.name,
        price: this.service.price,
        time_required: this.service.time_required,
        description: this.service.description,
        // show_update: false
        click_book: false
      } 
    },
    methods:{
      bookService(e){
        this.$emit('bookService', this.service.service_id);
        this.click_book = true;
      }
    //   emitUpdate(){
    //     console.log(this.service.service_id, this.name, this.price, this.time_required, this.description)
    //     this.$emit('update-service', this.service.service_id, this.name, this.price, this.time_required, this.description);
    //     this.name= this.service.name,
    //     this.price= this.service.price,
    //     this.time_required= this.service.time_required,
    //     this.description= this.service.description,
    //     this.show_update = false;
    //   },
    //   updateService(){
    //     this.show_update = true; 
    //   },
    //     deleteService(){
    //         this.$emit('delete-service', this.service.service_id)
    //     }
    }
  }
</script>
