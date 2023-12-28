<template>
    <div class="row">
      <ToggleButton 
      class="col-4"
      v-for="(isActive, index) in buttonStates"
      :key="index"
      :buttonText="'No '+buttonTexts[index]"
      :index="index"
      :isActiveProp="isActive"
      @toggle="updateListState"/>
    </div>
    <div class="row">
      <table v-if="msg.length > 0" class="table table-striped table-dark">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Hostname</th>
            <th>TimeStamp</th>
            <th v-for="(objects) in buttonTexts">{{ objects }} Count</th>
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
        buttonStates: [true,true,true,true,true,true,],
        buttonTexts: ["Apron", "Bunnysuit", "Mask", "Gloves", "Goggles", "Headcap"],
        paramKeys:["aC","bSC","mC","gLC","gOC","hCC"],
      };
    },
    methods: {
      async getMessage() {
        await axios.get(`http://localhost:5001/allLogs/all`, {params:this.createParam(this.paramKeys,this.buttonStates)})
          .then((res) => {
            this.msg = res.data;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      updateListState(index, isActive){
        this.buttonStates.splice(index, 1, isActive);
        this.getMessage();
      },
      createParam(keys,states){
        const result = {};
        for (let i=0;i<keys.length; i++){
          const value = states[i] ? 1 : 0;
          if (value === 0) {
            result[keys[i]] = value;
          }
        }
        return result;
      },
    },
    created() {
      this.getMessage();
    },
  };
</script>

<style>

</style>