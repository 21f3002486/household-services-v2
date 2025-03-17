<template>
    <div class="container mt-4">
      <h2>Your Service Requests</h2>
      <div v-if="serviceRequests.length === 0">No service requests found.</div>
      
      <span v-if="message !== ''"><h5 class="text-danger">{{ message }}</h5></span>

      <div v-else class="row">
        <div v-for="request in serviceRequests" :key="request.service_request_id" class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <span v-if="message !== ''"><h5 class="text-danger">{{ message }}</h5></span>
              <h5 class="card-title">Service Name: {{ services.find(s => s.service_id === request.service_id).name }}</h5>
              <p class="card-text"><strong>Requested on:</strong> {{ request.date_of_request }}</p>
              <p class="card-text"><strong>Status:</strong> {{ request.service_status }}</p>
              <p class="card-text"><strong>Professional ID:</strong> {{ request.professional_id || "Not Assigned" }}</p>
              <p v-if="request.remarks" class="card-text"><strong>Remarks:</strong> {{ request.remarks }}</p>
  
              <!-- Edit & Delete Buttons -->
              <button class="btn btn-primary me-2" @click="editRequest(request.service_request_id)">Edit</button>
              <button class="btn btn-danger me-2" @click="deleteRequest(request.service_request_id)">Delete</button>
  
              <!-- Review Button (Only if Completed) -->
              <button v-if="request.service_status === 'closed'" class="btn btn-success" @click="reviewRequest(request.id)">
                Review
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
    export default {
        name: 'MyServiceRequests',
        data(){
            return{
                serviceRequests: [],
                services: [],
                professionals: [],
                message: ''
            }
        },
        methods:{
            async fetchServiceRequests() {
                try {
                    // Fetch services
                    const serviceResponse = await fetch('http://127.0.0.1:5000/getservices', {
                        method: "POST",
                        headers: {
                            'Authorization': 'Bearer ' + this.$store.state.token,
                            'Access-Control-Allow-Origin': "*",
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            serviceName: ''
                        })
                    });

                    const serviceData = await serviceResponse.json();
                    this.services = serviceData.services;

                    // Fetch service requests
                    const requestResponse = await fetch('http://127.0.0.1:5000/bookservice', {
                        method: "GET",
                        headers: {
                            'Authorization': 'Bearer ' + this.$store.state.token,
                            'Access-Control-Allow-Origin': "*"
                        }
                    });

                    const requestData = await requestResponse.json();
                    this.serviceRequests = requestData.service_requests;

                } catch (error) {
                    console.error("Error fetching service requests:", error);
                }
            },
            deleteRequest(id){
                console.log(id, ': service req to be deleted')
                fetch('http://127.0.0.1:5000/deleteservicerequest', {
                    method: "POST",
                    headers: {
                        'Access-Control-Allow-Origin': "*",
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        'id': id
                    })
                })
                .then(resp => resp.json())
                .then(data => {
                    console.log(data);
                    this.message = data.message;
                })
            }
        },
        mounted(){
            this.fetchServiceRequests();
        }
    }
</script>

<style scoped>

</style>