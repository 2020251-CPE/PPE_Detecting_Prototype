<template>
  <div class="container">
    <button type="button" class="btn btn-primary" @click="navigateToHome">{{ msg }}</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/ping';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navigateToHome() {
      this.$router.push({ path:'/' });
    }
  },
  created() {
    this.getMessage();
  },
};
</script>