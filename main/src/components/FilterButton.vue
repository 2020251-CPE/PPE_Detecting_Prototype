<template>
  <div>
    <button class="btn" @click="toggleButton" :class="{ 'btn-dark': isActive, 'btn-secondary': !isActive }">
      {{ buttonText }}
    </button>
  </div>
</template>

<script>
export default {
  name:'ToggleButton',
  props: {
    buttonText: { type: String, required: true, default: 'Toggle' },
    index:{ type:Number, required: true },
    isActiveProp:{ type:Boolean, required: true, default:false}
  },
  data() {
    return {
      isActive: this.isActiveProp
    };
  },
  methods: {
    toggleButton() {
      this.isActive = !this.isActive;
      this.$emit('toggle', this.index, this.isActive);
    }
  },
};
</script>

<style scoped>
/* Scoped styles specific to ToggleButton.vue */
</style>
