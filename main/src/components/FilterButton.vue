<template>
  <div>
    <button class="btn" @click="toggleButton" :class="{ 'btn-secondary': isActive, 'btn-dark': !isActive }">
      {{ buttonText }}
    </button>
    <p v-if="isActive" class="mt-2">Button is active!</p>
  </div>
</template>

<script>
export default {
  name:'ToggleButton',
  props: {
    buttonText: {
      type: String,
      default: 'Toggle'
    }
  },
  data() {
    return {
      isActive: false
    };
  },
  methods: {
    toggleButton() {
      this.isActive = !this.isActive;
    }
  },
};
</script>

<style scoped>
/* Scoped styles specific to ToggleButton.vue */
</style>
