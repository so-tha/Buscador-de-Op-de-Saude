<template>
  <div id="app">
    <SearchOperadoras />
  </div>
</template>

<script>
import SearchOperadoras from './components/PesquisaOperadoras.vue';

export default {
  name: 'App',
  components: {
    SearchOperadoras
  }
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
