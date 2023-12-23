<template>
    <div class="row">
      <ToggleButton class="col-4" buttonText="No Apron" />
      <ToggleButton class="col-4" buttonText="No Bunny Suit" />
      <ToggleButton class="col-4" buttonText="No Mask" />
    </div>
    <div class="row">
      <ToggleButton class="col-4" buttonText="No Gloves" />
      <ToggleButton class="col-4" buttonText="No Goggles" />
      <ToggleButton class="col-4" buttonText="No Headcap" />
    </div>
    <div class="row">
      <table v-if="msg.length > 0" class="table table-striped table-dark">
        <thead>
          <tr>
            <th>File Name</th>
            <th>TimeStamp</th>
            <th>Apron Count</th>
            <th>Bunnysuit Count</th>
            <th>Mask Count</th>
            <th>Gloves Count </th>
            <th>Goggles Count</th>
            <th>Headcap Count</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in msg" :key="index">
            <td>{{ item.fileName }} <a :href="item[1]" target="_blank">{{ item[0] }}</a></td>
            <td v-for="(value, key) in item.slice(2)" :key="key">{{ value }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>No logs available.</div>
    </div>
</template>

  
  <script>
  import axios from 'axios';
  import ToggleButton from './FilterButton.vue';
  
  export default {
    name: 'Logs',
    components:{
      ToggleButton,
    },
    data() {
      return {
        msg: [],
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

<style>

</style>