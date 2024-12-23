<template>
  <div>
    <ExpandableCard 
      v-for="professional in profos"
      :key="professional.user_id"
      :professional="professional"
      @approve="approveProfessional"
    />
  </div>
</template>

<script>
import ExpandableCard from './ExpandableCard.vue';
  export default{
    name: 'ProfessionalRequests',
    components: {ExpandableCard},
    data(){
      return{
        profos: []
      }
    },
    methods:{
      approveProfessional(user_id){
        console.log(user_id+" to be approved");
        // backend call here
        const data = {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({
                'user_id': user_id
              })
        };
        fetch("http://127.0.0.1:5000/professionalrequests", data)
        .then(resp => resp.json())
        .then(data => {
          console.log(data)
        })
      }
    },
    beforeMount(){
      fetch('http://127.0.0.1:5000/professionalrequests')
      .then(resp => resp.json())
      .then(data => {
        if(data.message=="Got requests"){
          this.profos = data.professionals;
        }
      })
    }
  }
</script>
