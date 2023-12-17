<template>
      <button type="button" class="btn btn-primary">{{ msg }}</button>

  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Logs',
    data() {
      return {
        msg: '',
      };
    },
    methods: {
      getMessage() {
        const path = 'http://localhost:5001/allLogs';
        axios.get(path)
          .then((res) => {
            this.msg = res.data;
          })
          .catch((error) => {
  
            console.error(error);
          });
      },
    },
    created() {
      this.getMessage();
    },
  };
  </script>