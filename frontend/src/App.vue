<template>
  <div class="wrapper">
  <div id="app">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
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
html, body{
  height: 100%;
}
body {
    background-image: url(./assets/background.jpeg) ;
    background-position: center center;
    background-repeat:  no-repeat;
    background-attachment: fixed;
    background-size:  cover;
    background-color: #999;
}

div, body{
  margin: 0;
  padding: 0;
  font-family: exo, sans-serif;

}
.wrapper {
  height: 100%;
  width: 100%;
}
</style>
